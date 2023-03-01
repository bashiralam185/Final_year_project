from dash import Dash, html, dcc, Input, Output, ctx
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# importing the dataset
bishkek_data = pd.read_csv("assets/Bishkek_data.csv")

# plotting graphs in Python of all pollutants 
fig = px.line(bishkek_data, x="Date", y="median", color='Specie', title='Bishkek City')



app = Dash(__name__)
server =  app.server

app.layout = html.Div([
    html.Div(html.H1( children='Analyze, predict and forecasting Air Pollution in Bishkek'), className='Heading'),
    html.Hr(),

    html.Div([
    html.Div(html.Button('Analyze', id='btn-nclicks-1', n_clicks=0), className='top_button'),
    html.Div(html.Button('Predictions', id='btn-nclicks-2', n_clicks=0), className='top_button'),
    html.Div(html.Button('Forecasting', id='btn-nclicks-3', n_clicks=0), className='top_button')],
    className='buttons'),
    html.Hr(),
    html.Div(id='container-button-timestamp'),
    html.Label("Air Pollutants from 2019-2022 in Bishkek"),
    html.Div(
    dcc.Graph(id = "pollutants",
              figure=fig)
    )
    
])

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):
    msg = "None of the buttons have been clicked yet"
    if "btn-nclicks-1" == ctx.triggered_id:
        msg = "Button 1 was most recently clicked"
    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "Button 2 was most recently clicked"
    elif "btn-nclicks-3" == ctx.triggered_id:
        msg = "Button 3 was most recently clicked"
    return html.Div(msg)

if __name__ == "__main__":
    app.run_server(debug=True)