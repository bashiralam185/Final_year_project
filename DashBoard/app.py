from dash import Dash, html, dcc, Input, Output, ctx
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# importing the dataset
bishkek_data = pd.read_csv("assets/Bishkek_data.csv")
data = pd.read_csv("assets/pm2_data.csv")
pollutants = pd.read_csv("assets/grid-export.csv")

#preprocessing of the datasets
data.dropna(inplace=True)
pollutants['Day'] = pd.to_datetime(pollutants['Day'])
data = data.replace('Unhealthy for Sensitive Groups', 'USG')



app = Dash(__name__)
server =  app.server

app.layout = html.Div([
    html.Div(html.H1( children='Analyze, predict and forecast Air Pollution in Bishkek'), className='Heading'),
    html.Hr(),

    html.Div([
    html.Div(html.Button('Analyze', id='btn-nclicks-1', n_clicks=0), className='top_button'),
    html.Div(html.Button('Predictions', id='btn-nclicks-2', n_clicks=0), className='top_button'),
    html.Div(html.Button('Forecasting', id='btn-nclicks-3', n_clicks=0), className='top_button')],
    className='buttons'),
    html.Hr(),
    html.Div(id='container-button-timestamp'),
    html.Label("Air Pollutants from 2019-2022 in Bishkek"),
    
])

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):
    if "btn-nclicks-1" == ctx.triggered_id:
        graph_1 = px.line(bishkek_data, x="Date", y="median", color='Specie', title='Bishkek City')
        graph_2 = px.pie(data, names='AQI Category', title='Quality of Air in Bishkek from 2019 to 2022', width=400, height=400)
        graph_3 = px.bar(data, x="Year", y="AQI",color="AQI Category",  barmode='group', title="Bishkek air pollution per year", width=600, height=400)
        graph_5 = px.line(data, x="Date (LT)", y="AQI",  title='AQI of Bishkek city from 2019 to 2022')
        graph_4 = px.line(pollutants, x="Day", y="PM1(mcg/m³)", title='Concentration of pollutants in Bishkek Air')
        # y can have values from [min, max, median, variance]
        y = 'median' 
        return html.Div([
            # first graph inside the analyze button
            html.Div([
            html.Div(),
            html.Div(dcc.Graph(id = "pollutant",
              figure=graph_1)
              )]), 
            
            # second graph inside the analyze button
            html.Div([
                html.Div(
                    dcc.Graph(id='pie_chat', 
                              figure=graph_2) 
                ), 
                html.Div(
                    dcc.Graph(
                        id='bar_chart',
                        figure=graph_3
                    ),
                )
            ], className='SecondGraph'),

            #third graph
            html.Div(
            dcc.Graph(id='AQI', 
                      figure=graph_4)
            ), 

            ## fifth graph
            html.Div(
            dcc.Graph(id='air_pollutants',
                      figure=graph_5)
            )

              ], className='analyze')
    
    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "Button 2 was most recently clicked"
    elif "btn-nclicks-3" == ctx.triggered_id:
        msg = "Button 3 was most recently clicked"
    

if __name__ == "__main__":
    app.run_server(debug=True)