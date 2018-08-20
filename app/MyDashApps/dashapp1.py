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
#import dash_table_experiments as dt

# In[2]:






# In[ ]:




def select_chart(x_axis,y_axis,chart_type,file,state) :
    data_chart = file
    dataPanda = []
    state_list = state
    dataPanda = create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda,state_list)
    #for i in range(0,36):
        #dataPanda[i]['visible'] = False
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

                yaxis=dict(title=y_axis),

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


    #html.Div( dt.DataTable(id='datatable', rows=[{}]) ),  
    
     html.Div(id='text'),
    
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
           className='ten columns',
           style={'margin-top': '10'}
     ),
            
      html.Div(
        [ 
       dcc.RadioItems(
        id='toggle',
        options=[{'label': i, 'value': i} for i in ['Show Edit Options', 'Hide Edit Options']],
        value='Hide Edit Options'
    )
        ],
           className='two columns',
           style={'margin-top': '15'}
      )    

        ], className='row'
   ),

  #chart
    html.Div(
        [ 
       html.Div(
        [
            dcc.Graph(id='example-graph',
                              #animate=True, 
                              style={'margin-top': '20'}
                              , config = {'showLink': True} 
                              #,config={'displayModeBar': False}
                     )
        ], className='ten    columns',
            ),
            
       html.Div(id='controls-container', children=
        [
            dcc.Checklist(
                id='state',
               options=[
                     {'label': 'CHANDIGARH', 'value': 'CHANDIGARH'},
                     {'label': 'HARYANA', 'value': 'HARYANA'},
                     {'label': 'HIMACHAL PRADESH', 'value': 'HIMACHAL_PRADESH'},
                     {'label': 'JAMMU & KASHMIR', 'value': 'JAMMU_KASHMIR'},
                     {'label': 'NCT OF DELHI', 'value': 'NCT_OF_DELHI'},
                     {'label': 'PUNJAB', 'value': 'PUNJAB'},
                     {'label': 'RAJASTHAN', 'value': 'RAJASTHAN'},
                     {'label': 'ARUNACHAL PRADESH', 'value': 'ARUNACHAL_PRADESH'},
                     {'label': 'ASSAM', 'value': 'ASSAM'},
                     {'label': 'MANIPUR', 'value': 'MANIPUR'},
                     {'label': 'MEGHALAYA', 'value': 'MEGHALAYA'},
                     {'label': 'MIZORAM', 'value': 'MIZORAM'},
                     {'label': 'NAGALAND', 'value': 'NAGALAND'},
                     {'label': 'TRIPURA', 'value': 'TRIPURA'},
                     {'label': 'ANDAMAN & NICOBAR ISLANDS', 'value': 'ANDAMAN_NICOBAR_ISLANDS'},
                     {'label': 'BIHAR', 'value': 'BIHAR'},
                     {'label': 'JHARKHAND', 'value': 'JHARKHAND'},
                     {'label': 'ODISHA', 'value': 'ODISHA'},
                     {'label': 'SIKKIM', 'value': 'SIKKIM'},
                     {'label': 'WEST BENGAL', 'value': 'WEST_BENGAL'},
                     {'label': 'CHHATTISGARH', 'value': 'CHHATTISGARH'},
                     {'label': 'MADHYA PRADESH', 'value': 'MADHYA_PRADESH'},
                     {'label': 'UTTARAKHAND', 'value': 'UTTARAKHAND'},
                     {'label': 'UTTAR PRADESH', 'value': 'UTTAR_PRADESH'},
                     {'label': 'DADRANAGAR HAVELI', 'value': 'DADRANAGAR_HAVELI'},
                     {'label': 'DAMAN DIU', 'value': 'DAMAN_DIU'},
                     {'label': 'GOA', 'value': 'GOA'},
                     {'label': 'GUJARAT', 'value': 'GUJARAT'},
                     {'label': 'MAHARASHTRA', 'value': 'MAHARASHTRA'},
                     {'label': 'ANDHRA PRADESH', 'value': 'ANDHRA_PRADESH'},
                     {'label': 'KARNATAKA', 'value': 'KARNATAKA'},
                     {'label': 'KERALA', 'value': 'KERALA'},
                     {'label': 'LAKSHADWEEP', 'value': 'LAKSHADWEEP'},
                     {'label': 'PUDUCHERRY', 'value': 'PUDUCHERRY'},
                     {'label': 'TAMIL NADU', 'value': 'TAMIL_NADU'},
                     {'label': 'TELANGANA', 'value': 'TELANGANA'},
                     {'label': 'All India', 'value': 'All_India'}
                       ],
                  values=['All_India']#,
                  #labelStyle={'width':'100px', 'display': 'inline-block', 'padding-right':'20px'} 
                         )
        ], className='two columns',
             style={'margin-top': '20'} 
            )
         ], className='row'   
            ),


    dcc.Markdown('Created by [Ashutosh Datar](https://twitter.com/adatar)')
], className='ten columns offset-by-one')    




DashServer.css.append_css({'external_url':

#                 'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'

                  'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'

               })

DashServer.title = 'States of India'

@DashServer.callback(
    dash.dependencies.Output('text', 'children'),
    [dash.dependencies.Input('chart_type', 'value'),
     dash.dependencies.Input('url', 'pathname')
    ])
def update_output(chart_type, pathname):
    des = str(pathname)
    filter = des.split('/')[-1]
    filter = urllib.parse.unquote(filter)
    #file = pd.DataFrame(rows)
    data = db.session.query(test_data_dummy_data)
    file = pd.read_sql(data.statement, data.session.bind)
    #file = pd.read_csv('Test_Data_Dummy_Data.csv')
    category = file[file['Description'] == filter].Category.unique()
    source = file[file['Description'] == filter].Source.unique()
    return html.Div([
        html.H3('Visualization for {}'.format(filter)),
        html.H4('Series:{}'.format(category)),
        html.H6('Source:{}'.format(source))
         ])


@DashServer.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('chart_type', 'value'),
     #dash.dependencies.Input('datatable', 'rows'),
     dash.dependencies.Input('url', 'pathname'),
     dash.dependencies.Input ('state', 'values')
    ])
def update_output(chart_type, pathname, state):
    des = str(pathname)
    #des = str('Outstanding loans of Scheduled commercial banks  in semi urban areas')
    filter = des.split('/')[-1]
    filter = urllib.parse.unquote(filter)
    data = db.session.query(test_data_dummy_data)
    file = pd.read_sql(data.statement, data.session.bind)
    #file = pd.read_csv('Test_Data_Dummy_Data.csv')
    #file.iloc[:,15:51] = file.iloc[:,16:52].apply(lambda x : x.astype('float'))
    #file.iloc[:,15:51] = file.iloc[:,16:52].apply(lambda x : round(x, 2))
    #file = pd.DataFrame.from_dict(datatable, orient='index')
    #file = pd.DataFrame(rows)
    x_axis = 'Date'
    y_axis = filter
    dataPanda = select_chart(x_axis,y_axis,chart_type,file,state)
    layout = create_layout(x_axis,y_axis)
    figure = {'data': dataPanda,
              'layout': layout}
    return figure

@DashServer.callback(Output('controls-container', 'style'), [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Hide Edit Options':
        return {'display': 'none'}
    else:
        return {'display': 'block'}

layout = DashServer.layout

    
