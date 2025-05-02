import requests
from config import SERVER_ADDRESS, API_KEY_STATIC

def find_business(ll, text):
    search_params = {
        "apikey": API_KEY_STATIC,
        "lang": "ru_RU",
        "ll": ll,
        "spn": "0.001,0.001",
        "type": "biz",
        "text": text,
    }

    response = requests.get(SERVER_ADDRESS, params=search_params)
    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=SERVER_ADDRESS, status=response.status_code, reason=response.reason))

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    organizations = json_response["features"]
    return organizations[0] if organizations else None
