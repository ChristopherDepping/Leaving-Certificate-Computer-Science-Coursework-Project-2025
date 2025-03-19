# Annual Earnings and Gender Pay Gap Analysis

This project analyzes annual earnings and gender pay gap data, generates summary statistics, and creates interactive visualizations using Flask and Dash.

## Requirements

The project requires the following Python packages:

- dash==2.18.2
- Flask==2.1.2
- pandas==2.2.3
- plotly==6.0.0
- pygal==3.0.5

These packages are listed in the `requirements.txt` file.
They can be installed with the following command:

pip install -r requirements.txt

## Running the Application

If you would like to see the data processing in action, feel free to delete everything in the 'data' folder, besides DDA02.20241213T091229.csv (The original dataset), as well as the three scg files in the static folder, and run dataProcessing.py. This will generate the data and graphs again.

To start the application, you can use the start_app.bat file. This batch file will set up the necessary environment variables and run the Flask server.

## Application Routes

Home Page: http://localhost:5000/
Pygal Graphs: http://localhost:5000/pygal
Dash Graphs: http://localhost:5000/dash
Data Page: http://localhost:5000/data
Survey Page: http://localhost:5000/poll
Summary Page: http://localhost:5000/summary
Recommendations Page: http://localhost:5000/recommendations