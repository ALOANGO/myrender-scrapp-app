import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from fincaprueba import fincaraiz
from metrocuadrado import metrocuadrado
from realityserver import realityserver
from lonja import lonja
import openpyxl
from datetime import date
from bs4 import BeautifulSoup
import dash_bootstrap_components as dbc
import re
import os

# Cambia al directorio donde se encuentra el script
#os.chdir(os.path.dirname(os.path.abspath(__file__)))




data_historica=pd.read_csv("data_contatenada.csv", sep=',')




#1- inicializo la app
app= dash.Dash()
server = app.server


# #2- creo componentes ( la tabla, boton upload, boton download)


actualiza_button=html.Button("Actualizar tabla", id="actualiza-button",  style={"marginTop": 20})
download_button =html.Button("Download Excel", style={"marginTop": 20})
tabla_container=html.Div(id="table-container")
download_component = dcc.Download()
# filtro1=dcc.Dropdown(id='mifiltro',
#                      options={'value':'fuente'},
#                      placeholder='Escoge la fuente' ,
#                      multi=True, 
#                      style={'width': "40%"}   )    
cantidad= dcc.Markdown(id="cantidad-markdown", style={"text-align": "center"})

dtable = dash_table.DataTable(id='datascraping',
        columns=[{"name": i, "id": i} for i in (data_historica.columns)],
        data=data_historica.to_dict('records'),
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




# #3-Mete los componentes a la pagina (layout)

app.layout =dbc.Container([ 
    
        dcc.Markdown('# MURILLO PROPIEDADES - VENTA DE VIVIENDAS EN ANTIOQUIA', style={"text-align": "center"}), 
        cantidad,
         
        dbc.Label("Numero de filas"),
        row_drop := dcc.Dropdown(value=10, clearable=False, style={'width':'35%'},
                             options=[10, 25, 50, 100]),

        download_component,
        download_button,
        actualiza_button, 
                           
                       

        dbc.Row([
            dbc.Col([
                tipopropiedad_drop := dcc.Dropdown([x for x in sorted(data_historica.tipopropiedad.unique())])
            ], style={'width': "40%"}),

            dbc.Col([
            fuente_drop := dcc.Dropdown([x for x in sorted(data_historica.fuente.unique())], multi=True)
            ], style={'width': "40%"}),

            ],justify="between", className='mt-3 mb-4') ,

            dtable,
            tabla_container  
            
            ])


# #___________________________________________________________________________________________________________________
# #4-callbacks (juntar componentes con los datos)

@app.callback(
    Output(dtable, "data"),
    Output(dtable, 'page_size'),
    Output("cantidad-markdown", 'children'),

    Input(tipopropiedad_drop, 'value'),
    Input(fuente_drop, 'value'),
    Input(row_drop, 'value')
)

def update_dropdown_options(tipop_v, fuent_v, row_v):
    copia_data= data_historica.copy()

    if tipop_v:
        copia_data = copia_data[copia_data.tipopropiedad==tipop_v]
    if fuent_v:
        copia_data = copia_data[copia_data.fuente.isin(fuent_v)]

    cantidad_text= f'''REGISTROS: {copia_data.shape}'''

    return copia_data.to_dict('records'), row_v, cantidad_text






@app.callback(
    Output('datascraping', "children"),
    Input("actualiza-button", "n_clicks"))

def actualiza_table(n_clicks):

    if n_clicks is None:
        return dash.no_update  # No actualiza la salida si aún no se ha hecho click
    
    #EXTRAER DATA WEB SCRAPP
    df1=fincaraiz()
    df2=metrocuadrado()
    df3=realityserver()
    df4=lonja()
    


    #CONCATENAR DATA
    df_total=pd.concat([data_historica,df1,df2,df3, df4])
    df_total.drop_duplicates(['idpropiedad'], inplace=True)
    df_total.reset_index(drop=True, inplace=True)

    def format_currency(value):
        try:
            return '${:,.0f}'.format(float(value))
        except (ValueError, TypeError):
            return value  # Devuelve el valor original si no se puede convertir a un número
        
    df_total["precio"]=df_total["precio"].apply(format_currency)
    df_total["tipopropiedad"]=df_total["tipopropiedad"].str.strip()

    df_total.to_csv("data_contatenada.csv", index=False)
    

    return df_total.to_dict('records')




    #return dtable, download_link

@app.callback(
    Output(download_component, "data"),
    Input(download_button, "n_clicks"),
   
    prevent_initial_call=True)


def download_data(n_clicks):
   if n_clicks is None:
     return None 
   
   excel_data = data_historica.to_excel("houses_antioquia.xlsx", index=False)
   return dcc.send_file("houses_antioquia.xlsx")



if __name__ == '__main__':
 app.run_server(debug=False)