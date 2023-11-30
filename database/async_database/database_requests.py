from .database_models import Users, Advertisements, ViewedAdv, SearchSetting, async_session
from sqlalchemy import select, insert


class Requests:
    """Класс для создания select, insert и update запросов к базе данных"""

    @staticmethod
    async def check_entry(tg_id):
        """Метод проверки наличия записи пользователя в таблице 'users'"""
        async with async_session() as session:
            check_entry = await session.execute(select(Users).where(Users.telegram_id == tg_id))
            if check_entry:
                return check_entry.fetchone()
            else:
                return None

    @staticmethod
    async def check_settings(tg_id):
        """Метод проверки наличия записи настроек пользователя в таблице 'searchsetting'"""
        async with async_session() as session:
            check_settings = await session.execute(select(SearchSetting).where(SearchSetting.telegram_id == tg_id))
            if check_settings:
                return check_settings.fetchone()
            else:
                return None

    @staticmethod
    async def check_adv(adv_id):
        """Метод проверки наличия записи объявления в таблице 'advertisements'"""
        async with async_session() as session:
            check_adv = await session.execute(select(Advertisements).where(Advertisements.advertisements_id == adv_id))
            if check_adv:
                return check_adv.fetchone()
            else:
                return None

    @staticmethod
    async def get_viewed_adv(tg_id):
        """Метод получения по telegram_id массива из id всех просмотренных объявлений, внесенных в таблицу 'viewedadv'
        Если же просмотренные объявления отсутствуют, возвращает список с единственным числовым значением 0
        """
        async with async_session() as session:
            apartments_list = [0]
            aparts_request = await session.execute(select(ViewedAdv).where(ViewedAdv.telegram_id == tg_id))
            apartments = aparts_request.fetchall()
            #print('апарты', apartments)
            if apartments:
                for apartment in apartments:
                    if apartments:
                        apartments_list += [adv_id for key, adv_id in apartment.items() if key == 'adv_id']
            else:
                return apartments_list

    @staticmethod
    async def get_entry_apart(telegram_id):
        """Метод получения непросмотренного объявления (т.е. отсутствует в таблице viwedadv конкретно у текущего
        пользователя по telegram_id)"""
        viewed_apartments = await Requests.get_viewed_adv(telegram_id)
        user_settings = await Requests.check_settings(telegram_id)
        print('ключики', user_settings[0].__dict__.keys())
        async with async_session() as session:
            check_apartments = await session.execute(select(Advertisements).
                                                     where(Advertisements.advertisements_id.notin_(viewed_apartments)).
                                                     where(Advertisements.district == user_settings[0].district).
                                                     where(Advertisements.rooms == user_settings[0].rooms).
                                                     where(Advertisements.price > user_settings[0].low_price).
                                                     where(Advertisements.price < user_settings[0].high_price).limit(1)
                                                     )
            return check_apartments.fetchone()

    @staticmethod
    async def insert_entry(tg_id, user_name, full_name='Не указано', phone=0):
        """Метод добавления новых пользователей в таблицу 'users' при нажатии кнопки старт
        params:
        check_entry возвращает False при наличии записи пользователя в таблице 'users', а иначе добавляет запись
        о пользователе в таблицу и возвращает True
        """
        check_entry = await Requests.check_entry(tg_id)
        if check_entry:
            return False
        else:
            async with async_session() as session:
                await session.execute(insert(Users).values(
                    {
                        "telegram_id": tg_id,
                        "user_name": user_name,
                        "full_name": full_name,
                        "phone": phone
                    }))
                await session.commit()
                return True

    @staticmethod
    async def insert_settings(tg_id, district, rooms, low_price, high_price):
        """Метод добавления настроек поиска пользователя в таблицу 'searchsettings', после окончания
        стартового анкетирования
        params:
        check_entry возвращает False при наличии записи в таблице 'searchsettings', а иначе добавляет запись настроек
        поиска в таблицу и возвращает True
        """
        check_settings = await Requests.check_settings(tg_id)
        if check_settings:
            return False
        else:
            async with async_session() as session:
                await session.execute(insert(SearchSetting).values(
                    {
                        "telegram_id": tg_id,
                        "district": district,
                        "rooms": rooms,
                        "low_price": low_price,
                        "high_price": high_price
                    }))
                await session.commit()
                return True

    @staticmethod
    async def insert_advertisements(adv_id, date_adv, district, rooms, floor, price, square, repair, furniture,
                                    description, address, phone, images, url):
        """Метод добавления объявления о квартире в таблицу 'advertisements' из API запроса объявлений
        params:
        check_entry возвращает False при наличии записи в таблице 'advertisements', а иначе добавляет запись объявления
        в таблицу и возвращает True
        """
        check_adv = await Requests.check_adv(adv_id)
        if check_adv:
            return False
        else:
            async with async_session() as session:
                await session.execute(insert(Advertisements).values(
                    {
                        'advertisements_id': adv_id,
                        'date_adv': date_adv,
                        'district': district,
                        'rooms': rooms,
                        'floor': floor,
                        'price': price,
                        'square': square,
                        'repair': repair,
                        'furniture': furniture,
                        'description': description,
                        'address': address,
                        'phone': phone,
                        'images': images,
                        'url': url
                    }))
                await session.commit()
                return True

    @staticmethod
    async def insert_adv_to_viewed(tg_id, adv_id):
        """Метод срабатывающий при получении нового объявления для внесения его в таблицу просмотренных объявлений
        viewedadv"""
        try:
            async with async_session() as session:
                await session.execute(insert(SearchSetting).values(
                    {
                        "telegram_id": tg_id,
                        "adv_id": adv_id
                    }))
                await session.commit()
                return True
        except Exception as exc:
            print('Ошибка. Возможно неуместное использование метода', exc)
            return False
                    # new_adv_in_viewed = (
                    #     f"INSERT INTO `angarhaev`.`viewed` (`telegram_id`, `adv_id`, `favorite`) "
                    #     f"VALUES ('{telegram_id}', '{adv_id}', {0});")
                    # cursor.execute(new_adv_in_viewed)
                    # connection.commit()
