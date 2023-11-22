from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from database.inserts import insert_new_entry
from utils import texts
from my_keyboards.__init__ import create_one, create_inline_keyboard, create_reply
from states.states import AlSettings
from database.my_connect import create_connection
from database.update_entry import check_settings, update_low, select_data_settings
from config_data.config import db_host, db_user_name, db_password, db_db_name


router_settings = Router()


keyboard_start_search = create_one(button_one=texts.first)
keyboard_settings = create_inline_keyboard(width=1, buttons_dict=texts.params_inline, button_back=texts.back)
keyboard_back = create_one(button_one=texts.back, button_back=None)
keyboard_district = create_inline_keyboard(width=2, buttons_dict=texts.district_choose_inline, button_back=texts.back)
keyboard_rooms = create_inline_keyboard(width=3, buttons_dict=texts.rooms_inline, button_back=texts.back)
keyboards_swipe = create_reply(width=1, buttons_dict=texts.swipe)


@router_settings.callback_query(StateFilter(AlSettings.update_min, AlSettings.update_max,
                                            AlSettings.update_rooms, AlSettings.update_disrict), F.data == '/back')
@router_settings.callback_query(StateFilter(AlSettings.start), F.data == '/settings')
async def new_settings(callback: CallbackQuery, state: FSMContext):
    """Функция для редактирования параметров поиска"""
    await callback.message.delete()
    settings_check = await check_settings(callback.from_user.id)
    if settings_check:
        await callback.message.answer('Выберите параметр для редактирования', reply_markup=keyboard_settings)
    else:
        await callback.message.answer('Пора приступить к поиску квартиры!', reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.update)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/metro')
async def update_metro(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Выберите район', reply_markup=keyboard_district)
    await state.set_state(AlSettings.update_disrict)

@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/low_price')
async def update_low_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data_settings = await select_data_settings(callback.from_user.id)
    await callback.message.answer(f"Ваша текущая нижняя граница: "
                                  f"{data_settings['low_price']}")
    await callback.message.answer(f"Укажите нижнюю границу не менее 1000 рублей, но меньше "
                                  f"верхней границы поиска: {data_settings['high_price']}",
                                  reply_markup=keyboard_back)
    await state.set_state(AlSettings.update_min)


@router_settings.message(StateFilter(AlSettings.update_min))


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/high_price')
async def update_high_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите верхнюю границу ниже 100000, но выше нижней границы поиска:')

@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/rooms')
async def update_rooms(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Отлично! Сколько комнат должно быть в квартире?', reply_markup=keyboard_rooms)
    await state.set_state(AlSettings.pre_update)
# bot.send_message(id, '<a href="IMG_URL">&#8203;</a>', parse_mode="HTML")