from import_api import get_api_key
import gmaps
import googlemaps
from datetime import datetime

api_key = get_api_key()
gmaps.configure(api_key)

def get_time(origin = (50.04992178714987, 19.925072145463666), dest = "Reymonta 44, Polska, Kraków")
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    direction_result = gmaps.directions(origin, dest, mode="driving", avoid="ferries", departure_time=now)
    print(direction_result[0]['legs'][0]['duration']['text'])
    return direction_result[0]['legs'][0]['duration']['value']