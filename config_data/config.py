import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

"""Параметры для соединения с базой данных"""
db_host = os.getenv('DB_HOST')
db_user_name = os.getenv('DB_USER_NAME')
db_password = os.getenv('DB_PASSWORD')
db_db_name = os.getenv('DB_NAME')

"""Параметры для поиска квартиры"""
API_KEY = os.getenv('API_KEY')
url_api = os.getenv('URL_API')
user_api = os.getenv('USER_API')
