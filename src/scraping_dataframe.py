import requests
import pandas as pd
import json
from numpy import float64
import numpy as np


def fincaraiz(tipo , ciudad):

    url = 'https://api.fincaraiz.com.co/document/api/1.0/listing/search'
    headers={"User-Agent": "Mozilla/5.0", "referer": "https://fincaraiz.com.co/"}


    json_data = {
    'filter': {
    'offer': {
        'slug': [
            'sell',
            ],
        },
    'property_type': {
        'slug': [
            f'{tipo}',
            ],
        },
    'locations': {
        'location_point':ciudad,
    },

    },

    'fields': {
    'exclude': [],

    'include': [


                        'address',
                        'age.name',
                        'area',
                        'baths.name',
                        'client.client_type',
                        'client.company_name',
                        'client.first_name',
                        'client.last_name',
                        'dates.published',
                        'garages.name',
                        'locations.cities.name',
                        'locations.countries.name',
                        'locations.groups.subgroups.name',
                        'locations.groups.subgroups.slug',
                        'locations.location_point',
                        'locations.neighbourhoods.name',
                        'locations.neighbourhoods.slug',
                        'locations.states.name',
                        'media.floor_plans.count',
                        'price',
                        'products.configuration.tag_name',
                        'products.label',
                        'products.name',
                        'rooms.name',
                        'title',
                        'property_type.name',
                        'offer.name',
                        'fr_property_id',
                        'description',
                        'seo.description',
                        'floor.id',
                        'stratum.id',


                    #COORDENADAS PARA JAMUNDI
                    # [-76.5766830444336,3.4943666458129883],
                    # [-76.502929,3.2008246],

                    #COORDENADAS CALI
                    #[-76.59027692154969,3.535311581094419],
                    #[-76.48934003190125,3.3689308955117525],




    ],
    'limit': 100,
    'offset': 100, #set to 25 to get the second page, 50 for the 3rd page etc.
    'ordering': [],
    'platform': 40,
    'with_algorithm': False,
    },
    }




    response = requests.post(url, headers = headers, json=json_data)
    datap= json.loads(response.text)
    listadatos=datap["hits"]["hits"]



    area=[]
    cuartos=[]
    antiguedad=[]
    piso=[]
    titulo=[]
    oferta=[]
    garajes=[]
    tocadores=[]
    precio=[]
    companyname=[]
    nombrevendedor=[]
    apellidovendedor=[]
    tipocliente=[]
    tipopropiedad=[]
    barrio=[]
    ciudad=[]
    pais=[]
    depto=[]
    propid=[]
    zona=[]
    point=[]
    estrato=[]
    direccion=[]
    descripcion=[]
    fecha=[]



    for e in listadatos:

        try:

            estrato.append(e["_source"]["listing"]["stratum"]["id"])
            area.append(e["_source"]["listing"]["area"])
            cuartos.append(e["_source"]["listing"]["rooms"]["name"])
            antiguedad.append(e["_source"]["listing"]["age"]["name"])
            piso.append(e["_source"]["listing"]["floor"]["id"])
            titulo.append(e["_source"]["listing"]["title"])
            oferta.append(e["_source"]["listing"]["offer"][0]["name"])
            garajes.append(e["_source"]["listing"]["garages"]["name"])
            tocadores.append(e["_source"]["listing"]["baths"]["name"])
            precio.append(e["_source"]["listing"]["price"])
            companyname.append(e["_source"]["listing"]["client"]["company_name"])
            nombrevendedor.append(e["_source"]["listing"]["client"]["first_name"])
            apellidovendedor.append(e["_source"]["listing"]["client"]["last_name"])
            tipocliente.append(e["_source"]["listing"]["client"]["client_type"])
            tipopropiedad.append(e["_source"]["listing"]["property_type"][0]["name"])
            ciudad.append(e["_source"]["listing"]["locations"]["cities"][0]["name"])
            pais.append(e["_source"]["listing"]["locations"]["countries"][0]["name"])
            depto.append(e["_source"]["listing"]["locations"]["states"][0]["name"])
            propid.append(e["_source"]["listing"]["fr_property_id"])
            point.append(e["_source"]["listing"]["locations"]["location_point"])
            direccion.append(e["_source"]["listing"]["address"])
            descripcion.append(e["_source"]["listing"]["description"])
            fecha.append(e["_source"]["listing"]["dates"]["published"])
            zona.append(e["_source"]["listing"]["locations"]["groups"][0]["subgroups"]["name"])

        except:

            zona.append("n/a")



    for e in listadatos:
        try:
          barrio.append(e["_source"]["listing"]["locations"]["neighbourhoods"][0]["name"])
        except:


          barrio.append("n/a")


    df={  "aream2":area,
            "cuartos":cuartos,
            "antiguedad":antiguedad,
            "piso":piso,
            "enunciado":titulo,
            "oferta":oferta,
            "garajes":garajes,
            "toilets":tocadores,
            "estrato":estrato,
            "precio":precio,
            "companyname":companyname,
            "nombrevendedor":nombrevendedor,
            "apellidovendedor":apellidovendedor,
            "tipocliente":tipocliente,
            "tipopropiedad":tipopropiedad,
            "barrio":barrio,
            "ciudad":ciudad,
            "pais":pais,
            "depto":depto,
            "direccion":direccion,
            "zona":zona, "idpropiedad":propid,
            "punto":point,
            "descripcion":descripcion,
            "fecha":fecha,}






    consolidado = pd.DataFrame(data=df)

    #ARREGLAR COLUMNAS

    consolidado["punto"]= consolidado["punto"].replace('POINT','', regex=True)
    consolidado=consolidado.replace('"','', regex=True)
    consolidado["punto"]= consolidado["punto"].str.strip("( )")
    consolidado["zona"]= consolidado["zona"].str.strip("Zona ")
    consolidado[["longitud","latitud"]]= consolidado["punto"].str.split(" ", expand=True)
    consolidado[["longitud","latitud"]]=round((consolidado[["longitud","latitud"]].astype(float64)),2)
    consolidado["precio"]=consolidado["precio"].astype(float64)
    consolidado["aream2"]=consolidado["aream2"].astype(float64)
    consolidado["idpropiedad"]=consolidado["idpropiedad"].astype(str)
    consolidado["direccion"]= consolidado["direccion"].str.strip("{ }")
    consolidado["direccion"]= consolidado["direccion"].str.strip("address:")
    consolidado["direccion"]= consolidado["direccion"].str.strip(" attribution: legacy")
    consolidado["direccion"]= consolidado["direccion"].str.replace(",",".")
    consolidado["fecha"]= consolidado["fecha"].str.replace(r'T.*','',regex=True)
    consolidado["zona"]= consolidado["zona"].str.replace("/"," ")


    #CREAR COLUMNA PAGINA WEB
    consolidado["pagina_web"]="https://fincaraiz.com.co/inmueble/"+consolidado.enunciado+"/"+consolidado.barrio+"/"+consolidado.ciudad+"/"+consolidado.idpropiedad

    return consolidado