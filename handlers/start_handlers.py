from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils import texts
from my_keyboards import create_one
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest
from database import Requests


router = Router()

"""Глобальные переменные клавиатуры"""
keyboard_start_search = create_one(button_one=texts.first)
keyboard_repeat_start_search = create_one(width=2, button_one=texts.again_keyboard, button_back=texts.back)


@router.message(StateFilter(None), CommandStart)
async def start_handler(message: Message, state: FSMContext):
    """Стартовый handler с внесением в базу данных пользователя, нажавшего старт"""
    entry_insert_or_no = await Requests.insert_entry(message.from_user.id, message.from_user.username,
                                                     message.from_user.full_name)
    if entry_insert_or_no:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz6llYNDvOb2kfDYQrXqb-GF-6jQrlQACTKcAAmOLRgwvLC3Va72R7TME')
        await message.answer(texts.wellcome_text.format(name=message.from_user.full_name),
                             reply_markup=keyboard_start_search)
    else:
        try:
            for i in range(message.message_id, 0, -1):
                await message.bot.delete_message(message.from_user.id, i)
        except TelegramBadRequest:
            await message.answer(f'{message.from_user.first_name}, желаете обновить настройки поиска квартиры?',
                                 reply_markup=keyboard_repeat_start_search)
    await state.set_state(AlSettings.start)


@router.callback_query(StateFilter(AlSettings.metro, AlSettings.settings,
                                   AlSettings.update, AlSettings.start), F.data == '/back', CommandStart)
async def start_settings(callback: CallbackQuery, state: FSMContext):
    entry_insert_or_no = await Requests.insert_entry(callback.from_user.id, callback.message.from_user.username,
                                                     callback.from_user.full_name)
    if entry_insert_or_no:
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz6llYNDvOb2kfDYQrXqb-GF-6jQrlQACTKcAAmOLRgwvLC3Va72R7TME')
        await callback.message.answer(texts.wellcome_text.format(name=callback.from_user.full_name),
                                      reply_markup=keyboard_start_search)
    else:
        await callback.message.delete()
        settings_check = await Requests.check_settings(callback.from_user.id)
        if settings_check:
            await callback.message.answer(f'{callback.from_user.first_name}, вы вернулись в начало. '
                                          f'Желаете обновить настройки поиска? ', reply_markup=keyboard_repeat_start_search)
        else:
            await callback.message.answer(f'{callback.from_user.first_name}, вы вернулись в начало. ',
                                          reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.start)


@router.message(StateFilter(AlSettings.start))
async def error_start(message: Message, state: FSMContext):
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        entry_insert_or_no = await Requests.insert_entry(message.from_user.id, message.from_user.username,
                                                         message.from_user.full_name)
        if entry_insert_or_no:
            await message.bot.send_sticker(chat_id=message.chat.id,
                                           sticker='CAACAgIAAxkBAAEKz7NlYNfpIrodmS_oSyG4xxFIa-34zgACVQADr8ZRGmTn_PAl6RC_MwQ')
            await message.answer(f'{message.from_user.first_name}, пора приступить к поиску квартиры!',
                                 reply_markup=keyboard_start_search)

        else:
            await message.answer(f'{message.from_user.first_name}, нажмите на одну из кнопок',
                                 reply_markup=keyboard_repeat_start_search)

        await state.set_state(AlSettings.start)
