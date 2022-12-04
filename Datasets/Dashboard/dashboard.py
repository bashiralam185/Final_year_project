# importing required modules
from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from catboost import CatBoostRegressor
import tensorflow as tf

# ---------------------------------------------------------------------
external_stylesheets = ["assets/style.css"]
app = Dash(__name__)
server =  app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# --------------------------------Data importing------------------------------------
# reading dataset
data = pd.read_csv("../grid/grid-export.csv")
data['Day'] = pd.to_datetime(data['Day'])

# creating dataset for PM1
pm1 = data.drop('PM10(mcg/m³)', axis=1)
pm1 = pm1.drop('PM2.5(mcg/m³)', axis = 1)
pm1 = pm1.drop('Day', axis=1)

# input and output of dataset
X = pm1.drop('PM1(mcg/m³)', axis=1)
Y = pm1['PM1(mcg/m³)']

# ----------------------------------------Training and splitting of dataset------------------------------------------------
# splitting into testing and training parts
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0)

# initialzing the model
model_reg = lgb.LGBMRegressor()
# train the model
model_reg.fit(X_train,y_train)
# Making predictions
reg_pred = model_reg.predict(X_test)


# initializing the CatBoost regressor
CatBoost_rg = CatBoostRegressor()
# training the catboost Regressor model
CatBoost_rg.fit(X_train, y_train)
# making predictions
catboost_pred = CatBoost_rg.predict(X_test)


# creating neural networks for regression, input layer and output layer
model = tf.keras.Sequential([tf.keras.layers.InputLayer(
    input_shape=7),
    # second hidden layer with 20 nodes
  tf.keras.layers.Dense(20, activation = tf.keras.activations.relu),
                                 # building hiden layer with 10 nodes
  tf.keras.layers.Dense(10, activation = tf.keras.activations.relu),
    tf.keras.layers.Dense(1)])
# second step is to compile neural networks for regression
model.compile(loss=tf.keras.losses.mae,
                optimizer=tf.keras.optimizers.Adam(),
                metrics=['mae'])
#traing model with 50 epochs 
model.fit(tf.expand_dims(X_train, axis=-1), y_train, epochs=200)
# making predictions using neural networks for regression
y_preds = model.predict(X_test)




# ----------------------------------------Plotting graph-------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(x=[i for i in range(len(y_test))], y=reg_pred,
                    mode='lines',
                    name='Predicted values'))
fig.add_trace(go.Scatter(x=[i for i in range(len(y_test))], y=y_test,
                    mode='lines',
                    name='Actual values'))
fig.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title ={
        'text': "PM1-Prediction using LighGBM",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=[i for i in range(len(y_test))], y=catboost_pred,
                    mode='lines',
                    name='Predicted values'))
fig1.add_trace(go.Scatter(x=[i for i in range(len(y_test))], y=y_test,
                    mode='lines',
                    name='Actual values'))
fig1.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title ={
        'text': "PM1-Prediction using Catboost",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)


# layout of dashboard ---------------------------------------------------------------------------------
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Final Year Project Visualizations',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Regression models to predict PM1, PM2.5 and PM10', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='dashboard4',
        figure=fig
    ),
    dcc.Graph(
        id='dashboard4',
        figure=fig1
    )
])

# ----------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)


