from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from database import Requests, insert_new_entry
from states.states import AlSettings
from utils import texts
from my_keyboards import create_one
from aiogram.exceptions import TelegramBadRequest


router_echo = Router()

"""Глобальные переменные кнопок для удобства внесения изменений"""
keyboard_start_search = create_one(button_one=texts.first)
keyboard_repeat_start_search = create_one(width=2, button_one=texts.again_keyboard, button_back=texts.back)


@router_echo.message(StateFilter(None))
async def echo_mes(message: Message, state: FSMContext):
    """Функция для ловли эхо и перенаправлении в начало"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        entry_insert_or_no = await insert_new_entry(message.from_user.id, message.from_user.username)
        if entry_insert_or_no:
            await message.answer(f'{message.from_user.first_name}, желаете обновить настройки поиска квартиры?',
                                 reply_markup=keyboard_repeat_start_search)
        else:
            await message.answer(texts.wellcome_text.format(name=message.from_user.full_name),
                                 reply_markup=keyboard_start_search)

        await state.set_state(AlSettings.start)


@router_echo.callback_query(StateFilter(None), F.data.in_(texts.all_buttons))
async def echo_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    entry_insert_or_no = await Requests.insert_entry(callback.from_user.id, callback.from_user.username)
    if entry_insert_or_no:
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz6llYNDvOb2kfDYQrXqb-GF-6jQrlQACTKcAAmOLRgwvLC3Va72R7TME')
        await callback.message.answer(texts.wellcome_text.format(name=callback.from_user.full_name),
                                      reply_markup=keyboard_start_search)

    else:
        await callback.message.answer('Потеряно соединение с сервером... Попробуйте снова!')
        settings_check = await Requests.check_settings(callback.from_user.id)
        if settings_check:
            await callback.message.answer(f'{callback.from_user.first_name}, начнем с начала',
                                          reply_markup=keyboard_repeat_start_search)
        else:
            await callback.message.answer(f'{callback.from_user.first_name}, начнем с начала. ',
                                          reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.start)
