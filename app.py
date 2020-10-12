import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pdb
from threading import Thread
import dash_table
from dash.dependencies import Input, Output
import datetime
import time
from collections import deque

prices = deque(maxlen=10)
msg_body = {}
summation = {}

# start another thread listening to different sources
# navigation bar
def read_price():
    with open('hi1.csv', 'r') as f:
        for line in f:
            data_fields= line.replace('\ufeff','').replace('\n','').split(',')
            prices.append(data_fields)
            time.sleep(2)


def simulate_realtime():
    with open('sample_volume.txt', 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            elements = line.split(';')
            msg_body[elements[0]] = float(elements[1].strip())
            time.sleep(2)
            try :
                summation[elements[0]] = summation[elements[0]] + float(elements[1].strip())
            except KeyError:
                summation[elements[0]] = float(elements[1].strip())


task1 = Thread(target=simulate_realtime)
task2 = Thread(target=read_price)
task1.start()
task2.start()

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']

app = dash.Dash("Alan Pattern", external_stylesheets=external_stylesheets)

app.layout=html.Div([
            #nav bar
            html.Nav(
                #inside div
                [html.Ul([
                    html.Li(html.A(
                        'Dashboard Analytics',
                        href='/'
                    )), 
                    html.Li(html.A(
                        'Alan',
                        href='/'
                    )),
                    html.Li(html.A(
                        'Handsome boy',
                        href='/'
                    ))
                ], style={'margin': 'auto', 'padding':'0.5em'}
                    ),
                ]),
    html.Div([
        html.Div([
        html.H3("Bid-Ask Volume"),
        dcc.Interval(
            id = 'interval-component',
            interval = 2000,
            n_intervals = 0
        ),
        dash_table.DataTable(
            id = 'bid-ask-vol',
            columns = [{"name":i, "id": i} for i in ['symbol', 'time', 'ratio']],
            data = [],
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio}>1'
                    },
                    'background' : 'dodgerblue',
                    'color' : 'white',
                },
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio}<1'
                    },
                    'color' : 'white',
                    'background' : 'tomato'
                },
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio}==1'
                    },
                    'color' : 'black',
                    'background' : 'RRGGBB'
                }
            ],
            style_table={
                'overflowY': 'scroll',
                'overflowX': 'hidden'
            }
        )
    ], className="col s4 m4 l4", style={'margin': 'auto', 'alignSelf': 'top'}),
    # start of second table.
    html.Div([
        html.H3("consolidation ratio"),
        dash_table.DataTable(
            id = 'consolidation',
            columns = [{"name":i, "id": i} for i in ['symbol', 'time', 'ratio']],
            data = [],
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio}>30'
                    },
                    'background' : '#228B22',
                    'color' : 'white',
                },
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio}<20'
                    },
                    'color' : 'white',
                    'background' : '#FA8072'
                },
                {
                    'if': {
                        'column_id': 'ratio',
                        'filter_query': '{ratio} >= 20 && {ratio} <=30'
                    },
                    'color' : 'black',
                    'background' : 'RRGGBB'
                }
            ],
            style_table={
                'overflowY': 'scroll',
                'overflowX': 'hidden'
            }
        )
    ], className="col s4 m4 l4", style={'margin': 'auto', 'alignSelf': 'top'}),
    # start of second table.
    html.Div([
        html.H3("futures prices"),
        dash_table.DataTable(
            id = 'futures_price',
            columns = [{"name":i, "id": i} for i in ['timestamp', 'open', 'close', 'high', 'low']],
            data = []
        )
    ], className="col s4 m4 l4", style={'margin': 'auto', 'alignSelf': 'top'})
    ], style={'display': 'flex', 'flexDirection': 'row'}),
])

@app.callback(Output('bid-ask-vol', 'data'),
              [Input('interval-component', 'n_intervals')])
def bidaskvol(val):
    data = []
    for i in msg_body.keys():
        time_now = str(datetime.datetime.now())
        current = [i,time_now, msg_body[i]]
        data.append(current)
    df_final = pd.DataFrame(data =data,columns = ['symbol', 'time', 'ratio'])
    return round(df_final,5).to_dict('records')

@app.callback(Output('consolidation', 'data'),
              [Input('interval-component', 'n_intervals')])
def consolidation(val):
    data = []
    for i in summation.keys():
        time_now = str(datetime.datetime.now())
        current = [i,time_now, summation[i]]
        data.append(current)
    df_final = pd.DataFrame(data =data,columns = ['symbol', 'time', 'ratio'])
    return round(df_final,5).to_dict('records')

@app.callback(Output('futures_price', 'data'),
              [Input('interval-component', 'n_intervals')])
def futures(val):
    df_final = pd.DataFrame(data=prices,columns = ['timestamp', 'open', 'close', 'high', 'low'])
    return round(df_final,5).to_dict('records')

if __name__ =='__main__':
    app.run_server(debug=True)


