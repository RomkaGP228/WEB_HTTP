import requests
from get_coords import get_coords
import sys


def main():
    coords = get_coords(' '.join(sys.argv[1:]))
    geocoder_server = "http://geocode-maps.yandex.ru/1.x/"
    params = {"geocode": ','.join(list(map(str, coords))),
              "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
              "kind": "district",
              "format": "json",
              "results": 1}
    data = requests.get(geocoder_server, params).json()
    print(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name'])


if __name__ == '__main__':
    main()
