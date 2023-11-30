from database.my_connect import create_connection
from config_data.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME


async def insert_new_entry(telegram_id, user_name):
    """Функция для внесения пользователя в базу данных, если его там нет"""
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    with connection.cursor() as cursor:
        entry_check = f"SELECT * FROM `angarhaev`.`users` WHERE `telegram_id` = {telegram_id} limit 1"
        cursor.execute(entry_check)
        res = cursor.fetchone()
        if res:
            return True
        else:
            try:
                with connection.cursor() as cursor_insert:
                    new_entry = (f"INSERT INTO `angarhaev`.`users`"
                                 f"( `telegram_id`, `user_name`)"
                                 f" VALUES ('{telegram_id}', '{user_name}');")
                    cursor_insert.execute(new_entry)
                    connection.commit()
                    print('Запись пользователя внесена')
            except Exception as exc:
                print(exc)
            finally:
                connection.close()
            return None


async def insert_settings(telegram_id, district, rooms, low_price, high_price):
    """Функция для внесения настроек пользователя в базу данных"""
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    with connection.cursor() as cursor:
        entry_check = f"SELECT * FROM `angarhaev`.`settings` WHERE `telegram_id` = {telegram_id} limit 1"
        cursor.execute(entry_check)
        res = cursor.fetchone()
        if res:
            return True
        else:
            try:
                with connection.cursor() as cursor_insert:
                    new_entry = (f"INSERT INTO `angarhaev`.`settings`"
                                 f"( `telegram_id`, `district`, `rooms`, `low_price`, `high_price`)"
                                 f" VALUES ('{telegram_id}', '{district}', '{rooms}', '{low_price}', '{high_price}');")
                    cursor_insert.execute(new_entry)
                    connection.commit()
                    print('Запись настроек поиска внесена')
            except Exception as exc:
                print(exc)

            finally:
                connection.close()
            return None


async def insert_adv(adv_id, date_adv, metro, rooms, floor, price, square, repair, furniture,
                     description, address, phone, image_1, image_2, image_3,
                     image_4, image_5, image_6, image_7, image_8, image_9, url):
    """Функция для внесения записей о квартирах в базу данных"""
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    with connection.cursor() as cursor:
        entry_check = f"SELECT * FROM `angarhaev`.`settings` WHERE `telegram_id` = {adv_id} limit 1"
        cursor.execute(entry_check)
        res = cursor.fetchone()
        if res:
            return True
        else:
            try:
                with connection.cursor() as cursor_insert:
                    new_entry = (
                        f"INSERT INTO `angarhaev`.`advertisements` (`adv_id`, `date_adv`, `metro`, `rooms`, `floor`, "
                        f"`price`, `square`, `repair`, `furniture`, `description`, `address`, `phone`, "
                        f"`image_1`, `image_2`, `image_3`, `image_4`, `image_5`, `image_6`, "
                        f"`image_7`, `image_8`, `image_9`, `url`) "
                        f"VALUES ('{adv_id}', '{date_adv}', '{metro}', '{rooms}', '{floor}', '{price}', '{square}', "
                        f"'{repair}', '{furniture}', '{description}', "
                        f"'{address}','{phone}', '{image_1}', '{image_2}', '{image_3}', '{image_4}', '{image_5}', '{image_6}', "
                        f"'{image_7}', '{image_8}', '{image_9}', '{url}');")
                    cursor_insert.execute(new_entry)
                    connection.commit()
                    print('Записи о квартирах внесены в бд')
            except Exception as exc:
                print(exc)
            finally:
                connection.close()


async def insert_adv_to_viewed(telegram_id, adv_id):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    try:
        with connection.cursor() as cursor:
            new_adv_in_viewed = (
                f"INSERT INTO `angarhaev`.`viewed` (`telegram_id`, `adv_id`, `favorite`) "
                f"VALUES ('{telegram_id}', '{adv_id}', {0});")
            cursor.execute(new_adv_in_viewed)
            connection.commit()
            print('Запись о квартире добавлена в просмотрено')
    except Exception as exc:
        print(exc)
    finally:
        connection.close()
