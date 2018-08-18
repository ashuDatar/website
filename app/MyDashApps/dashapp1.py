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
import dash_table_experiments as dt

# In[2]:






# In[ ]:




def select_chart(x_axis,y_axis,chart_type,file) :
    data_chart = file
    dataPanda = []
    state_list = ['CHANDIGARH', 'HARYANA', 'HIMACHAL_PRADESH', 'JAMMU_KASHMIR','NCT_OF_DELHI','PUNJAB','RAJASTHAN',
                  'ARUNACHAL_PRADESH','ASSAM','MANIPUR','MEGHALAYA','MIZORAM','NAGALAND','TRIPURA','ANDAMAN_NICOBAR_ISLANDS',
                  'BIHAR','JHARKHAND','ODISHA','SIKKIM','WEST_BENGAL','CHHATTISGARH','MADHYA_PRADESH','UTTARAKHAND',
                  'UTTAR_PRADESH','DADRANAGAR_HAVELI','DAMAN_DIU','GOA','GUJARAT','MAHARASHTRA','ANDHRA_PRADESH',
                  'KARNATAKA','KERALA','LAKSHADWEEP','PUDUCHERRY','TAMIL_NADU','TELANGANA','All_India']
    dataPanda = create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list)
    for i in range(0,36):
        dataPanda[i]['visible'] = False
    return dataPanda
     

    

def create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list):    
    if (x_axis == 'Date'):
            dataPanda = create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list)
    else:
            dataPanda = create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list)
    return dataPanda



def create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list) : 
    x=data_chart[data_chart['Description'] == y_axis]['Date']
    if (chart_type == 'scatter'): 
            for i in state_list:
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
            for i in state_list:
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
                for i in state_list:
                        trace = go.Bar(
                            x=x,
                            y=data_chart[data_chart['Description'] == y_axis][i],
                            text= i,
                            opacity=0.7,
                            name=i  ) 
                        dataPanda.append(trace)            
    return dataPanda


def create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list) : 
    if (chart_type == 'scatter'): 
            for i in state_list:
                trace = go.Scatter(
                    x=data_chart[data_chart['Metric'] == x_axis][i],
                    y=data_chart[data_chart['Metric'] == y_axis][i],
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
            for i in state_list:
                    trace = go.Scatter(
                                x=data_chart[data_chart['Metric'] == x_axis][i],
                                y=data_chart[data_chart['Metric'] == y_axis][i],
                                text= i,
                                mode = 'lines',
                                opacity=0.7,
                                name=i  ) 
                    dataPanda.append(trace)
        else:            
            if (chart_type == 'bar'): 
                    for i in state_list:
                            trace = go.Bar(
                                    x=data_chart[data_chart['Metric'] == x_axis][i],
                                    y=data_chart[data_chart['Metric'] == y_axis][i],
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

                xaxis = dict(title= 'Date'),

                yaxis=dict(title='Outstanding loans of Scheduled commercial banks  in semi urban areas'),

                #legend=dict(orientation="h"),
               
                hovermode='closest',
              
                showlegend=True

            )

    return layout


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


     html.Div( dt.DataTable(id='datatable', rows=[{}]) #, style={'display': 'none'}
             ),  
    
    # html.Div(id='text'),
    
     #dcc.Location(id='url', refresh=False),
    

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
                    value='bar'
                        )
            ],
           className='four columns',
           style={'margin-top': '10'}
     )

        ], className='row'
   ),

  #chart
   # html.Div(
   #    [
   #       dcc.Graph(id='example-graph',
                              #animate=True, 
   #                         style={'margin-top': '20'},
   #                          config={'displayModeBar': False}
   #                )
   #     ], className='row'
   #      ),

    dcc.Markdown('Created by [Ashutosh Datar](https://twitter.com/adatar)')
], className='ten columns offset-by-one')    




DashServer.css.append_css({'external_url':

#                 'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'

                  'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'

               })

DashServer.title = 'States of India'

@DashServer.callback(
    dash.dependencies.Output('datatable', 'rows'),[dash.dependencies.Input('chart_type', 'value')])
def update_data(chart_type):
    #data = db.session.query(test_data_dummy_data)
    #file = pd.read_sql(data.statement, data.session.bind)
    file = pd.read_csv('Test_Data_Dummy_Data.csv')
    file.iloc[:,16:52] = file.iloc[:,16:52].apply(lambda x : x.astype('float'))
    file.iloc[:,16:52] = file.iloc[:,16:52].apply(lambda x : round(x, 2))
    cleaned_df = file.to_dict('records')
    #dataframe = file.to_json(date_format='iso', orient='split')
    return cleaned_df




layout = DashServer.layout

    
