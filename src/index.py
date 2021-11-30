import src.datagenerator as dg
import time
import json

def write_file(data, name):
    f = open(f"./{name}.result.json", "w")
    f.write(json.dumps(data, indent=2))
    f.close()
def display_results(name):
    score = json.loads(open(f"./{name}.result.json").read())
    print(f"City: {name}, Score:{score['total_value']}, location: {score['location']}, Schools: {len(score['school']['locations'])}, Starbucks: {len(score['cafe']['locations'])}, Night Clubs: {len(score['night_club']['locations'])}, Train Stations: {len(score['train_station']['locations'])} Airports: {len(score['airport']['locations'])}")

def main(address):
        address_info = dg.geocode(address) # Obtenemos las coordenadas de la direccion
        if(address_info != -1):
            coords = f"{address_info['latt']},{address_info['longt']}"
            name = address_info["standard"]["city"]
            score = dg.get_google_nearby_data(coords) # Buscamos cuantos establecimientos tiene cerca las coordenadas
            write_file(score, name) #Guardamos los datos en un json
            display_results(name)
        else:
            print("Geocode fails with: " + address)


