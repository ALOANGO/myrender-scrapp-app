import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
from scraping_dataframe import fincaraiz







#COORDENADAS CALI Y JAMUNDI
cali=[[-76.59027692154969,3.535311581094419],[-76.48934003190125,3.3689308955117525]]
jamundi=[[-76.5766830444336,3.4943666458129883],[-76.502929,3.2008246]]
#DATAFRAME CASAS
dfcalihouse= fincaraiz("house",cali)
dfjamundihouse=fincaraiz("house",jamundi)
dataframehouses=pd.concat([dfcalihouse,dfjamundihouse])
#DATAFRAME APARTAMENTOS
dfcaliapartment= fincaraiz("apartment",cali)
dfjamundiapartment=fincaraiz("apartment",jamundi)
dataframeapartment=pd.concat([dfcaliapartment,dfjamundiapartment])
#CONCATENAR DATAFRAME CASAS Y APTOS
df= pd.concat([dataframehouses,dataframeapartment])

#1- inicializo la app


app= dash.Dash()
server = app.server

#2- creo componentes ( la tabla, boton upload, boton download)



generate_button = html.Button("Generar tabla", id="load-button")
download_button =html.Button("Download Excel", id="btn_xlsx")
tabla_container=html.Div(id="table-container")
#download_button = html.Button("Download Tabla", style={"marginTop": 20})

download_component = dcc.Download()



#3-Mete los componentes a la pagina (layout)

app.layout = html.Div(
    [
        html.H2('WEB SCRAPING VIVIENDAS EN VENTA DE CALI Y JAMUNDI', style={"marginBottom": 20}), 
         
        generate_button, 
        download_button,
        dcc.Download(id="download-dataframe-xlsx"),
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
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True)


def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")



if __name__ == '__main__':
 app.run_server(debug=False)