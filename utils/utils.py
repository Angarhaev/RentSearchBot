import requests
import json
from config_data.config import API_KEY, url_api, user_api

url = url_api

#async def advertisement(price_low, price_high, rooms)

params = {
    'user': user_api,
    'token': API_KEY,
    #'metro': 'Железнодорожный',
    'category_id': 2, #2 для квартирб 3 для комнат и 4 для дач
    'price1': 10000,
    'price2': 15000,
    'date1': "2023-11-01",
    'date2': "2023-11-19",
    'city': 'Бурятия, Улан-Удэ',
    'param[2016]': 'На длительный срок',
    'param[2019]': 1, #количество комнат
    'nedvigimost_type': 2,
    'limit': 100,
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    json_info = json.loads(response.text)
    print(json_info)

    with open('flats.txt', 'w', encoding='utf-8') as json_dict:
        my_json_dict = dict()
        my_json_dict['data'] = json_info['data']
        json.dump(my_json_dict, json_dict, indent=4)


else:
    print('Error:', response.status_code)
