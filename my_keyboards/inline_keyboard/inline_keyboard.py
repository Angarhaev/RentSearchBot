from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_one(button_one: dict[str, int: str, int]):
    """Функция для создания одинокой произвольной кнопки"""
    back_button_keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for key, button in button_one.items():
        buttons.append(InlineKeyboardButton(text=button, callback_data=key))

    back_button_keyboard.row(*buttons, width=1)
    return back_button_keyboard.as_markup()


def button_back_add(button_back: dict[str, int: str, int]):
    """Функция кнопки дополнительной кнопки "Назад" для клавиатуры"""
    if button_back:
        for key, button in button_back.items():
            kb_button_back = InlineKeyboardButton(text=button, callback_data=key)
            return kb_button_back
    else:
        return None


def create_inline_keyboard(width: int, buttons_dict: dict[str, int: str, int],
                           button_back: dict[str, int: str, int] = None):
    """Функция для создания произвольного количества кнопок с возможностью наличия
    кнопки "Назад" при явном указании"""
    rooms_menu: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for key, button in buttons_dict.items():
        buttons.append(InlineKeyboardButton(text=button, callback_data=key))

    rooms_menu.row(*buttons, width=width)

    kb_button_back = button_back_add(button_back)
    if kb_button_back:
        rooms_menu.row(kb_button_back)

    return rooms_menu.as_markup()
