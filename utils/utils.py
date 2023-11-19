import requests
import json
from config_data.config import API_KEY, url_api, user_api

url = url_api
params = {
    'user': user_api,
    'token': API_KEY,
    'category_id': 2, #2 для квартирб 3 для комнат и 4 для дач
    'price1': 5000,
    'price2': 15000,
    'date1': "2023-11-07",
    'date2': "2023-11-11",
    'city': 'Бурятия, Улан-Удэ',
    'param[2016]': 'На длительный срок',
    'param[1945]': 2, #количество комнат
    'nedvigimost_type': 2,
    'limit': 5,
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    json_dict = json.loads(response.text)
    print(json_dict)
else:
    print('Error:', response.status_code)