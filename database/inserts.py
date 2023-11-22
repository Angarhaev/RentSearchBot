from database.my_connect import create_connection
from config_data.config import db_host, db_user_name, db_password, db_db_name


async def insert_new_entry(telegram_id, user_name):
    """Функция для внесения пользователя в базу данных, если его там нет"""
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    with connection.cursor() as cursor:
        entry_check = (f"SELECT * FROM `angarhaev`.`users` WHERE `telegram_id` = {telegram_id} limit 1")
        cursor.execute(entry_check)
        res = cursor.fetchone()
        if res:
            return res['user_name']
        else:
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
            return None


async def insert_settings(telegram_id, district, rooms, low_price, high_price):
    """Функция для внесения настроек пользователя в базу данных"""
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


async def insert_adv(adv_id, date_adv, metro, rooms, floor, price, square, repair, furniture,
                     description, address, phone, image_1, image_2, image_3, url):
    """Функция для внесения записей о квартирах в базу данных"""
    connection = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with connection.cursor() as cursor:
            new_entry = (
                f"INSERT INTO `angarhaev`.`advertisements` (`adv_id`, `date_adv`, `metro`, `rooms`, `floor`, "
                f"`price`, `square`, `repair`, `furniture`, `description`, `address`, `phone`, "
                f"`image_1`, `image_2`, `image_3`, `url`) "
                f"VALUES ('{adv_id}', '{date_adv}', '{metro}', '{rooms}', '{floor}', '{price}', '{square}', "
                f"'{repair}', '{furniture}', '{description}', "
                f"'{address}','{phone}', '{image_1}', '{image_2}', '{image_3}', '{url}');")
            cursor.execute(new_entry)
            connection.commit()
            print('Записи о квартирах внесены в бд')
    except Exception as exc:
        print(exc)

    finally:
        connection.close()
