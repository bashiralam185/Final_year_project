from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


app = Dash(__name__)
server =  app.server


app.layout = html.Div(
    html.H1( children='Analyze, predict and forecasting Air Pollution in Bishkek')
)


if __name__ == "__main__":
    app.run_server(debug=True)