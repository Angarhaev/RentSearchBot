from aiogram.types import InputMediaPhoto
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest


class EasyFunc:
    """Класс для простых методов расчета, сортировки, поиска значений и т.д."""

    @staticmethod
    async def links_images(dict_links):
        """Функция получения списка ссылок фотографий объявления для отправки нескольких фотографий в одном сообщении
        при нажатии кнопки 'Больше фото' в клавиатуре под фото.
        Params:
        media - хранит список с объектами класса InputMediaPhoto
        count - ограничивает список количеством 10 объектов, так как больше телеграм не может отправить в одном сообщении
        """
        media = []
        count = 0
        for i_num, i_url in enumerate(dict_links):
            if i_num != 0 and count < 10:
                count += 1
                media.append(InputMediaPhoto(media=i_url))
        return media

    @staticmethod
    async def not_indicated(filterable_dict):
        """
        Функция для заполнения словаря парой ключ-значения, которые не были инициализированы. Значения будут
        принимать дефолтное значение 'Не указано'
        """
        params_to_db = {'time', 'metro', 'url', 'description', 'Этаж', "техника", "Общая площадь",
                        "Ремонт", "Количество комнат", "price", "address", "phone", "Мебель", "images"}

        for key, value in filterable_dict.items():
            for i_param in params_to_db:
                if i_param not in value:
                    value[i_param] = 'Не указано'

        return filterable_dict

    @staticmethod
    def custom_message_filter_search_settings_high():
        """Кастомный фильтр для декорирования функции ввода значения с учетом другой границы поиска"""
        def decorator(func):
            async def wrapped(message: Message, state: FSMContext):
                data = await state.get_data()
                stored_low_value = int(data.get('low', 0))
                low = int(message.text)
                if low > stored_low_value:
                    return await func(message, state)
                else:
                    try:
                        for i in range(message.message_id, 0, -1):
                            await message.bot.delete_message(message.from_user.id, i)
                    except TelegramBadRequest:
                        await message.answer(
                            f"Верхняя граница должна быть цифровым значением (без букв и пробелов). "
                            f"Меньше чем 100000 и не меньше, чем нижняя граница {int(data['low'])}",
                            reply_markup=data['user_keyboard_back'])
                        await state.set_state(AlSettings.max_price)
            return wrapped
        return decorator

    @staticmethod
    def custom_message_filter_edit_settings_low():
        """Кастомный фильтр для декорирования функции ввода значения с учетом другой границы поиска"""
        def decorator(func):
            async def wrapped(message: Message, state: FSMContext):
                data = await state.get_data()
                user_dict_set = data['user_dict_set']
                stored_high_value = int(user_dict_set[0].high_price)
                low = int(message.text)
                if low < stored_high_value:
                    return await func(message, state)
                else:
                    try:
                        for i in range(message.message_id, 0, -1):
                            await message.bot.delete_message(message.from_user.id, i)
                    except TelegramBadRequest:
                        await message.answer(f"Неверно указан параметр 'Нижняя граница': {message.text}. "
                                             f"Внимательно посмотрите диапазон значений: \n"
                                             f"Ваша текущая нижняя граница: {user_dict_set[0].low_price}\n"
                                             f"Ваша текущая верхняя граница: {user_dict_set[0].high_price}\n"
                                             f"Выберите параметр для редактирования или начните поиск:",
                                             reply_markup=data['keyboard_settings'])
                        await state.set_state(AlSettings.update)

            return wrapped

        return decorator

    @staticmethod
    def custom_message_filter_edit_settings_high():
        """Кастомный фильтр для декорирования функции ввода значения с учетом другой границы поиска"""
        def decorator(func):
            async def wrapped(message: Message, state: FSMContext):
                data = await state.get_data()
                user_dict_set = data['user_dict_set']
                stored_low_value = int(user_dict_set[0].low_price)
                high = int(message.text)
                if high > stored_low_value:
                    return await func(message, state)
                else:
                    try:
                        for i in range(message.message_id, 0, -1):
                            await message.bot.delete_message(message.from_user.id, i)
                    except TelegramBadRequest:
                        await message.answer(f"Неверно указан параметр 'Верхняя граница': {message.text}. "
                                             f"Внимательно посмотрите диапазон значений: \n"
                                             f"Ваша текущая нижняя граница: {user_dict_set[0].low_price}\n"
                                             f"Ваша текущая верхняя граница: {user_dict_set[0].high_price}\n"
                                             f"Выберите параметр для редактирования или начните поиск:",
                                             reply_markup=data['keyboard_settings'])
                        await state.set_state(AlSettings.update)

            return wrapped

        return decorator
