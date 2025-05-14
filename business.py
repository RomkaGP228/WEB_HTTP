import requests
from config import SEARCH_ADDRESS, API_KEY_SEARCH

def find_business(ll, res, text):
    search_params = {
        "apikey": API_KEY_SEARCH,
        "lang": "ru_RU",
        "ll": ll,
        "spn": "0.001,0.001",
        "type": "biz",
        'text': text,
        "results": res
    }

    response = requests.get(SEARCH_ADDRESS, params=search_params)
    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=SEARCH_ADDRESS, status=response.status_code, reason=response.reason))

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    return json_response
