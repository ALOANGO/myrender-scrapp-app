# -*- coding: utf-8 -*-
"""metrocuadrado.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1joWjZwRMSxZ1d9ejte90oC7wypwMm7oS
"""

import requests
import pandas as pd
from datetime import date

def metrocuadrado ():

              def metrocuadrado_scrap(ciudad, tipo_p):

                        # URL de la solicitud
                        url = f"https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList=venta&city={ciudad}&realEstateTypeList={tipo_p}&from=0&size=50"
                        headers={'X-Api-Key': 'P1MfFHfQMOtL16Zpg36NcntJYCLFm8FqFfudnavl'}
                        r=requests.get(url, headers=headers)


                        datacruda=r.json()["results"]

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


                        for e in datacruda:
                          try:
                              aream2.append(e.get('marea',None))
                              cuartos.append(e['mnrocuartos'])
                              enunciado.append(e['title'])
                              oferta.append(e['mtiponegocio'])
                              garajes.append(e['mnrogarajes'])
                              toilets.append(e['mnrobanos'])
                              precio.append(e['mvalorventa'])
                              admon.append(e.get('data', {}).get('mvaloradministracion', None))
                              tipopropiedad.append(e['mtipoinmueble']['nombre'])
                              nombrevendedor.append(e['mnombreconstructor'])
                              companyname.append(e['mnombreproyecto'])
                              barrio.append(e['mbarrio'])
                              direccion.append(e['mnombrecomunbarrio'])
                              ciudad.append(e['mciudad']['nombre'])
                              idpropiedad.append(e['midinmueble'])
                              apellidovendedor.append(e['contactPhone'])
                              antiguedad.append(e['mestadoinmueble'])
                              descripcion.append(e['data']['murldetalle'])
                              links.append(e['data']['murldetalle'])
                              zona.append(e['mzona']['nombre'])

                              depto.append("Antioquia")
                              piso.append(0)
                              estrato.append(0)
                              tipocliente.append("PRIVATE")
                              punto.append("null")
                              longitud.append("null")
                              latitud.append("null")
                              fecha.append(date.today())
                              fuente.append("Metrocuadrado")

                          except:
                              zona.append("null")
                              depto.append("Antioquia")
                              piso.append(0)
                              estrato.append(0)
                              tipocliente.append("PRIVATE")
                              punto.append("null")
                              longitud.append("null")
                              latitud.append("null")
                              fecha.append(date.today())
                              fuente.append("Metrocuadrado")





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
                              "zona":zona,
                              "idpropiedad":idpropiedad,
                              "punto":punto,
                              "longitud":longitud,
                              "latitud":latitud,
                              "descripcion":descripcion,
                              "fecha":fecha,
                              "links":links,
                              "fuente":fuente}

                        dfconsolidado=pd.DataFrame(df)
                        dfconsolidado["precio"]=pd.to_numeric(dfconsolidado["precio"], errors='ignore')
                        

                        #Organizar columna de link
                        dfconsolidado["links"]="https://www.metrocuadrado.com"+dfconsolidado.descripcion

                        return dfconsolidado

              cities=["Medellin",	"Bello","Itagui",	"Envigado",	"Sabaneta",	"Estrella",	"Caldas",	"Copacabana",	"Girardota",	"Barbosa",	"Rionegro",	"Viboral",	"Retiro",	"Ceja",	"Marinilla",	"Penol",	"Guatape",	"Vicente",	"union",	"Guarne",	"Cocorna",	"Apartado",	"Turbo",	"Carepa",	"Chigorodo",	"Necocli",	"Arboletes",]
              tipo_prop=['apartamento','casa','oficina','finca','bodega','local%20comercial','lote%20o%20casalote']
              dfs=[]

              for c in cities :
                try:
                 for  s in tipo_prop:
                   dfs.append(metrocuadrado_scrap(c,s))
                except:
                  continue


             #Concatenar tablas extraidas
              dfdefinit=pd.concat(dfs, ignore_index=True)


              #eliminar duplicados de columna propid
              dfdefinit.drop_duplicates(['idpropiedad'], inplace=True)
              dfdefinit.reset_index(drop=True, inplace=True)

              def format_currency(value):
                try:
                    return '${:,.0f}'.format(float(value))
                except (ValueError, TypeError):
                    return value  # Devuelve el valor original si no se puede convertir a un número
        
              dfdefinit["precio"]=dfdefinit["precio"].apply(format_currency)
              dfdefinit["tipopropiedad"]=dfdefinit["tipopropiedad"].str.strip()

              return dfdefinit