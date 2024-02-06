from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import texts


class ButtonsCreate:
    """Класс для создания кнопок"""
    @staticmethod
    async def create_one(button_one: dict[str, int: str, int], button_back: dict[str, int: str, int] = None,
                         width: int = 1):
        """Метод для создания одинокой произвольной кнопки с возможностью наличия
           кнопки "Назад" при явном указании"""
        one_button_keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []

        for key, button in button_one.items():
            buttons.append(InlineKeyboardButton(text=button, callback_data=key))

        one_button_keyboard.row(*buttons, width=width)

        kb_button_back = await ButtonsCreate.button_back_add(button_back)
        if kb_button_back:
            one_button_keyboard.row(kb_button_back, width=width)

        return one_button_keyboard.as_markup()

    @staticmethod
    async def button_back_add(button_back: dict[str, int: str, int]):
        """Метод кнопки дополнительной кнопки "Назад" для клавиатуры"""
        if button_back:
            for key, button in button_back.items():
                kb_button_back = InlineKeyboardButton(text=button, callback_data=key)
                return kb_button_back
        else:
            return None

    @staticmethod
    async def create_inline_keyboard(width: int, buttons_dict: dict[str, int: str, int],
                                     button_back: dict[str, int: str, int] = None):
        """Метод для создания произвольного количества кнопок с возможностью наличия
        кнопки "Назад" при явном указании"""
        rooms_menu: InlineKeyboardBuilder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []

        for key, button in buttons_dict.items():
            buttons.append(InlineKeyboardButton(text=button, callback_data=key))

        rooms_menu.row(*buttons, width=width)

        kb_button_back = await ButtonsCreate.button_back_add(button_back)
        if kb_button_back:
            rooms_menu.row(kb_button_back)

        return rooms_menu.as_markup()


class KeyboardsCreateSearchSettings:
    """Класс для создания клавиатур для модуля search_settings"""

    @staticmethod
    async def create_keyboard_back():
        """Метод для создания клавиатуры, состоящей из кнопки back"""
        keyboard_back = await ButtonsCreate.create_one(button_one=texts.back, button_back=None)
        return keyboard_back

    @staticmethod
    async def create_district():
        """Метод для создания клавиатуры выбора района города"""
        keyboard_district = await ButtonsCreate.create_inline_keyboard(width=2,
                                                                       buttons_dict=texts.district_choose_inline,
                                                                       button_back=texts.back)
        return keyboard_district

    @staticmethod
    async def create_rooms():
        """Метод для создания клавиатуры выбора количества комнат"""
        keyboard_rooms = await ButtonsCreate.create_inline_keyboard(width=3, buttons_dict=texts.rooms_inline,
                                                                    button_back=texts.back)
        return keyboard_rooms

    @staticmethod
    async def create_keyboard_swipe():
        """Метод для создания клавиатуры состоящей из кнопки swipe и показывающего нам первый вариант с квартирой"""
        keyboard_swipe = await ButtonsCreate.create_inline_keyboard(width=1, buttons_dict=texts.swipe)
        return keyboard_swipe


class KeyboardsStartCreate:
    """Класс для создания клавиатур для модуля start_handlers"""

    @staticmethod
    async def create_start_search():
        """Метод для создания клавиатуры после нажатия кнопки старт 'Приступить к поиску'"""
        keyboard_start_search = await ButtonsCreate.create_one(button_one=texts.first)
        return keyboard_start_search

    @staticmethod
    async def create_repeat_start_search():
        """Метод для создания клавиатуры при нажатии на кнопку старт, но если пользователь уже есть в базе"""
        keyboard_repeat_start_search = await ButtonsCreate.create_one(width=2, button_one=texts.again_keyboard,
                                                                      button_back=texts.back)
        return keyboard_repeat_start_search


class KeyboardEditCreate:
    """Класс для создания клавиатуры для модуля edit_settings"""
    @staticmethod
    async def create_start_search():
        """Метод для создания клавиатуры при нажатии на кнопку старт, но если пользователь уже есть в базе и
        находится в состоянии редактирования настроек"""
        keyboard_start_search = await ButtonsCreate.create_one(button_one=texts.first)
        return keyboard_start_search

    @staticmethod
    async def create_settings():
        """Метод для создания клавиатуры для редактирования настроек поиска"""
        keyboard_settings = await ButtonsCreate.create_inline_keyboard(width=1, buttons_dict=texts.params_inline,
                                                                       button_back=texts.back)
        return keyboard_settings

    @staticmethod
    async def create_keyboard_back():
        """Метод для создания клавиатуры, состоящей из кнопки back"""
        keyboard_back = await ButtonsCreate.create_one(button_one=texts.back, button_back=None)
        return keyboard_back

    @staticmethod
    async def create_district_edit():
        """Метод для создания клавиатуры для редактирования выбора района города"""
        keyboard_district_edit = await ButtonsCreate.create_inline_keyboard(width=2,
                                                                            buttons_dict=texts.district_choose_inline,
                                                                            button_back=texts.back)
        return keyboard_district_edit

    @staticmethod
    async def create_rooms_edit():
        """Метод для создания клавиатуры для редактирования выбора количества комнат"""
        keyboard_rooms_edit = await ButtonsCreate.create_inline_keyboard(width=3, buttons_dict=texts.rooms_inline,
                                                                         button_back=texts.back)
        return keyboard_rooms_edit


class KeyboardRunCreate:
    """Класс для создания клавиатуры для модуля Run"""
    @staticmethod
    async def keyboards_adv():
        """Метод для создания клавиатуры выпадающей с объявлением"""
        keyboards_adv = await ButtonsCreate.create_inline_keyboard(width=2, buttons_dict=texts.adv_buttons)
        return keyboards_adv

    @staticmethod
    async def keyboards_adv_more():
        """Метод для создания клавиатуры выпадающей с объявлением"""
        keyboards_adv_more = await ButtonsCreate.create_inline_keyboard(width=2, buttons_dict=texts.adv_buttons_more)
        return keyboards_adv_more

    @staticmethod
    async def keyboard_back():
        """Метод для создания клавиатуры, состоящей из кнопки back"""
        keyboard_back = await ButtonsCreate.create_one(button_one=texts.back, button_back=None)
        return keyboard_back

