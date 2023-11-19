from my_connect import create_connection
from config_data.config import db_host, db_user_name, db_password, db_db_name


async def insert_new_entry(id_from_telegram, user_name):
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            new_entry = (f"INSERT INTO `users`"
                         f"( `telegram_id`, `user_name`)"
                         f" VALUES ('{id_from_telegram}, {user_name});")
            cursor.execute(new_entry)
            connection.commit()
            print('Запись внесена')
    except Exception as exc:
        print(exc)

    finally:
        connection.close()
