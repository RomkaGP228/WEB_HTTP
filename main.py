import sys
from io import BytesIO
from distance import lonlat_distance
from get_coords import get_coords
import requests
from PIL import Image
from business import find_business


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    toponym_coordinates = get_coords(toponym_to_find)
    toponym_longitude, toponym_latitude = toponym_coordinates

    organization = find_business(','.join([toponym_longitude, toponym_latitude]), 'Круглосуточная Аптека')
    organization_coordinates = organization['geometry']['coordinates']
    organization_longitude, organization_latitude = organization_coordinates
    organization_metadata = organization['properties']['CompanyMetaData']
    print('Адрес:', organization_metadata['address'])
    print('Название:', organization_metadata['name'])
    print('Время работы:', organization_metadata['Hours']['text'])
    print('Прямое расстояние по карте:', str(int(lonlat_distance(list(
        map(float, toponym_coordinates)), list(map(float, organization_coordinates))))) + "м")

    map_params = {
        "l": "map",
        "pt": f'{toponym_longitude},{toponym_latitude},comma~{organization_longitude},{organization_latitude},pm2rdl'
    }

    SERVER_ADDRESS = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(SERVER_ADDRESS, params=map_params)
    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    main()
