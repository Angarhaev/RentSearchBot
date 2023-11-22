import requests
import json
from config_data.config import API_KEY, url_api, user_api
from datetime import datetime, timedelta


url = url_api
apartments_dict: dict = {}


async def recurs(data: dict, tg_id: int, id_adv=None):
    if 'id' in data and data['id'] not in apartments_dict[tg_id]:
        id_adv = data['id']
        apartments_dict[tg_id][id_adv] = {}

    for key, value in data.items():
        if isinstance(value, dict):
            await recurs(value, tg_id, id_adv)
        elif isinstance(value, list):
            for list_elem in value:
                await recurs(list_elem, tg_id, id_adv)
        else:
            if key in {'time', 'metro', 'url', 'description', 'Этаж', "техника", "Общая площадь",
                       "Ремонт", "Количество комнат", "price", "address", "phone", "Мебель"}:
                apartments_dict[tg_id][id_adv][key] = value
            elif key == 'imgurl':
                if 'images' in apartments_dict[tg_id][id_adv]:
                    apartments_dict[tg_id][id_adv]['images'].append(value)
                else:
                    apartments_dict[tg_id][id_adv]['images'] = []
                    apartments_dict[tg_id][id_adv]['images'].append(value)


async def advertisement(telegram_id, metro, price_low, price_high, rooms):
    params = {
        'user': user_api,
        'token': API_KEY,
        'metro': metro,
        'category_id': 2,
        'price1': price_low,
        'price2': price_high,
        'date1': datetime.now() - timedelta(days=30),
        'date2': datetime.now(),
        'city': 'Бурятия',
        'param[2016]': 'На длительный срок',
        'param[2019]': rooms,
        'nedvigimost_type': 2,
        'limit': 50,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        apartments_dict[telegram_id] = {}
        await recurs(json_data, telegram_id)
        #print(json_data)

    else:
        print('Error:', response.status_code)
        return None

    params_to_db = {'time', 'metro', 'url', 'description', 'Этаж', "техника", "Общая площадь",
                    "Ремонт", "Количество комнат", "price", "address", "phone", "Мебель"}

    for key, value in apartments_dict[telegram_id].items():
        for i_param in params_to_db:
            if i_param not in value:
                value[i_param] = 'Не указано'

        for i_key, i_value in value.items():
            if i_key == 'images':
                if len(value[i_key]) < 3:
                    for i in range(0, 3 - len(value[i_key])):
                        value[i_key].append('Не указано')

    return apartments_dict[telegram_id]

# answer = advertisement(300844218, 'Советский', 10000, 25000, '1')
# print(answer)
