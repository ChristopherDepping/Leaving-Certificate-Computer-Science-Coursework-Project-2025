# Importing modules
from flask import Flask, render_template, request, jsonify, redirect
from dash import dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlite3
from collections import Counter

# Load the cleaned data
df = pd.read_csv(r"data/cleanedData.csv")

# Initialise the Flask server
server = Flask(__name__)

# Initialise the first Dash app
app1 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash1/")

# Define the layout of the first Dash app
app1.layout = html.Div([
    # Title of the app
    html.H1(children='Annual Earnings Estimates and Associated Annual Change by Sex and NACE Rev 2 Sector', style={'textAlign': 'center'}),

    # Dropdown to filter by sex
    html.Div([
        dcc.Dropdown(
            id='sex-dropdown',
            options=[{'label': sex, 'value': sex} for sex in df['Sex'].unique()],
            value='Both sexes'
        ),
    ]),

    # Dropdown to filter by sector
    html.Div([
        dcc.Dropdown(
            id='sector-dropdown',
            options=[{'label': sector, 'value': sector} for sector in df['NACE Rev 2 Sector'].unique()],
            value='Accommodation and food service activities (I)'
        ),
        # Radio Buttons to select the data points to be displayed
         dcc.RadioItems(
            options=['Median Annual Earnings (€)', 'Annual Change (%)'],
            value='Median Annual Earnings (€)',
            id='graph-controls'
        ),       
    ]),

    dcc.Graph(id='graph-content')
])

# Define the callback function to update the graph based on the selected filters
@app1.callback(
    Output('graph-content', 'figure'),
    Input('sex-dropdown', 'value'),
    Input('sector-dropdown', 'value'),
    Input('graph-controls', 'value')
)
def updateGraph1(sex, sector, column):
    # Filter the data based on the selected sex and sector
    dff = df[(df['Sex'] == sex) & (df['NACE Rev 2 Sector'] == sector)]
    # Return the line graph of the selected data
    return px.line(dff, x='Year', y=column, title=f'{column} for {sector} by Year ({sex})')

# Initalise the second Dash app
app2 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash2/")

# Define the layout of the second Dash app
app2.layout = html.Div([
    # Title of the app
    html.H1(children='Annual Earnings Estimates and Associated Annual Change by Sex and NACE Rev 2 Sector', style={'textAlign': 'center'}),

    # Dropdown to filter by year
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': str(year)} for year in df['Year'].unique()],
            value='2023'
        ),
    ]),

    # Dropdown to filter by sex
    html.Div([
        dcc.Dropdown(
            id='sex-dropdown',
            options=[{'label': sex, 'value': sex} for sex in df['Sex'].unique()],
            value='Both sexes'
        ),
        # Radio Buttons to select the data points to be displayed
        dcc.RadioItems(
            options=['Median Annual Earnings (€)', 'Annual Change (%)'],
            value='Median Annual Earnings (€)',
            id='graph-controls'
        ),
    ]),

    dcc.Graph(id='graph-content', style={'height': '700px', 'width': '100%'})
])

# Define the callback function to update the graph based on the selected filters
@app2.callback(
    Output('graph-content', 'figure'),
    Input('sex-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('graph-controls', 'value')
)
# Function to update the graph based on the selected filters
def updateGraph2(sex, year, column):
    # Filter the data based on the selected sex and year
    dff = df[(df['Sex'] == sex) & (df['Year'] == int(year))]
    # Return the bar chart of the selected data
    return px.histogram(dff, x='NACE Rev 2 Sector', y=column, title=f'{column} in {year} by Sector ({sex})')

# Load the gender pay gap dataset
gpg = pd.read_csv("data/genderPayGap.csv")

# Initialise the third Dash app
app3 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash3/")

# Define the layout of the third Dash app
app3.layout = html.Div([
    # Title of the app
    html.H2("Gender Pay Gap By NACE Rev 2 Sector"),
    # Create a table from the gender pay gap dataset
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in gpg.columns],
        data=gpg.to_dict('records'),
        page_size=13,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )
])

