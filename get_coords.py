import requests


def get_coords(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    API_KEY_GEOCODE = "8013b162-6b42-4997-9691-77b7074026e0"
    geocoder_params = {
        "apikey": API_KEY_GEOCODE,
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return list(map(str, toponym["Point"]["pos"].split(" ")))
