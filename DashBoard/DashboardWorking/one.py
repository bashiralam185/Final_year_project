from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import pickle


one = Dash(__name__)

params = [
    'year', 'month', 'day', 'hour',
    'nowcast', 'aqi', 'raw'
]

one.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': p, 'name': p} for p in params]
        ),
        data=[
            dict(Model=i, **{param: 0 for param in params})
            for i in range(1)
        ],
        editable=True
    ),
    html.Div(
    html.Div(id="example-output")
    ),
])


@one.callback(
    Output('example-output', 'children'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    input_value = df.values[:1]
    pickled_model = pickle.load(open('CatBoost', 'rb'))
    pred = pickled_model.predict(input_value)
    pred1 = "The predicted air quality is  " + pred[0]
    return pred1

if __name__ == '__main__':
    one.run_server(debug=True)
