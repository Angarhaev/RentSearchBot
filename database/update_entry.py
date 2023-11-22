from database.my_connect import create_connection
from config_data.config import db_host, db_user_name, db_password, db_db_name


async def check_settings(telegram_id):
    """Функция для проверки наличия настроек пользователя в базе данных"""
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    with connection.cursor() as cursor:
        entry_check = (f"SELECT * FROM `angarhaev`.`settings` WHERE `telegram_id` = {telegram_id} limit 1")
        cursor.execute(entry_check)
        res = cursor.fetchone()
        return res


async def select_data_settings(telegram_id):
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            check_low = (f"SELECT * FROM `angarhaev`.`settings` WHERE `telegram_id` = {telegram_id} limit 1")
            cursor.execute(check_low)
            res = cursor.fetchone()
            return res
    except Exception as exc:
        print('Не удалось получить данные из таблицы')
        return None

async def update_low(telegram_id, low_price):
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            update_low_price = (f"UPDATE `settings` SET `low_price` = '{low_price}' WHERE `settings`.`telegram_id` = {telegram_id};")
            cursor.execute(update_low_price)
            connection.commit()
            print('Данные успешно обновлены')
    except Exception as exc:
        print('Не удалось обновить данные')


