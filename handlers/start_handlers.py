from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils import texts
from my_keyboards import KeyboardsStartCreate, ReplyKeyboardCreate
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest
from database import DatabaseCommands


router = Router()


@router.message(StateFilter(None), F.text != '/edit_settings', F.text != "🏠", F.text != "/swipe", CommandStart)
async def start_handler(message: Message, state: FSMContext):
    """Стартовый handler с внесением в базу данных пользователя, нажавшего старт"""
    user_keyboard_repeat_start_search = await KeyboardsStartCreate.create_repeat_start_search()
    user_keyboard_start = await KeyboardsStartCreate.create_start_search()
    user_reply_swipe = await ReplyKeyboardCreate.create_keyboard_swipe()
    entry_insert_or_no = await DatabaseCommands.insert_user_start(message.from_user.id, message.from_user.username,
                                                                  message.from_user.full_name)
    if entry_insert_or_no:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz6llYNDvOb2kfDYQrXqb-GF-6jQrlQACTKcAAmOLRgwvLC3Va72R7TME',
                                       reply_markup=user_reply_swipe)
        await message.answer(texts.wellcome_text.format(name=message.from_user.full_name),
                             reply_markup=user_keyboard_start)
    else:
        await message.answer(f'{message.from_user.first_name}, желаете обновить настройки поиска квартиры?',
                             reply_markup=user_keyboard_repeat_start_search)
    await state.set_state(AlSettings.start)


@router.callback_query(StateFilter(AlSettings.metro, AlSettings.settings,
                                   AlSettings.update, AlSettings.start), F.data == '/back', CommandStart)
async def start_settings(callback: CallbackQuery, state: FSMContext):
    """Хэндлер для отлавливания колбэков при нажатии кнопки back из стартовых меню прочих модулей"""
    user_keyboard_start = await KeyboardsStartCreate.create_start_search()
    user_keyboard_repeat_start_search = await KeyboardsStartCreate.create_repeat_start_search()

    entry_insert_or_no = await DatabaseCommands.insert_user_start(callback.from_user.id, callback.message.from_user.username,
                                                                  callback.from_user.full_name)
    if entry_insert_or_no:
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz6llYNDvOb2kfDYQrXqb-GF-6jQrlQACTKcAAmOLRgwvLC3Va72R7TME')
        await callback.message.answer(texts.wellcome_text.format(name=callback.from_user.full_name),
                                      reply_markup=user_keyboard_start)
    else:
        await callback.message.delete()
        settings_check = await DatabaseCommands.select_settings_user(callback.from_user.id)
        if settings_check:
            await callback.message.answer(f'🏠', reply_markup=user_keyboard_repeat_start_search)
        else:
            await callback.message.answer(f'🏠',
                                          reply_markup=user_keyboard_start)
    await state.set_state(AlSettings.start)


@router.message(StateFilter(AlSettings.start), F.text != "🏠", F.text != "/swipe", F.text != '/edit_settings')
async def error_start(message: Message, state: FSMContext):
    """Хэндлер для отлавливания ввода с клавиатуры пользователя из стартового состояния"""
    user_keyboard_start = await KeyboardsStartCreate.create_start_search()
    user_keyboard_repeat_start_search = await KeyboardsStartCreate.create_repeat_start_search()
    entry_insert_or_no = await DatabaseCommands.insert_user_start(message.from_user.id, message.from_user.username,
                                                                  message.from_user.full_name)
    if entry_insert_or_no:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz7NlYNfpIrodmS_oSyG4xxFIa-34zgACVQADr8ZRGmTn_PAl6RC_MwQ')
        await message.answer(f'{message.from_user.first_name}, пора приступить к поиску квартиры!',
                             reply_markup=user_keyboard_start)

    else:
        await message.answer(f'{message.from_user.first_name}, нажмите на одну из кнопок',
                             reply_markup=user_keyboard_repeat_start_search)

    await state.set_state(AlSettings.start)
