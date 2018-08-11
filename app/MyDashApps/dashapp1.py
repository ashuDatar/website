from app.Dashserver import DashServer
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash
import dash_core_components as dcc
import pandas as pd
from bisect import bisect_left
from datetime import datetime
from copy import deepcopy
import plotly.graph_objs as go
from flask import Flask, render_template
from app.server import db
from app.models import test_data_dummy_data
import urllib


# In[2]:






# In[ ]:




def select_chart(x_axis,y_axis,chart_type,file) :

    data_chart = file

    dataPanda = []

    dataPanda = create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)

    return dataPanda

     

    

def create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda):    

    if (x_axis == 'Date'):

            dataPanda = create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)

    else:

            dataPanda = create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)

    return dataPanda





def create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda) : 

    x=data_chart[data_chart['Description'] == y_axis]['Date']

    if (chart_type == 'scatter'): 

            for i in data_chart.iloc[:,15:51].columns.unique():

                trace = go.Scatter(

                    x=x,

                    y=data_chart[data_chart['Description'] == y_axis][i],

                    text= i,

                    mode='markers',

                    opacity=0.7,

                    marker={

                        'size': 15,

                        'line': {'width': 0.5, 'color': 'white'}

                    },

                    name=i  ) 

                dataPanda.append(trace)

    else:            

        if (chart_type == 'line'): 

            for i in data_chart.iloc[:,15:51].columns.unique():

                    trace = go.Scatter(

                            x=x,

                            y=data_chart[data_chart['Description'] == y_axis][i],

                            text= i,

                            mode = 'lines',

                            opacity=0.7,

                            name=i  ) 

                    dataPanda.append(trace)

        else:            

            if (chart_type == 'bar'): 

                for i in data_chart.iloc[:,15:51].columns.unique():

                        trace = go.Bar(

                            x=x,

                            y=data_chart[data_chart['Description'] == y_axis][i],

                            text= i,

                            opacity=0.7,

                            name=i  ) 

                        dataPanda.append(trace)            

    return dataPanda



def create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda) : 

    if (chart_type == 'scatter'): 

            for i in data_chart.iloc[:,15:51].columns.unique():

                trace = go.Scatter(

                    x=data_chart[data_chart['Description'] == x_axis][i],

                    y=data_chart[data_chart['Description'] == y_axis][i],

                    text= i,

                    mode='markers',

                    opacity=0.7,

                    marker={

                        'size': 15,

                        'line': {'width': 0.5, 'color': 'white'}

                    },

                    name=i  ) 

                dataPanda.append(trace)

    else :            

        if (chart_type == 'line'): 

            for i in data_chart.iloc[:,15:51].columns.unique():

                    trace = go.Scatter(

                                x=data_chart[data_chart['Description'] == x_axis][i],

                                y=data_chart[data_chart['Description'] == y_axis][i],

                                text= i,

                                mode = 'lines',

                                opacity=0.7,

                                name=i  ) 

                    dataPanda.append(trace)

        else:            

            if (chart_type == 'bar'): 

                    for i in data_chart.iloc[:,15:51].columns.unique():

                            trace = go.Bar(

                                    x=data_chart[data_chart['Description'] == x_axis][i],

                                    y=data_chart[data_chart['Description'] == y_axis][i],

                                    text= i,

                                    opacity=0.7,

                                    name=i  ) 

                            dataPanda.append(trace)            

    return dataPanda





    

def create_layout(x_axis,y_axis) : 

    layout =  go.Layout(

               # autosize=False,

               # width=1000,

                height=700,

                xaxis = dict(title= x_axis),

                yaxis=dict(title=y_axis),

                legend=dict(orientation="h"),

                hovermode='closest'

            )

    return layout





#

#Define x and y axis options



#x_axis_list = file['Metric'].unique().tolist()

#y_axis_list = file['Metric'].unique().tolist()

#x_axis_list.append('Date')





DashServer.css.append_css({'external_url':

#                 'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'

                  'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'

               })

DashServer.title = 'States of India'

#server = app.server



DashServer.layout = html.Div([

    # title row

    html.Div(

        [

            html.H1(

                'States of India',

                style={'font-family': 'Helvetica',

                       "margin-top": "25",

                       "margin-bottom": "0"},

                className='eight columns',

            ),

             html.P(

                'Explore states of India',

                style={'font-family': 'Helvetica',

                       "font-size": "120%",

                       "width": "80%"},

                className='eight columns',

            ),

        ], 

         className='row'

        ),

    

    # Select visualization

    

     html.Div(

        [

  

    # selectors

     html.Div(

        [

        

    

       html.Div(

        [

            html.P('Choose chart-type:'), 

            dcc.Dropdown(

                    id='chart_type',

                    options=[{'label': 'Scatter', 'value': 'scatter'},

                             {'label': 'Line', 'value': 'line'},

                             {'label': 'Bar', 'value': 'bar'}],

                    value='scatter'

                        )

            ],

           className='four columns',

           style={'margin-top': '10'}

     )

        ], className='row'

   ),

    

  #chart

     html.Div(

        [

            dcc.Graph(id='example-graph',

                              #animate=True, 

                              style={'margin-top': '20'},

                               config={'displayModeBar': False}

                     )

        ], className='row'

         ),

    

    dcc.Markdown('Created by [Ashutosh Datar](https://twitter.com/adatar)')

   

], className='ten columns offset-by-one')    



@DashServer.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('chart_type', 'value'),
    dash.dependencies.Input('url', 'pathname'),
    ])
def update_output(chart_type, pathname):
    des = str(pathname)
    filter = des.split('/')[-1]
    filter = urllib.parse.unquote(filter)
    #data = db.session.query(test_data_dummy_data)
    #file = pd.read_sql(data.statement, data.session.bind)
    file = pd.read_csv('Test_Data_Dummy_Data.csv')
    file.iloc[:,15:51] = file.iloc[:,15:51].apply(lambda x : x.astype('float'))
    file.iloc[:,15:51] = file.iloc[:,15:51].apply(lambda x : round(x, 2))
    x_axis = 'Date'
    y_axis = filter
    dataPanda = select_chart(x_axis,y_axis,chart_type,file)
    layout = create_layout(x_axis,y_axis)
    figure = {'data': dataPanda,
            'layout': layout}
    return figure  

  
layout = DashServer.layout

    
