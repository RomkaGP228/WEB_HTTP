import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image
from get_spn import get_spn

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print("Произошла ошибка! Выход из программы...", response)
    exit(0)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coordinates = toponym["Point"]["pos"]
toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
delta_longitude, delta_latitude = get_spn(toponym)
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_latitude]),
    "spn": ",".join([delta_longitude, delta_latitude]),
    "apikey": apikey,
    "pt": ",".join([toponym_longitude, toponym_latitude, "comma"])
}


def main():
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.show()


if __name__ == '__main__':
    main()
