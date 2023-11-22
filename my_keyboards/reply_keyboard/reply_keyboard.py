from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def create_reply(width: int, buttons_dict:  dict[str, int: str, int]):
    """Создание произвольного количества кнопок"""
    settings: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []

    for key, button in buttons_dict.items():
        buttons.append(KeyboardButton(text=button, callback_data=key))

    settings.row(*buttons, width=width)
    return settings.as_markup()
