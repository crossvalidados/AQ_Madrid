#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import datetime as dt
import itertools

import numpy as np
import matplotlib.tri as tri
import import_data

import base64
with open("./assets/map.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
#add the prefix that plotly will want when using the string as source
encoded_image = "data:image/png;base64," + encoded_string

compuestos = {"Dióxido de Azufre": 1, "Monóxido de Carbono" : 6, "Monóxido de Nitrógeno": 7, "Dióxido de Nitrógeno": 8, "Partículas < 2.5 µm": 9, "Partículas < 10 µm": 10, "Óxidos de Nitrógeno": 12, "Ozono": 14, "Tolueno": 20, "Benceno": 30, "Etilbenceno": 35, "Metaxileno": 37, "Paraxileno": 38, "Ortoxileno": 39}
horas = {"1 AM": "H01", "2 AM": "H02", "3 AM": "H03", "4 AM": "H04", "5 AM": "H05", "6 AM": "H06", "7 AM": "H07", "8 AM": "H08", "9 AM": "H09", "10 AM": "H10", "11 AM": "H11", "12 AM": "H12", "1 PM": "H13", "2 PM": "H14", "3 PM": "H15", "4 PM": "H16", "5 PM": "H17"}

data = import_data.generar_datos()

if dt.datetime.now().minute > 20:
    time_now = horas[list(dict(itertools.islice(horas.items(), dt.datetime.now().hour)).keys())[-1]]
else:
    time_now = horas[list(dict(itertools.islice(horas.items(), dt.datetime.now().hour)).keys())[-2]]


def actualizar_datos(tiempo, variable):
    global datos, width, height, z, x, y, x_mean, y_mean

    datos = data.iloc[np.where(data.MAGNITUD == variable)[0], :]
    width = np.max(datos["lon"])-np.min(datos["lon"])
    height = np.max(datos["lat"])-np.min(datos["lat"])

    z = datos[tiempo].values
    if variable == 6:
        z = z * 1000

    x = datos["lon"].values
    y = datos["lat"].values
    y_mean = np.mean(y)
    x_mean = np.mean(x)

def interpolation(x, y, z):

    ngridx = 200
    ngridy = 200

    xi = np.linspace(np.min(x), np.max(x), ngridx)
    yi = np.linspace(np.min(y), np.max(y), ngridy)

    triang = tri.Triangulation(x, y)
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)

    return(xi, yi, zi)

app = dash.Dash()
app.scripts.config.serve_locally=True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"})
server = app.server


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    },
    'header': {
        'height': '60px',
        'line-height': '60px',
        'padding': '5px',
        'padding-left': '10px',
        'backgroundColor': '#333333'
    },
    'title': {
        'font-size': '26px',
        'padding-left:': '10px',
        'color': '#ffffff'
    },
    'logo': {
        'float': 'right',
        'padding-left': '15px',
        'padding': '10px'
    },
    'plot': {
        'border-width': '10px',
        'border-left-style': 'solid',
        'color': '#ffffff',
        'backgroundColor': '#333333',
        'padding' : '10px'
    }
}

colors = {
        'background': '#333333',
        'text': '#ffffff',
        'text2': '#706f6f'
}



