from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def create_key(width: int, *args: str, **kwargs: str):
    """Создание произвольного количества кнопок"""
    settings: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))

    if kwargs:
        for key, button in kwargs.items():
            buttons.append(KeyboardButton(text=button))

    settings.row(*buttons, width=width)
    return settings.as_markup()
