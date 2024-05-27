import requests
import json
from config_data.config import API_URL
from .utils_config import ApiConfig
from . import EasyFunc


url = API_URL


class ApiInteraction:
    def __init__(self):
        self.apartments_dict: dict = {}
    """Клаcc для запросов и получения ответов от API"""

    async def recurs(self, data_adv: dict, id_adv=None):
        """
        Функция рекурсивного поиска для заполнения по json словарю с ответом от API
        для записей полей таблицы Advertisements из базы данных
        Params:
        data_adv - словарь для рекурсивного поиска
        tg_id - telegram_id пользователя
        id_adv - уникальный id объявления
        looking_keys - множество имен ключей для внесения значений в словарь для бд
        Обратите внимание на ключ 'images'. Это список ключей со ссылками на фотографии квартир: т.к. они хранятся
        списком словарей, где имя каждого ключа 'imgurl', а значение ссылка
        """
        if 'id' in data_adv and data_adv['id']:
            id_adv = data_adv['id']
            self.apartments_dict[id_adv] = {}

        looking_keys = {'time', 'metro', 'url', 'description', 'Этаж', "техника", "Общая площадь",
                        "Ремонт", "Количество комнат", "price", "address", "phone", "Мебель"}

        for key, value in data_adv.items():
            if isinstance(value, dict):
                await self.recurs(data_adv=value, id_adv=id_adv)
            elif isinstance(value, list):
                for i in value:
                    if isinstance(i, dict):
                        await self.recurs(data_adv=i, id_adv=id_adv)
            else:
                #print('check', key, value)
                if id_adv is not None:
                    if key in looking_keys:
                        self.apartments_dict[id_adv][key] = value
                    elif key == 'imgurl':
                        if 'images' in self.apartments_dict[id_adv]:
                            self.apartments_dict[id_adv]['images'] += f', {value}'
                        else:
                            self.apartments_dict[id_adv]['images'] = value


    @staticmethod
    async def all_advertisement_request_api(self):
        """Метод запроса всех объявлений для обновления базы"""
        params = ApiConfig.all_adv_request()
        response = requests.get(url, params=params)

        if response.status_code == 200:
            json_data = json.loads(response.text)
            #print(json_data)
            request_adv = self.apartments_dict
            await request_adv.recurs(data_adv=json_data)
        else:
            print('Error:', response.status_code)
            return None
        print(request_adv.apartments_dict)
        filtered_dict = await EasyFunc.not_indicated(request_adv.apartments_dict)

        return filtered_dict
