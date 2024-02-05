from datetime import datetime, timedelta
from utils.utils import ApiInteraction
from .database_models import Users, Advertisements, ViewedAdv, SearchSetting, async_session
from sqlalchemy import select, insert, update, delete
from cachetools import TTLCache


class CacheDatabase:
    """Класс для кэширования данных"""
    _cache = TTLCache(maxsize=100, ttl=86400)

    @classmethod
    def _get_cache_key(cls, method, *args, **kwargs):
        """Метод генерации ключа для кэша на основе переданных аргументов"""
        return f"{method.__name__}_{'_'.join(map(str, args))}_{'_'.join(map(str, kwargs.values()))}"

    @classmethod
    async def fetch_and_cache(cls, method, *args, **kwargs):
        """Общий метод для выполнения запроса, кэширования и получения результатов"""
        cache_key = cls._get_cache_key(method, *args, **kwargs)
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        result = await method(*args, **kwargs)
        cls._cache[cache_key] = result
        return result

    @classmethod
    async def update_cache(cls, cache_method, *args, **kwargs):
        """Общий метод для кеширования обновленных данных"""
        cache_key = cls._get_cache_key(cache_method, *args, **kwargs)
        result = await cache_method(*args, **kwargs)
        cls._cache[cache_key] = result
        return result


cache = CacheDatabase()


