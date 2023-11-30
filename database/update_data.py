from database.my_connect import create_connection
from config_data.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME


async def update_high_db(telegram_id, high_price):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    try:
        with connection.cursor() as cursor:
            update_high_price = (f"UPDATE `settings` SET `high_price` = '{high_price}' "
                                 f"WHERE `settings`.`telegram_id` = {telegram_id};")
            cursor.execute(update_high_price)
            connection.commit()
            print('Данные успешно обновлены')
    except Exception as exc:
        print('Не удалось обновить данные', exc)
    finally:
        connection.close()


async def update_low_db(telegram_id, low_price):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    try:
        with connection.cursor() as cursor:
            update_low_price = (f"UPDATE `settings` SET `low_price` = '{low_price}' "
                                f"WHERE `settings`.`telegram_id` = {telegram_id};")
            cursor.execute(update_low_price)
            connection.commit()
            print('Данные успешно обновлены')
    except Exception as exc:
        print('Не удалось обновить данные', exc)
    finally:
        connection.close()


async def update_district_db(telegram_id, district):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    try:
        with connection.cursor() as cursor:
            update_district = (f"UPDATE `settings` SET `district` = '{district}' "
                               f"WHERE `settings`.`telegram_id` = {telegram_id};")
            cursor.execute(update_district)
            connection.commit()
            print('Данные успешно обновлены')
    except Exception as exc:
        print('Не удалось обновить данные', exc)
    finally:
        connection.close()


async def update_rooms_db(telegram_id, rooms):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    try:
        with connection.cursor() as cursor:
            update_rooms = (f"UPDATE `settings` SET `rooms` = '{rooms}' "
                            f"WHERE `settings`.`telegram_id` = {telegram_id};")
            cursor.execute(update_rooms)
            connection.commit()
            print('Данные успешно обновлены')
    except Exception as exc:
        print('Не удалось обновить данные', exc)
    finally:
        connection.close()