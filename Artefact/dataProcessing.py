# Importing modules
import pandas as pd
import pygal
from pathlib import Path
import sys

# Get the directory of the current script
script_dir = Path(__file__).parent

# Construct the path to the source data CSV file and where the cleaned data and statistics will be saved
sourceDataPath = script_dir / "data/DDA02.20241213T091229.csv"
cleanedDataPath = script_dir / "data/cleanedData.csv"
genderPayGapPath = script_dir / "data/genderPayGap.csv"
sectorSummaryPath = script_dir / "data/sectorSummary.csv"
sexSummaryPath = script_dir / "data/sexSummary.csv"
yearSummaryPath = script_dir / "data/yearSummary.csv"


expectedTypes = {
    'Statistic Label': 'object',
    'Year': 'int64',
    'Sex': 'object',
    'NACE Rev 2 Sector': 'object',
    'Age Group': 'object',
    'UNIT': 'object',
    'VALUE': 'float64',
}

# Cleaning data function
def cleanData(df):
    # Check for incorrect data types
    for column, expectedType in expectedTypes.items():
        if df[column].dtype != expectedType:
            print(f"Error: Column '{column}' has incorrect data type. Expected {expectedType}, but got {df[column].dtype}.")
            sys.exit(1)
    # Check for missing values
    filteredDf = df[df["Statistic Label"] != "Annual Change (Median Annual Earnings)"]
    if filteredDf.isnull().values.any():
        print("Error: There are missing values in the dataset.")
        sys.exit(1)
    else:
        # Create a new column for the annual change values
        df["Annual Change (%)"] = pd.Series(df[df["Statistic Label"] == "Annual Change (Median Annual Earnings)"]["VALUE"].values)
    
        # Drop redundant rows
        df = df.drop(df[df["Statistic Label"] == "Annual Change (Median Annual Earnings)"].index)
    
        # Rename the value column
        df = df.rename(columns={"VALUE": "Median Annual Earnings (€)"})
    
        # Reorder columns
        df = df[['Year', 'Sex', 'NACE Rev 2 Sector', 'Age Group', 'Median Annual Earnings (€)', 'UNIT', 'Annual Change (%)']]
    
        # Drop redundant/unused columns
        df = df.drop(columns=["UNIT", "Age Group"])
    
        # Return cleaned data
        return df


# Get summary statistics function
def getSummary(df, groupByColumn):
    
    # Group data by the specified column
    groups = {group: data for group, data in df.groupby(groupByColumn)}
    
    # Initialize a list to store the results
    results = []
    
    # Iterate over each group to calculate summary statistics for mean, median, max and min values
    for name, group in groups.items():
        meanValues = group.mean(numeric_only=True).round(2)
        medianValues = group.median(numeric_only=True).round(2)
        maxValue = group.max(numeric_only=True).round(2)
        minValue = group.min(numeric_only=True).round(2)
        
        # Create a dictionary with the summary statistics for the current group
        result = {
            groupByColumn: name,
            'Mean Annual Earnings': meanValues.get('Median Annual Earnings (€)', None),
            'Median Annual Earnings': medianValues.get('Median Annual Earnings (€)', None),
            'Max Annual Earnings': maxValue.get('Median Annual Earnings (€)', None),
            'Min Annual Earnings': minValue.get('Median Annual Earnings (€)', None),
            'Mean Annual Change': meanValues.get('Annual Change (%)', None),
            'Median Annual Change': medianValues.get('Annual Change (%)', None),
            'Max Annual Change': maxValue.get('Annual Change (%)', None),
            'Min Annual Change': minValue.get('Annual Change (%)', None),
        }
        # Append the result to the results list
        results.append(result)
    
    # Create a dataframe from the results list
    summary = pd.DataFrame(results)
    
    # Return the summary statistics and the grouped data
    return summary, groups

def createGraph(data, title, years):
    
    # Create a line graph using pygal
    lineGraph = pygal.Line()
    
    # Set the graph title as a variable and the axis labels
    lineGraph.title = title
    lineGraph.x_title = "Year"
    lineGraph.y_title = "Median Annual Earnings (€)"
    lineGraph.x_labels = years
    
    # Add data for each sector
    for sector in data['NACE Rev 2 Sector'].unique():
        currentSector = data[data['NACE Rev 2 Sector'] == sector]
        currentEarnings = [
            currentSector[currentSector['Year'] == year]['Median Annual Earnings (€)'].mean()
            if year in currentSector['Year'].values
            else None
            for year in years
        ]
        
        # Add the data to the graph and include labels for the values with the euro symbol
        lineGraph.add(sector, [{"value": e, "label": f" €{e:.2f}"} if e else None for e in currentEarnings])
    
    # Render the graph as a unicode string
    return lineGraph.render(is_unicode=True)

