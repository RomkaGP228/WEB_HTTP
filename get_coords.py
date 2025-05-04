import requests
from config import API_KEY_GEOCODE, SERVER_GEOCODE

def get_coords(toponym_to_find):
    geocoder_params = {
        "apikey": API_KEY_GEOCODE,
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(SERVER_GEOCODE, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return list(map(str, toponym["Point"]["pos"].split(" ")))
