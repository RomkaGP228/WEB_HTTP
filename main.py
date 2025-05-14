import sys
from io import BytesIO
import requests
from PIL import Image
from config import SERVER_GEOCODE, API_KEY_GEOCODE, SERVER_ADDRESS
from business import find_business


def is_fullday(availabilities):
    for entry in availabilities:
        if "TwentyFourHours" in entry and entry['TwentyFourHours'] is True:
            return True
    return False


def generate_point(str_coords, color):
    return f'{str_coords},pm2{color}l'


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_params = {
        "apikey": API_KEY_GEOCODE,
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(SERVER_GEOCODE, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coords = toponym["Point"]["pos"].split(" ")
    toponym_longitude, toponym_lattitude = toponym_coords

    data = find_business(','.join([toponym_longitude, toponym_lattitude]), 10, 'аптека')
    round = []
    nonround = []
    unknown = []

    for organization in data["features"]:
        organization_coordinates = organization['geometry']['coordinates']
        organization_metadata = organization['properties']['CompanyMetaData']
        isround = False
        isknown = False
        if 'Hours' in organization_metadata and 'Availabilities' in organization_metadata['Hours']:
            isround = is_fullday(
                organization_metadata['Hours']['Availabilities'])
        if 'Hours' in organization_metadata:
            isknown = True
        str_coords = ','.join(map(str, organization_coordinates))
        if str_coords != '':
            if isround:
                round.append(str_coords)
            elif isknown:
                nonround.append(str_coords)
            else:
                unknown.append(str_coords)
    round_str = '~'.join([generate_point(i, 'gn') for i in round])
    nonround_str = '~'.join([generate_point(i, 'bl')
                             for i in nonround])
    unknown_str = '~'.join([generate_point(i, 'gr') for i in unknown])
    to_join = []
    if round_str != '':
        to_join.append(round_str)
    if nonround_str != '':
        to_join.append(nonround_str)
    if unknown_str != '':
        to_join.append(unknown_str)
    pt = '~'.join(to_join)

    map_params = {
        "l": "map",
        "pt": pt,
    }

    map_api_server = SERVER_ADDRESS
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    main()
