from config_data.config import db_host, db_user_name, db_password, db_db_name
from my_connect import create_connection


def start_create_table():
    database_connect = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with database_connect.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS `users` (id int AUTO_INCREMENT,"
                                                                "telegram_id varchar int UNIQE,"
                                                                "user_name varchar,"
                                                                "settings_id int;")
            cursor.execute("CREATE TABLE IF NOT EXISTS `settings` (id int AUTO_INCREMENT,"
                          "dist_ id str,"
                          "rooms_id id varchar,"
                          "low_price id int,"
                          "high_price id int;")
            database_connect.commit()
            print('База данных готова к работе')

            for data_bases in cursor:
                print(data_bases)
    except Exception as exc:
        print('Ошибка создания таблицы', exc)
    finally:
        database_connect.close()