class DatabaseCommands:
    """Класс для select, insert и update запросов к базе данных"""

    @classmethod
    async def select_one_user(cls, tg_id):
        """Метод проверки наличия записи пользователя в таблице 'users' сначала с помощью кэша, а иначе через
        метод запроса к базе данных _select_one_user по telegram id"""
        return await cache.fetch_and_cache(cls._select_one_user, tg_id)

    @staticmethod
    async def _select_one_user(tg_id):
        """Метод проверки наличия записи пользователя в таблице 'users' через запрос к базе данных"""
        async with async_session() as session:
            check_entry = await session.execute(select(Users).where(Users.telegram_id == tg_id).limit(1))
            if check_entry:
                return check_entry.fetchone()
            else:
                return None

    @classmethod
    async def select_settings_user(cls, tg_id):
        """Метод проверки наличия настроек пользователя в таблице 'searchsettings' сначала с помощью кэша, а иначе через
        метод запроса к базе данных _select_settings_user по telegram id"""
        return await cache.fetch_and_cache(cls._select_settings_user, tg_id)

    @staticmethod
    async def _select_settings_user(tg_id):
        """Метод проверки наличия записи настроек пользователя в таблице 'searchsettings'. Select запрос на одну запись
        настроек одного конкретного пользователя"""
        async with async_session() as session:
            check_settings = await session.execute(select(SearchSetting).where(SearchSetting.telegram_id == tg_id))
            if check_settings:
                return check_settings.fetchone()
            else:
                return None

    @classmethod
    async def select_one_adv(cls, adv_id):
        """Метод получения одного объявления"""
        return await cache.fetch_and_cache(cls._select_one_adv, adv_id)

    @staticmethod
    async def _select_one_adv(adv_id):
        """Метод проверки наличия записи объявления в таблице 'advertisements'. Select запрос на одно объявление"""
        async with async_session() as session:
            check_adv = await session.execute(
                select(Advertisements).
                where(Advertisements.advertisements_id == adv_id)
            )
            if check_adv:
                return check_adv.fetchone()
            else:
                return None

    @classmethod
    async def get_viewed_ads(cls, tg_id, adv_id):
        """Метод получения просмотренного обновления из базы"""
        return await cache.fetch_and_cache(cls._get_viewed_ads, tg_id, adv_id)

    @staticmethod
    async def _get_viewed_ads(tg_id, adv_id):
        """Метод запроса просмотренных страниц"""
        async with async_session() as session:
            check_entry = await session.execute(
                select(ViewedAdv).
                where(ViewedAdv.telegram_id == tg_id).
                where(ViewedAdv.adv_id == adv_id)
            )
            if check_entry:
                return check_entry.fetchone()
            else:
                return None


    @classmethod
    async def select_not_viewed_adv_cache(cls, tg_id):
        """Метод для просмотра объявлений из кэша, соответствующих настройкам"""
        user_settings = await DatabaseCommands.select_settings_user(tg_id)
        cache_ads = await cache.fetch_and_cache(cls._select_not_viewed_adv_to_db, tg_id)
        for cache_ad in cache_ads:
            print('Ищем в КЭШЕ')
            if (cache_ad[0].district == user_settings[0].district and
                    cache_ad[0].rooms == user_settings[0].rooms and

                    #пока временно прайс сделали 0 теперь надо временно учесть
                    #user_settings[0].low_price <= cache_ad[0].price <= user_settings[0].high_price and

                    await DatabaseCommands.get_viewed_ads(tg_id=tg_id, adv_id=cache_ad[0].advertisements_id) is None):
                await DatabaseCommands.insert_adv_to_viewed(tg_id=tg_id,
                                                            adv_id=cache_ad[0].advertisements_id,
                                                            date_adv=cache_ad[0].date_adv)
                return cache_ad

    @staticmethod
    async def _select_not_viewed_adv_to_db(tg_id):
        """Метод получения непросмотренного объявления (т.е. отсутствует в таблице viwedadv конкретно у текущего
        пользователя по telegram_id)"""
        user_settings = await DatabaseCommands.select_settings_user(tg_id)
        async with async_session() as session:
            check_apartments = await session.execute(
                select(Advertisements).
                where(Advertisements.advertisements_id.notin_(
                    select(ViewedAdv.adv_id).
                    where(ViewedAdv.telegram_id == tg_id))).
                where(Advertisements.district == user_settings[0].district).
                where(Advertisements.rooms == user_settings[0].rooms).

                #пока временно прайс сделали 0 теперь надо временно учесть
                #where(Advertisements.price >= user_settings[0].low_price).
                #where(Advertisements.price <= user_settings[0].high_price).

                limit(20)
            )

            return check_apartments.fetchall()

    @classmethod
    async def insert_user_start(cls, tg_id, user_name, full_name='Не указано', phone=0):
        """Метод добавления новых пользователей в таблицу 'users' при нажатии кнопки старт
        params:
        check_entry возвращает False при наличии записи пользователя в таблице 'users', а иначе добавляет запись
        о пользователе в таблицу и возвращает True
        """
        check_entry = await DatabaseCommands.select_one_user(tg_id)
        if check_entry:
            return False
        else:
            async with async_session() as session:
                await session.execute(
                    insert(Users).values(
                        {
                            "telegram_id": tg_id,
                            "user_name": user_name,
                            "full_name": full_name,
                            "phone": phone
                        }))
                await session.commit()
                await cache.update_cache(cls._select_one_user, tg_id)
                return True

    @classmethod
    async def insert_settings(cls, tg_id, district, rooms, low_price, high_price):
        """Метод добавления настроек поиска пользователя в таблицу 'searchsettings', после окончания
        стартового анкетирования
        params:
        check_entry возвращает False при наличии записи в таблице 'searchsettings', а иначе добавляет запись настроек
        поиска в таблицу и возвращает True
        """
        check_settings = await DatabaseCommands.select_settings_user(tg_id)
        if check_settings:
            return False
        else:
            async with async_session() as session:
                await session.execute(
                    insert(SearchSetting).values(
                        {
                            "telegram_id": tg_id,
                            "district": district,
                            "rooms": rooms,
                            "low_price": low_price,
                            "high_price": high_price
                        }))
                await session.commit()
                await cache.update_cache(cls._select_settings_user, tg_id)
                return True

    @classmethod
    async def insert_advertisements(cls, adv_id, date_adv, district, rooms, floor, price, square, repair, furniture,
                                    description, address, phone, images, url):
        """Метод добавления объявления о квартире в таблицу 'advertisements' из API запроса объявлений
        params:
        check_entry возвращает False при наличии записи в таблице 'advertisements', а иначе добавляет запись объявления
        в таблицу и возвращает True
        """
        check_adv = await DatabaseCommands.select_one_adv(adv_id)
        if check_adv:
            return False
        else:
            async with async_session() as session:
                await session.execute(
                    insert(Advertisements).values(
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
                await cache.update_cache(cls._select_one_adv, adv_id)
                return True

    @classmethod
    async def insert_adv_to_viewed(cls, tg_id, adv_id, date_adv):
        """Метод срабатывающий при получении нового объявления для внесения его в таблицу просмотренных объявлений
        viewedadv"""
        try:
            async with async_session() as session:
                await session.execute(
                    insert(ViewedAdv).values(
                        {
                            "telegram_id": tg_id,
                            "adv_id": adv_id,
                            "date_adv": date_adv
                        }
                    ))
                await session.commit()
                await cache.update_cache(cls._get_viewed_ads, tg_id, adv_id)
                return True
        except Exception as exc:
            print('Ошибка. Возможно неуместное использование метода', exc)
            return False

    @classmethod
    async def update_high_price(cls, tg_id, new_high_price):
        """Метод для обновления настроек пользователя. Параметр: high_price - верхняя граница цены"""
        async with async_session() as session:
            await session.execute(
                update(SearchSetting).
                where(SearchSetting.telegram_id == tg_id).
                values(high_price=new_high_price)
            )
            await session.commit()
            await cache.update_cache(cls._select_settings_user, tg_id)
            await cache.update_cache(cls._select_not_viewed_adv_to_db,  tg_id)

    @classmethod
    async def update_low_price(cls, tg_id, new_low_price):
        """Метод для обновления настроек пользователя. Параметр: low_price - нижняя граница цены"""
        async with async_session() as session:
            await session.execute(
                update(SearchSetting).
                where(SearchSetting.telegram_id == tg_id).
                values(low_price=new_low_price)
            )
            await session.commit()
            await cache.update_cache(cls._select_settings_user, tg_id)
            await cache.update_cache(cls._select_not_viewed_adv_to_db, tg_id)

    @classmethod
    async def update_district(cls, tg_id, new_district):
        """Метод для обновления настроек пользователя. Параметр: district - район города"""
        async with async_session() as session:
            await session.execute(
                update(SearchSetting).
                where(SearchSetting.telegram_id == tg_id).
                values(district=new_district)
            )
            await session.commit()
            await cache.update_cache(cls._select_settings_user, tg_id)
            await cache.update_cache(cls._select_not_viewed_adv_to_db, tg_id)

    @classmethod
    async def update_rooms(cls, tg_id, new_rooms):
        """Метод для обновления настроек пользователя. Параметр: rooms - количество комнат"""
        async with async_session() as session:
            await session.execute(
                update(SearchSetting).
                where(SearchSetting.telegram_id == tg_id).
                values(rooms=new_rooms)
            )
            await session.commit()
            await cache.update_cache(cls._select_settings_user, tg_id)
            await cache.update_cache(cls._select_not_viewed_adv_to_db, tg_id)

    @staticmethod
    async def delete_old_adv():
        """Метод для удаления старых объявлений"""
        async with (async_session() as session):
            two_weeks = datetime.now() - timedelta(weeks=2)
            await session.execute(delete(Advertisements).where(Advertisements.date_adv < two_weeks))
            await session.commit()

    @staticmethod
    async def update_adv_base():
        """Метод обновления объявлений в базе"""
        adv_dict = await ApiInteraction.all_advertisement_request_api()
        #print(adv_dict)
        for key, value in adv_dict.items():
            await DatabaseCommands.insert_advertisements(
                adv_id=key,
                date_adv=value["time"],
                district=value["metro"],
                rooms=value["Количество комнат"],
                floor=value["Этаж"],
                price=value["price"],
                square=value["Общая площадь"],
                repair=value["Ремонт"],
                furniture=value["Мебель"],
                description=value["description"],
                address=value["address"],
                phone=value["phone"],
                images=value["images"],
                url=value["url"]
            )

