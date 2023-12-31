# -*- coding: utf-8 -*-
"""lonja2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FxlpaFx3c6YH2orb20CqfRGoj_dvHaPQ
"""

import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import lxml

def lonja():

        aream2=[]
        cuartos=[]
        antiguedad=[]
        piso=[]
        garajes=[]
        toilets=[]
        estrato=[]
        ciudad=[]
        admon=[]
        zona=[]
        barrio=[]
        tipopropiedad=[]
        idpropiedad=[]
        precio=[]
        enunciado=[]
        descripcion=[]
        nombrevendedor=[]
        punto=[]
        links=[]
        oferta=[]
        companyname=[]
        apellidovendedor=[]
        tipocliente=[]
        depto=[]
        direccion=[]
        fecha=[]
        fuente=[]
        longitud=[]
        latitud=[]


        for n in range(1,13):

          url=(f"https://lalonjapropiedadraiz.com/inmuebles/Venta/clases_Finca_Hotel_Local_Oficina_Terreno_Edificio_Apartamento_Casa/precio_0_999999999999/{n}")
          r=requests.get(url)

          if r.status_code==200:
              soup=BeautifulSoup(r.text, 'lxml')

              anuncios=soup.find_all("div", class_="listing-item")
              ul=soup.find_all("ul", class_="listing-details")



              for h in ul:
                try:
                    li=h.find_all("li")

                    aream2.append(li[0].text.strip().replace(" m2", "").replace(",", ""))
                    garajes.append(li[3].text.strip().replace(" Garaje", "").replace("Un", "1").replace("s", ""))
                except:
                    garajes.append("null")

                try:
                    cuartos.append(li[1].text.strip().replace(" Alcobas", ""))
                except:
                    cuartos.append("null")

                try:
                    toilets.append(li[2].text.strip().replace(" Baño", "").replace("Un", "1").replace("s", ""))
                except:
                    toilets.append("null")







              for e in anuncios:

                    precio.append (e.find("span", class_="listing-price").text.strip().replace(",","").replace("$",""))
                    ciudad.append (e.find('i', class_='fa-map-marker').next_sibling.text.strip().split(",")[0])
                    barrio.append (e.find('i', class_='fa-map-marker').next_sibling.text.strip().split(",")[1])
                    links.append("https://lalonjapropiedadraiz.com"+(e.find('a').get('href')))
                    tipopropiedad.append (e.select_one('#titulo32').text.strip().split("-")[0])
                    idpropiedad.append(e.select_one('#titulo32').text.strip().split("-")[1].replace(" Código: ",""))
                    enunciado.append((e.select_one('#titulo32').text.strip().split("-")[0])+("disponible para la venta"))
                    antiguedad.append("null")
                    piso.append("null")
                    estrato.append("null")
                    admon.append("null")
                    zona.append("null")
                    nombrevendedor.append("null")
                    punto.append("null")
                    oferta.append("VENTA")
                    companyname.append("null")
                    apellidovendedor.append("null")
                    tipocliente.append("null")
                    depto.append("Antioquia")
                    direccion.append(e.find('i', class_='fa-map-marker').next_sibling.text.strip().split(",")[1])
                    fecha.append(date.today())
                    fuente.append("Lonja")
                    longitud.append("null")
                    latitud.append("null")
                    cada_anuncio=requests.get("https://lalonjapropiedadraiz.com"+(e.find('a').get('href')))
                    soup_individual=BeautifulSoup(cada_anuncio.text, 'lxml')
                    descripcion.append(soup_individual.find('p', class_='resumen').text.strip())





        df={  "aream2":aream2,
        "cuartos":cuartos,
        "antiguedad":antiguedad,
        "piso":piso,
        "enunciado":enunciado,
        "oferta":oferta,
        "garajes":garajes,
        "toilets":toilets,
        "estrato":estrato,
        "precio":precio,
        "companyname":companyname,
        "nombrevendedor":nombrevendedor,
        "apellidovendedor":apellidovendedor,
        "tipocliente":tipocliente,
        "tipopropiedad":tipopropiedad,
        "barrio":barrio,
        "ciudad":ciudad,
        "admon":admon,
        "depto":depto,
        "direccion":direccion,
        "zona":zona, "idpropiedad":idpropiedad,
        "punto":punto,
        "descripcion":descripcion,
        "fecha":fecha,
        "fuente":fuente,
        "links":links,
        "longitud":longitud,
        "latitud":latitud}

        consolidado = pd.DataFrame(data=df)

        consolidado["precio"]=pd.to_numeric(consolidado["precio"], errors='ignore')
        
        def format_currency(value):
            try:
                return '${:,.0f}'.format(float(value))
            except (ValueError, TypeError):
                return value  # Devuelve el valor original si no se puede convertir a un número
        
        consolidado["precio"]=consolidado["precio"].apply(format_currency)
        
        

        return consolidado