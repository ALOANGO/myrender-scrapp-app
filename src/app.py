import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
from scraping_dataframe import fincaraiz
import openpyxl








#COORDENADAS CALI Y JAMUNDI
antioquia=[[-75.7751988,7.0938077],[-75.3140647788699,5.6973074]]

#DATAFRAME CASAS
dfantioquiahouse= fincaraiz("house",antioquia)


#DATAFRAME APARTAMENTOS
dfantioquiapartment= fincaraiz("apartment",antioquia)


#CONCATENAR DATAFRAME CASAS Y APTOS
df= pd.concat([dfantioquiahouse,dfantioquiapartment])
df.drop_duplicates(['idpropiedad'], inplace=True)
df.reset_index(drop=True, inplace=True)
#1- inicializo la app


app= dash.Dash()
server = app.server

#2- creo componentes ( la tabla, boton upload, boton download)



generate_button = html.Button("Generar tabla", id="load-button")
download_button =html.Button("Download Excel", style={"marginTop": 20})
tabla_container=html.Div(id="table-container")
#download_button = html.Button("Download Tabla", style={"marginTop": 20})

download_component = dcc.Download()



#3-Mete los componentes a la pagina (layout)

app.layout = html.Div(
    [
        html.H2('WEB SCRAPING VIVIENDAS EN VENTA EN ANTIOQUIA', style={"marginBottom": 20}), 
         
        generate_button, 
        download_component,
        download_button,
        tabla_container
        
        
    ]
)

#4-callbacks (juntar componentes con los datos)

@app.callback(
    Output("table-container", "children"),
    Input("load-button", "n_clicks"))

def generate_table(n_clicks):

    if n_clicks is None:
        return dash.no_update  # No actualiza la salida si aún no se ha hecho click
    
    dtable = dash_table.DataTable(id='datascraping',
        columns=[{"name": i, "id": i} for i in sorted(df.columns)],
        data=df.to_dict('records'),
        sort_action="native",
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
   
   excel_data = df.to_excel("houses_antioquia.xlsx", index=False)
   return dcc.send_file("houses_antioquia.xlsx")



if __name__ == '__main__':
 app.run_server(debug=False)