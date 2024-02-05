from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils import texts


class ReplyButtonsCreate:
    """Класс для создания кнопок reply клавиатуры"""
    @staticmethod
    async def create_reply(width: int, buttons_dict:  dict[str, int: str, int]):
        """Создание произвольного количества кнопок"""
        settings: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

        buttons: list[KeyboardButton] = []

        for key, button in buttons_dict.items():
            buttons.append(KeyboardButton(text=button, callback_data=key))

        settings.row(*buttons, width=width)
        return settings.as_markup()


class ReplyKeyboardCreate:
    """Класс для создания reply клавиатуры"""
    @staticmethod
    async def create_keyboard_swipe():
        """Метод для создания кнопки swipe"""
        keyboard_swipe = await ReplyButtonsCreate.create_reply(width=1, buttons_dict=texts.swipe)
        return keyboard_swipe

