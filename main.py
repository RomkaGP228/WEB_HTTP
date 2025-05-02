import requests
from get_coords import get_coords
import sys
from config import API_KEY_GEOCODE, SERVER_GEOCODE


def main():
    coords = get_coords(' '.join(sys.argv[1:]))
    params = {"geocode": ','.join(list(map(str, coords))),
              "apikey": API_KEY_GEOCODE,
              "kind": "district",
              "format": "json",
              "results": 1}
    # kind - это тип топонима, который мы ищем. В данном мы ищем район, но также можно искать дом, улицу, решион и тд.
    data = requests.get(SERVER_GEOCODE, params).json()
    print(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name'])


if __name__ == '__main__':
    main()