# Load the sector summary dataset
sectSum = pd.read_csv("data/sectorSummary.csv")

# Initialise the fourth Dash app
app4 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash4/")

# Define the layout of the fourth Dash app
app4.layout = html.Div([
    # Title of the app
    html.H2("Sector Summary"),
    # Create a table from the sector summary dataset
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in sectSum.columns],
        data=sectSum.to_dict('records'),
        page_size=14,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )
])

# Load the sex summary dataset
sexSum = pd.read_csv("data/sexSummary.csv")

# Initialise the fifth Dash app
app5 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash5/")

# Define the layout of the fifth Dash app
app5.layout = html.Div([
    # Title of the app
    html.H2("Sex Summary"),
    # Create a table from the sex summary dataset
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in sexSum.columns],
        data=sexSum.to_dict('records'),
        page_size=3,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )
])

# Load the year summary dataset
yearSum = pd.read_csv("data/yearSummary.csv")

# Initialise the sixth Dash app
app6 = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash6/")

# Define the layout of the sixth Dash app
app6.layout = html.Div([
    # Title of the app
    html.H2("Year Summary"),
    # Create a table from the year summary dataset
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in yearSum.columns],
        data=yearSum.to_dict('records'),
        page_size=14,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )
])

# Initialise the SQLite database
def init_db():
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT,
            factors TEXT,
            payGap REAL,
            '''
            # Add a column to store the value of the response to 
            # the government question as a boolean
            '''
            gov BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()
init_db()

# Define the route for the home page of the Flask server
@server.route('/')
def home():
    # Render the home page
    return render_template('index.html')

# Define the route for the Pygal graphs page
@server.route('/pygal')
def pygalCharts():
    return render_template('pygal.html')

# Define the route for the Dash graphs page                       
@server.route('/dash')
def dashCharts():
    return render_template('dash.html')

# Define the route for the data page
@server.route('/data')
def render_dash3():
    return render_template('data.html')

# Define the route for the survey page
@server.route('/poll')
def survey_poll():
    # Render the survey page
    return render_template('poll.html')

# Define the route to handle survey submission
@server.route('/submit', methods=['POST'])
# Function to submit the survey form
def submit():
    sector = request.form['sector']
    factors = request.form['factors']
    payGap = float(request.form['payGap'])
    gov = bool(int(request.form.get('gov', 0)))
    with sqlite3.connect('survey.db') as conn:
        conn.execute("INSERT INTO responses (sector, factors, payGap, gov) VALUES (?, ?, ?, ?)", 
                        (sector, factors, payGap, gov))
    print("Form submitted successfully.")
    
    # Redirect to the summary page after submission
    return redirect('/summary')

