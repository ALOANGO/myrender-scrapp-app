import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from fincaprueba import fincaraiz
from metrocuadrado import metrocuadrado
from realityserver import realityserver
from lonja import lonja
from datetime import date
from bs4 import BeautifulSoup
import dash_bootstrap_components as dbc
import re


#EXTRAER DATA WEB SCRAPP
df1=fincaraiz()
df2=metrocuadrado()
df3=realityserver()
df4=lonja()
data_historica=pd.read_csv("data_contatenada.csv", sep=",")


#CONCATENAR DATA
df_total=pd.concat([data_historica,df1,df2,df3, df4])
df_total.drop_duplicates(['idpropiedad'], inplace=True)
df_total.reset_index(drop=True, inplace=True)

df_total.to_csv("data_contatenada.csv", index=False)
#1- inicializo la app


app= dash.Dash()
server = app.server

#2- creo componentes ( la tabla, boton upload, boton download)



generate_button = html.Button("Generar tabla", id="load-button")
#actualiza_button=html.Button("Generar tabla", id="actualiza-button")
download_button =html.Button("Download CSV", style={"marginTop": 20})
tabla_container=html.Div(id="table-container")
download_component = dcc.Download()
# #filtro1=dcc.Dropdown(id='mifiltro',
#                      options={'value':'fuente'},
#                      placeholder='Escoge la fuente' ,
#                      multi=True, 
#                      style={'width': "40%"}   )                                                                                         



#3-Mete los componentes a la pagina (layout)

app.layout = html.Div(
    [
        html.H1('MURILLO PROPIEDADES - VENTA DE VIVIENDAS EN ANTIOQUIA', style={"text-align": "center"}), 
        html.Div('''Fincaraiz - Metrocuadrado - Lonja - Realityserver'''),
        html.Div(f'''Tamaño de la tabla: {df_total.shape}'''),
         
        generate_button, 
        download_component,
        download_button,
        tabla_container,
        #actualiza_button
        #filtro1
        
        
    ]
)


#___________________________________________________________________________________________________________________
#4-callbacks (juntar componentes con los datos)

@app.callback(
    Output("table-container", "children"),
    Input("load-button", "n_clicks"))

def generate_table(n_clicks):

    if n_clicks is None:
        return dash.no_update  # No actualiza la salida si aún no se ha hecho click
    
    dtable = dash_table.DataTable(id='datascraping',
        columns=[{"name": i, "id": i} for i in (df_total.columns)],
        data=df_total.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        filter_action="native",
        style_cell={"textAlign":"left", 
                    'whiteSpace': 'normal',
                    'height': 'auto', 
                    'lineHeight': '15px',
                    #'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        },
        style_cell_conditional=[{'if':{'column_id':'descripcion'},'width':'10%'}],
        page_size=10)
    return dtable




    #return dtable, download_link

@app.callback(
Output(download_component, "data"),
Input(download_button, "n_clicks"),

prevent_initial_call=True)


def download_data(n_clicks):
    if n_clicks is None:
     return None
    
    return dcc.send_data_frame(data_historica.to_csv, "Scrap_Antioquia.csv", index=False)


if __name__ == '__main__':
 app.run_server(debug=False)