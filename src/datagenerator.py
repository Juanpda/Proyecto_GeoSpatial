import requests
from requests.exceptions import HTTPError
import time
import json
import os

#Transformamos una direccion en coordenadas
def geocode(direction):
    try:
        response = requests.get(f"https://geocode.xyz/{direction}?json=1")
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
        return -1
    except Exception as err:
        print(f'Other error occurred: {err}')  
        return -1
    else:
        data = response.json()
        if("error" not in data.keys()):
            return data
        else:
            return -1

#Obtenemos las coordenadas de una lista de direcciones 

"""
Obtenemos una lista de las coordendas donde se encuentra el establecimiento de los parametros que le pasamos.
El center hace refenrencia a las coordenadas de las direcciones obtenidas con geocode.
El extra se usa para añadir más parametros sobre la query a la API de google maps
"""

def get_places_by_location_type_and_radius(center,g_type,radius,extra):
    token = os.getenv("tok")
    try:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={center}&radius={radius}&type={g_type}{extra}&key={token}"
        response = requests.get(url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
        return -1
    except Exception as err:
        print(f'Other error occurred: {err}')  
        return -1
    else:
        data = response.json()
        result = []
        if(data["status"] == "OK"):
            result = data["results"] 
        return result

"""
    Buscamos las coordenadas de los establecimientos que vamos a usar a la hora de decidir donde situar la empresa.
"""
def get_google_nearby_data(coords):
    radius = { #Distancia medida en metross
        "train_station":"10000",
        "school":"5000",
        "night_club":"2000",
        "airport":"15000",
        "cafe":"1000"
    }
    ponderations = {
        "train_station":10,
        "school":50,
        "night_club":25,
        "airport":10,
        "cafe":5
    }
    total_value = 0
    location_info = {
        "location":coords
    }
    for key in ["train_station","school", "night_club", "airport","cafe"]:
        extra = "" if key != "cafe" else "&keyword=starbucks"
        data = get_places_by_location_type_and_radius(coords,key,radius[key],extra)
        if(data != -1):
            place_value = len(data) * ponderations[key]
            total_value += place_value
            location_info[key] = {
                "locations":data,
                "value":place_value
            }
    location_info["total_value"] = total_value
    return location_info