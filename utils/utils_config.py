from config_data.config import API_KEY, API_URL, API_USER
from datetime import datetime, timedelta


class ApiConfig:
    """Класс для хранения настроек поиска"""
    @staticmethod
    def params_request(district, price_low, price_high, rooms):
        """Метод инициализации параметров поиска"""
        params = {
                    'user': API_USER,
                    'token': API_KEY,
                    'metro': district,
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

        return params

    @staticmethod
    def all_adv_request():
        """Метод инициализации поиска всех объявлений из Улан-Удэ для обновления базы"""
        params = {
            'user': API_USER,
            'token': API_KEY,
            'category_id': 2,
            'date1': datetime.now() - timedelta(days=30),
            'date2': datetime.now(),
            'city': 'Бурятия',
            'param[2016]': 'На длительный срок',
            'nedvigimost_type': 2,
            'limit': 50,
        }

        return params


