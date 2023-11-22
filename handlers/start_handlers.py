from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from database.inserts import insert_new_entry
from utils import texts
from my_keyboards.__init__ import create_one
from states.states import AlSettings


router = Router()

"""Глобальные переменные кнопок для удобства внесения изменений"""
keyboard_start_search = create_one(button_one=texts.first)
keyboard_repeat_start_search = create_one(width=2, button_one=texts.first_keyboard, button_back=texts.back)


@router.message(StateFilter(None), CommandStart)
async def start_handler(message: Message, state: FSMContext):
    """Стартовый handler с внесением в базу данных пользователя, нажавшего старт"""
    entry_insert_or_no = await insert_new_entry(message.from_user.id, message.from_user.username)
    if entry_insert_or_no:
        await message.answer(f'{entry_insert_or_no}, желаете обновить настройки поиска квартиры?',
                             reply_markup=keyboard_repeat_start_search)
    else:
        await message.answer(texts.wellcome_text.format(name=message.from_user.full_name),
                             reply_markup=keyboard_start_search)

    await state.set_state(AlSettings.start)


@router.callback_query(StateFilter(AlSettings.settings), F.data == '/back')
@router.callback_query(StateFilter(AlSettings.metro), F.data == '/back')
async def start_settings(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f'Вы вернулись в начало', reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.start)

# @router.callback_query(StateFilter(Navigation.menu), F.data == 'next')
# async def next_app(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(f'Далее')
#
#
# @router.callback_query(StateFilter(Navigation.menu), F.data == 'settings')
# async def settings_search(callback: CallbackQuery, state: FSMContext):
#     try:
#         await callback.message.edit_text('Изменить параметры поиска', reply_markup=keyboard_inline)
#     except TelegramBadRequest:
#         await callback.answer('Можете изменить параметры')
#
#
# @router.callback_query(StateFilter(Navigation.menu), F.data == 'support')
# async def support_msg(callback: CallbackQuery, state: FSMContext):
#     try:
#         await callback.message.answer('Введите сообщение(будет отправлено модератору)')
#     except TelegramBadRequest:
#         await callback.answer('Напишите и отправьте сообщение')
#
#
# @router.callback_query(StateFilter(Navigation.menu), F.data == 'about')
# async def about_bot(callback: CallbackQuery, state: FSMContext):
#     try:
#         await callback.message.edit_text('Дипломная работа школы skillbox')
#     except TelegramBadRequest:
#         await callback.answer('Разработчик: Ангархаев Москвин')
