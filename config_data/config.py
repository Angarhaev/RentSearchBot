import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

"""Параметры для соединения с базой данных"""
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

"""Параметры для поиска квартиры"""
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('URL_API')
API_USER = os.getenv('USER_API')


SQL_ALCHEMY_URL = f"mysql+asyncmy://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"