@server.route('/summary')
def summary():
    # Retrieve the survey responses from the database
    with sqlite3.connect('survey.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM responses")
        responses = cursor.fetchall()
    
    # Create a DataFrame from the responses    
    df = pd.DataFrame(responses, columns=['id', 'sector', 'factors', 'payGap', 'gov'])
    # Convert gov column to a boolean
    df['gov'] = df['gov'].astype(bool)
    # If there are no responses, render the summary page with no responses
    if df.empty:
        return render_template('summary.html', yes="No responses", no="No responses", message="No survey responses available.")
    
    # Calculate the mode of the sector column and the mean of the payGap column
    sectorMode = df['sector'].mode()[0] if not df['sector'].empty else "No responses"
    payGapMean = df['payGap'].astype(float).mean() if not df['payGap'].empty else 0.0
    
    # Calculate the percentage of yes and no responses
    totalResponses = len(df)
    yesCount = (df['gov'] == 1).sum()
    noCount = (df['gov'] == 0).sum()
    yesPercentage = round((yesCount / totalResponses) * 100, 2) if totalResponses > 0 else 0
    noPercentage = round((noCount / totalResponses) * 100, 2) if totalResponses > 0 else 0
    
    # Render the summary page with the calculated data summary
    return render_template('summary.html', 
                           yes=yesPercentage, 
                           no=noPercentage, 
                           sector=sectorMode, 
                           payGap=round(payGapMean, 2),
                           responses=responses,
                           message=None)

# Define the route for the recommendations page
@server.route('/recommendations')
def recommendations():
    with sqlite3.connect('survey.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM responses")
        responses = cursor.fetchall()
    
    # Create a DataFrame from the responses
    df = pd.DataFrame(responses, columns=['id', 'sector', 'factors', 'payGap', 'gov'])
    df['gov'] = df['gov'].astype(bool)
    if df.empty:
        return render_template('recommendations.html', message="No responses available to make recommendations.")
    payGapMean = df['payGap'].astype(float).mean() if not df['payGap'].empty else 0.0
    totalResponses = len(df)
    yesCount = (df['gov'] == 1).sum()
    noCount = (df['gov'] == 0).sum()
    yesPercentage = round((yesCount / totalResponses) * 100, 2) if totalResponses > 0 else 0
    noPercentage = round((noCount / totalResponses) * 100, 2) if totalResponses > 0 else 0
    
    # Determine the consensus message
    if yesPercentage > 50:
        consensusMessage = "Based on the survey responses, the consensus is that the government is doing enough to address the gender pay gap."
    elif noPercentage > 50:
        consensusMessage = "Based on the survey responses, the consensus is that the government is not doing enough to address the gender pay gap."
    else:
        consensusMessage = "Based on the survey responses, there is no clear consensus on whether the government is doing enough to address the gender pay gap."
    
    # Calculate the percentage difference between the mean estimated gender pay gap and the actual statistic
    actualPayGap = 17.27  # From the genderPayGap csv as the statistic for gender pay gap for All NACE Rev 2 Sectors in 2023
    percentageDifference = (payGapMean - actualPayGap)
    
    # Determine the estimation message
    if percentageDifference >= 10:
        estimationMessage = "The estimated gender pay gap is significantly higher than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is much wider than it actually is, and that perhaps too much emphasis is being placed on the gender pay gap."
    elif percentageDifference <= -10:
        estimationMessage = "The estimated gender pay gap is significantly lower than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is much narrower than it actually is, and that perhaps not enough emphasis is being placed on the gender pay gap."
    elif percentageDifference >= 5:
        estimationMessage = "The estimated gender pay gap is somewhat higher than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is wider than it actually is, and that perhaps a bit more emphasis is being placed on the gender pay gap than " \
        "is needed."
    elif percentageDifference <= -5:
        estimationMessage = "The estimated gender pay gap is somewhat lower than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is narrower than it actually is, and that perhaps a bit less emphasis is being placed on the gender pay gap " \
        "than is needed."   
    elif percentageDifference >  2.5:
        estimationMessage = "The estimated gender pay gap is a little higher than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is a only a little wider than it actually is, and that relatively enough emphasis is being placed on the " \
        "gender pay gap."
    elif percentageDifference < -2.5:
        estimationMessage = "The estimated gender pay gap is a little lower than the actual statistic, indicating that the public believe " \
        "that the gender pay gap is a only a little narrower than it actually is, and that relatively enough emphasis is being placed on the " \
        "gender pay gap."  
    else:
        estimationMessage = "The estimated gender pay gap is within an acceptable range (2.5%) of the actual statistic, indicating that the public " \
        "have a good understanding of the gender pay gap."
    
    # Identify the three most answered responses to the factors question that have occurred three or more times
    factorsResponses = [response[2] for response in responses]
    factorsCounter = Counter(factorsResponses)
    modalFactors = [factor for factor, count in factorsCounter.items() if count >= 3]
    topFactors = modalFactors[:3]

    # Render the recommendations page with the calculated data
    return render_template('recommendations.html', 
                           consensusMessage=consensusMessage, 
                           estimationMessage=estimationMessage,
                           payGapMean=round(payGapMean, 2),
                           actualPayGap=actualPayGap,
                           percentageDifference=round(percentageDifference, 2),
                           topFactors=topFactors,
                           message=None)

# Run the Flask Server
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