# Function to create and save graphs
def saveGraphs(both, female, male, years):

    # Use the createGraph function to create graphs for each sex
    bothGraph = createGraph(both, "Median Annual Earnings by Sector Over Time (Both Sexes)", years)
    maleGraph = createGraph(male, "Median Annual Earnings by Sector Over Time (Male Only)", years)
    femaleGraph = createGraph(female, "Median Annual Earnings by Sector Over Time (Female Only)", years)
    
    # Save graphs to files in the static folder
    with open(script_dir / "static/bothGraph.svg", "w", encoding="utf-8") as f:
        f.write(bothGraph)
    with open(script_dir / "static/maleGraph.svg", "w", encoding="utf-8") as f:
        f.write(maleGraph)
    with open(script_dir / "static/femaleGraph.svg", "w", encoding="utf-8") as f:
        f.write(femaleGraph)



# Function to generate a new dataframe with gender pay gap statistics
def gpgStatistics(male, female):
    
    # Merge the male and female dataframes
    genderPayGap = male.merge(female, on=['Year', 'NACE Rev 2 Sector'], suffixes=('_Male', '_Female'))
    
    # Calculate the difference in earnings
    genderPayGap['Difference in Earnings (€)'] = genderPayGap['Median Annual Earnings (€)_Male'] - genderPayGap['Median Annual Earnings (€)_Female']
    
    # Calculate the difference in annual change
    genderPayGap['Difference in Annual Change (%)'] = (genderPayGap['Annual Change (%)_Male'] - genderPayGap['Annual Change (%)_Female']).round(1)
    
    # Calculate the gender paygap as the difference in earnings as a percentage
    genderPayGap['Gender Pay Gap (%)'] = ((genderPayGap['Difference in Earnings (€)'] / genderPayGap['Median Annual Earnings (€)_Male']) * 100).round(2)
    
    # Sort the data by sector and year
    genderPayGap = genderPayGap.sort_values(by=['NACE Rev 2 Sector', 'Year'])
    
    # Calculate the change in gender paygap between years for each sector
    genderPayGap['Change in Gender Pay Gap (%)'] = genderPayGap.groupby('NACE Rev 2 Sector')['Gender Pay Gap (%)'].diff().round(2)
    
    # Reorder columns and dropping redundant columns and return the dataframe
    genderPayGap = genderPayGap[['Year', 'NACE Rev 2 Sector', 'Difference in Earnings (€)', 'Difference in Annual Change (%)', 'Gender Pay Gap (%)', 'Change in Gender Pay Gap (%)']]
    return genderPayGap

# Function to analyse the data and generate summary statistics and graphs
def analyseData(df):
    # Get summary statistics
    sectorSummary, sectors = getSummary(df, 'NACE Rev 2 Sector')
    sexSummary, sexes = getSummary(df, 'Sex')
    yearSummary, years = getSummary(df, 'Year')
    #Creating new dataframes for each sex
    male = sexes["Male"].drop(columns="Sex")
    female = sexes["Female"].drop(columns="Sex")
    # Save graphs
    saveGraphs(sexes['Both sexes'], sexes['Female'], sexes['Male'], list(years.keys()))
    # Calculate gender pay gap statistics
    genderPayGap = gpgStatistics(male, female)
    # Return summaries and gender pay gap statistics
    return sectorSummary, sexSummary, yearSummary, male, female, genderPayGap



if __name__ == '__main__':
    # Read the source data CSV file
    df = pd.read_csv(sourceDataPath)
    
    # Clean the data
    df = cleanData(df)
    
    # Save the cleaned data to a CSV file
    df.to_csv(cleanedDataPath, index=None, header=True)
    
    # Analyse the data and save graphs
    sectorSummary, sexSummary, yearSummary, male, female, genderPayGap = analyseData(df)

    # Save the summaries and gender pay gap statistics to CSV files
    sectorSummary.to_csv(sectorSummaryPath, index=False, header=True)
    sexSummary.to_csv(sexSummaryPath, index=False, header=True)
    yearSummary.to_csv(yearSummaryPath, index=False, header=True)
    genderPayGap.to_csv(genderPayGapPath, index=False, header=True)