app.layout = html.Div(style = {}, children =[
    html.Div(
       style = styles['header'], children = [
        html.Div(
            className='six columns',
            children = html.Div(style = styles['title'], children = 'Air Quality Madrid' )
        ),
            html.Div(
            className='six columns',
            children=html.Div(
                style = styles['logo'],
                children=[html.Img(src='./assets/logo-madrid.png')])
        )
    ]),
    html.Div(
        children = [
        html.Div(
            style = {'color': colors['text'], 'backgroundColor': colors['background'], 'padding' : '10px'},
            className='two columns',
            children = [
            html.H5("Compuesto (µg/m³)"),
            html.Div(
                style = {'color': colors['background']},
                children =
                dcc.Dropdown(
                    id='variable',
                    options=[{'label': i, "value": compuestos[i]} for i in compuestos],
                    value=8,
                )
            ),
            html.H5("Hora"),
            html.Div(
                style = {'color': colors['background']},
                children =
                dcc.Dropdown(
                    id='time',
                    options=[{'label': i, "value": horas[i]} for i in dict(itertools.islice(horas.items(), dt.datetime.now().hour))],
                    value=time_now)
            ),
            html.Div([
                html.H5('Actualización'),
                html.Div(id='live-update-text'),
                dcc.Interval(
                    id='interval-component',
                    interval=100000, # in milliseconds
                    #interval=3600000, # in milliseconds
                    n_intervals=0
                )
            ]),
            html.Br(),
            html.H6("Autores:", style={'color': colors['text2'], 'font-size': '1em'}),
            html.H6("Manuel Bajo y Kevin Craig", style={'color': colors['text2'], 'font-size': '1em'})


            ]),
        html.Div(
            className='five columns',
            style = styles['plot'],
            children = [
            html.H5("Mapa estaciones"),
            dcc.Graph(id='map', animate=True)
            ]
        ),
        html.Div(
            className='five columns',
            style = styles['plot'],
            children = [
            html.H5("Mapa interpolación"),
                html.Div(
                         children = dcc.Graph(id='cont'))
            ]
        )
    ])
])

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):

    global data
    data = import_data.generar_datos()
    style = {'padding': '5px', 'fontSize': '16px'}
    return[
        html.H6('Iteración: {0:.2f}'.format(n), style=style)
            ]


@app.callback(
    dash.dependencies.Output('cont', 'figure'),
    [dash.dependencies.Input('time', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('variable', 'value')])

def display_stores_over_time(time, n, variable):

    actualizar_datos(time, variable)

    xi, yi, zi = interpolation(x, y, z)

    return {
        'data': [
            {
                'x': xi,
                'y': yi,
                'z': zi,
                'name': 'Open Date',
                'type': 'contour',
                'opacity': 0.35,
                'line': {'width': 0},
                'contours': {'coloring': 'fill'},
                'connectgaps': True
            }
        ],
        'layout': {
            'margin': {'l': 40, 'r': 20, 't': 10, 'b': 30},
            'xaxis': dict(
                         autorange=True,
                         title='Longitud',
                         showgrid=False,
                         zeroline=False,
                         showline=False,
                     ),
            'yaxis': dict(
                            autorange=True,
                            title = 'Latitud',
                            showgrid=False,
                            tickangle=270,
                            zeroline=False,
                            showline=False,
                        ),
            'images': [dict(
                  source=encoded_image,
                  xref= "x",
                  yref= "y",
                  x= np.min(datos["lon"]) - 0.05*width,
                  y= np.max(datos["lat"]) + 0.05*height,
                  sizex= width + 0.1*width,
                  sizey= height + 0.1*height,
                  sizing= "stretch",
                  opacity= 1,
                  layer= "below")]
        }
    }


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('time', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('variable', 'value')])

def display_map(time, n, variable):

    actualizar_datos(time, variable)

    estacion = datos.iloc[np.where(datos.MAGNITUD == variable)[0], :]["ESTACIÓN"].values

    return {
        'data': [{
            'lat': y.flatten(),
            'lon': x.flatten(),
            'type': 'scattermapbox',
            'marker': {'size': 8, 'opacity': 0.8},
            'text': estacion + ': ' + [str(i) for i in z],
            'hoverinfo': "text",
            'selected': {
                'marker': {'color': '#85144b'}
            }
        }],
        'layout': {
            'mapbox': {
                'center': {
                    'lat': y_mean,
                    'lon': x_mean
                },
                'zoom': 10.5,
                'pitch': 0,
                'accesstoken': 'pk.eyJ1IjoibWJham9idWUiLCJhIjoiY2pyeTFuMWRrMHFwOTQ5b2E5b2E3Y3NleiJ9.0UXhwZBeHtsd7SPe_0E0QQ'
            },
            'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)



