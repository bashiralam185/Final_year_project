from dash import Dash, dash_table, html
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
from collections import OrderedDict

app = Dash(__name__)

df_typing_formatting = pd.DataFrame(OrderedDict([
    ('year', [2022]),
    ('month', [2]),
    ('day', [3]),
    ('hour', [5]),
    ('nowcast', [16.9]),
    ('aqi', [70]),
    ('raw', [46.0])
]))

app.layout = html.Div([
    dash_table.DataTable(
        id='typing_formatting',
        data=df_typing_formatting.to_dict('records'),
        columns=[{
            'id': 'year',
            'name': 'Year',
            'type': 'numeric'
        }, {
            'id': 'month',
            'name': 'Month',
            'type': 'numeric',
        }, {
            'id': 'day',
            'name': 'Day',
            'type': 'numeric',
        }, {
            'id': 'hour',
            'name': 'Hour',
            'type': 'numeric',
        },{
            'id':'aqi',
            'name':"AQI",
            'type':'numeric',
        },{
            'id':'nowcast',
            'name':"NowCast Conc.",
            'type':'numeric',
        },{
            'id':'raw',
            'name':"Raw Conc.",
            'type':'numeric',
        }
        ],
        editable=True,
        style_table={'overflowX': 'scroll'}
    )
])

print(df_typing_formatting)

if __name__ == '__main__':
    app.run_server(debug=True)
