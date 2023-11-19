from database.my_connect import create_connection
from config_data.config import db_host, db_user_name, db_password, db_db_name


async def insert_new_entry(telegram_id, user_name):
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            new_entry = (f"INSERT INTO `angarhaev`.`users`"
                         f"( `telegram_id`, `user_name`)"
                         f" VALUES ('{telegram_id}', '{user_name}');")
            cursor.execute(new_entry)
            connection.commit()
            print('Запись пользователя внесена')
    except Exception as exc:
        print(exc)

    finally:
        connection.close()


async def insert_settings(telegram_id, district, rooms, low_price, high_price):
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            new_entry = (f"INSERT INTO `angarhaev`.`settings`"
                         f"( `telegram_id`, `dist_id`, `rooms_id`, `low_price`, `high_price`)"
                         f" VALUES ('{telegram_id}', '{district}', '{rooms}', '{low_price}', '{high_price}');")
            cursor.execute(new_entry)
            connection.commit()
            print('Запись настроек поиска внесена')
    except Exception as exc:
        print(exc)

    finally:
        connection.close()
