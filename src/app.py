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

app = Dash(__name__)
server = app.server

data_historica=pd.read_csv("data_contatenada.csv", sep=',')



dtable = dash_table.DataTable(id='datascraping',
        columns=[{"name": i, "id": i} for i in (data_historica.columns)],
        data=data_historica.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        filter_action="native",
        style_cell={"textAlign":"left", 
                    'whiteSpace': 'normal',
                    'height': 'auto', 
                    'lineHeight': '15px',
                    #'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        },
        style_cell_conditional=[{'if':{'column_id':'descripcion'},'width':'10%'}],
        page_size=10)                                                                                    


download_button =html.Button("Download Excel", style={"marginTop": 20})
download_component = dcc.Download()

app.layout = html.Div(
    [
        html.H2('MURILLO PROPIEDADES - VENTA DE VIVIENDAS EN ANTIOQUIA', style={"text-align": "center"}),
        download_component,
        download_button,
        dtable,
    ]
)


@app.callback(
    Output(download_component, "data"),
    Input(download_button, "n_clicks"),
    State(dtable, "derived_virtual_data"),
    prevent_initial_call=True,
)
def download_data(n_clicks, data):
    excel_data = data_historica.to_excel("houses_antioquia.xlsx", index=False)
    return dcc.send_file("houses_antioquia.xlsx")



if __name__ == "__main__":
    app.run_server(debug=False)