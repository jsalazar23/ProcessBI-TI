# -*- coding: utf-8 -*-
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Datos de ejemplo
nombres = ['Módulo BEAS', 'Módulo WMS', 'Módulo de mantenimiento', 'Módulo CRM', 'Módulo Recursos Humanos', 'Software LIMS', 'Seguridad informática', 'Infraestructura en nube (AZURE)', 'SAP México', 'Control de roles y perfiles de los sistemas de información de la compañía', 'Control de roles y perfiles y seguridad del sistema de control y validación IMOMENTRICS', 'PLASMANET', 'Metodología SCRUM para proyectos']
porcentajes = [43, 47, 85, 42, 36, 93, 100, 100, 15, 100, 100, 20, 100]

# Datos de ejemplo para parametrización
nombres_parametrizacion = ['Módulo de compras', 'Módulo de logística', 'Módulo de tesorería']
porcentajes_parametrizacion = [90, 92, 50]

# Datos de ejemplo para "Otras actividades"
nombres_otras = [
    'PLATAFORMA DE MESA DE AYUDA WEB 100%',
    'REPOSITORIO WEB SISTEMA INTEGRADO DE GESTIÓN(SHAREPOINT) 100%',
    'REPOSITORIO DOCUMENTAL DE LA DIRECCIÓN FINANCIERA Y CONTABLE 100%'
]

# Función para crear gráfica de barras horizontal
def create_bar_chart(nombres, porcentajes, title):
    data = go.Bar(
        x=porcentajes,
        y=nombres,
        orientation='h',
        marker=dict(color=['#FF5733' if p < 40 else '#FFC300' if 40 <= p <= 99 else '#336600' for p in porcentajes])
    )
    layout = dict(title=title, xaxis_title='Avance (%)', yaxis_title='Objetivos',
                  font=dict(family='Arial, sans-serif', color='black'))
    return go.Figure(data=[data], layout=layout)

# Función para crear gráfica de pastel
def create_pie_chart(labels, values, title):
    data = go.Pie(labels=labels, values=values, textinfo='label+percent', hole=0.3,
                  marker=dict(colors=['#336600', '#FFC300']))
    layout = dict(title=title, font=dict(family='Arial, sans-serif', color='black'))
    return go.Figure(data=[data], layout=layout)

# Crear la aplicación Dash
app = dash.Dash(__name__)
server=app.server

# Diseño del dashboard
app.layout = html.Div([
    html.Div([
        html.H1('Proyectos TI/BI', style={'color': 'white', 'text-align': 'center', 'font-family': 'Arial, sans-serif'}),
    ], style={'background': 'linear-gradient(to right, #001f3f, #0074CC)', 'padding': '20px', 'text-align': 'center'}),

    dcc.Tabs(id='tabs', value='implementacion', children=[
        dcc.Tab(label='Implementación', value='implementacion'),
        dcc.Tab(label='Parametrización', value='parametrizacion')
    ]),

    dcc.Graph(id='grafica', config={'displayModeBar': False}),

    html.Div(id='otras-actividades', children=[
        html.H3('Otras actividades', style={'color': '#333'}),
        html.Div([
            html.Div(nombre, style={'background-color': '#001f3f', 'padding': '10px', 'border-radius': '10px', 'margin': '5px', 'color': 'white', 'font-family': 'Arial, sans-serif'})
            for nombre in nombres_otras
        ])
    ]),

    dcc.Graph(id='torta', config={'displayModeBar': False}),

    html.A('Abrir en pantalla completa', href='javascript:void(0);', id='fullscreen-button', target='_blank', style={'color': 'white', 'background-color': '#333', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'margin-top': '20px', 'display': 'block', 'font-family': 'Arial, sans-serif'})
])

# Callback para abrir en pantalla completa
@app.callback(
    Output('fullscreen-button', 'href'),
    Input('fullscreen-button', 'n_clicks')
)
def open_in_fullscreen(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return 'URL_DE_LA_PAGINA_DE_VISUALIZACION_COMPLETA'

# Callback para actualizar la gráfica según la pestaña seleccionada
@app.callback(
    Output('grafica', 'figure'),
    Input('tabs', 'value')
)
def update_graph(tab_value):
    if tab_value == 'implementacion':
        # Gráfica de implementación
        return create_bar_chart(nombres, porcentajes, 'Cumplimiento de Implementación')
    elif tab_value == 'parametrizacion':
        # Gráfica de parametrización
        return create_bar_chart(nombres_parametrizacion, porcentajes_parametrizacion, 'Cumplimiento de Parametrización')

# Datos para el gráfico de torta
labels_torta = ['Completadas', 'En Marcha']
values_torta = [8, 11]

# Callback para el gráfico de torta
@app.callback(
    Output('torta', 'figure'),
    Input('tabs', 'value')
)
def update_pie_chart(tab_value):
    if tab_value == 'implementacion':
        # Gráfico de torta para implementación
        return create_pie_chart(labels_torta, values_torta, 'Resumen de Actividades')

if __name__ == '__main__':
    app.run_server(debug=True)
