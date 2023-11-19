from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils import texts
from my_keyboards.__init__ import create_inline_keyboard, create_one
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest
import random
from database.inserts import insert_settings


router_search = Router()

"""Глобальные переменные кнопок для удобства внесения изменений"""
keyboard_back = create_one(texts.back)
keyboard_district = create_inline_keyboard(width=2, buttons_dict=texts.district_choose_inline, button_back=None)
keyboard_rooms = create_inline_keyboard(width=3, buttons_dict=texts.rooms_inline, button_back=texts.back)


"""Словарь для параметров поиска и внесения настроек в базу данных"""
user_dict: dict[int, dict[str]] = {}


@router_search.callback_query(StateFilter(AlSettings.min_price), F.data == '/back')
@router_search.callback_query(StateFilter(AlSettings.start), F.data == '/start_s_a')
async def settings(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий на кнопку "Задать параметры поиска", перенаправляющий на выбор района города"""
    #добавить условие: если есть в базе - очистить избранное?
    num_lets_go = random.randint(1, 7)
    await callback.message.delete()
    await callback.message.answer(texts.text_for_not_start[num_lets_go])
    await callback.message.answer('Выберите район', reply_markup=keyboard_district)
    await state.set_state(AlSettings.metro)


@router_search.message(StateFilter(AlSettings.metro))
async def no_write_pls(message: Message, state: FSMContext):
    """Handler, срабатывающий при попытке ввести текст, вместо выбора района"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Выберите, пожалуйста, район города!', reply_markup=keyboard_back)
        await state.set_state(AlSettings.metro)


@router_search.callback_query(StateFilter(AlSettings.metro), F.data.in_(texts.district_choose_inline))
async def districts(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий на выбор района города и перенаправляющий в указание нижней границы"""
    district_const = texts.district_choose_inline[callback.data]
    await state.update_data(district=district_const)
    await callback.message.delete()
    await callback.message.answer('Укажите нижнюю границу цены:', reply_markup=keyboard_back)
    await state.set_state(AlSettings.min_price)


@router_search.callback_query(StateFilter(AlSettings.max_price), F.data == '/back')
async def districts_without_update_dict(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий при нажатии кнопки назад без обновления словаря(добавление района города)"""
    await callback.message.delete()
    await callback.message.answer('Укажите нижнюю границу цены:', reply_markup=keyboard_back)
    await state.set_state(AlSettings.min_price)


@router_search.message(StateFilter(AlSettings.min_price),  F.text.isdigit(), lambda m: int(m.text) > 999)
async def low(message: Message, state: FSMContext):
    """Handler для указания верхней границы поиска и обновлением словаря(добавление нижней границы)"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await state.update_data(low=message.text)
        user_dict[message.from_user.id] = await state.get_data()
        await message.answer('Отлично! Теперь укажите верхнюю границу поиска:', reply_markup=keyboard_back)
        await state.set_state(AlSettings.max_price)


@router_search.callback_query(StateFilter(AlSettings.amount_rooms), F.data == '/back')
async def low__without_update_dict(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий при нажатии кнопки "Назад" для указания верхней границы
    без обновления словаря с информацией для поиска"""
    await callback.message.delete()
    await callback.message.answer('Укажите верхнюю границу поиска:', reply_markup=keyboard_back)
    await state.set_state(AlSettings.max_price)


@router_search.message(StateFilter(AlSettings.min_price))
async def low_filter(message: Message, state: FSMContext):
    """
    Handler, который отлавливает значения, содержащее буквы и прочие символы для указания
    нижней границы поиска
    """
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Нижняя граница должна быть цифровым значением (без букв и пробелов) '
                             'и больше, чем 999. Например 1000', reply_markup=keyboard_back)
        await state.set_state(AlSettings.min_price)


@router_search.message(StateFilter(AlSettings.max_price), F.text.isdigit(),
                       lambda m: 100001 > int(m.text) > int(user_dict[m.from_user.id]['low']))
async def high(message: Message, state: FSMContext):
    """Handler, перенаправляющий на указание количества комнат в квартире
    и с сохранением в словаре верхней границы поиска"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Отлично! Сколько комнат должно быть в квартире?', reply_markup=keyboard_rooms)
        await state.update_data(high=message.text)
        await state.set_state(AlSettings.amount_rooms)


@router_search.message(StateFilter(AlSettings.max_price))
async def high_filter(message: Message, state: FSMContext):
    """Handler, который отлавливает значения, содержащее буквы и прочие символы для указания
    нижней границы поиска"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer(f"Верхняя граница должна быть цифровым значением (без букв и пробелов). "
                             f"Меньше чем 100000 и меньше, чем {int(user_dict[message.from_user.id]['low'])}",
                             reply_markup=keyboard_back)
        await state.set_state(AlSettings.max_price)


@router_search.message(StateFilter(AlSettings.swipe))
async def no_write_pls_choice_rooms(message: Message, state: FSMContext):
    """Handler, срабатывающий при попытке ввести текст, вместо выбора количества комнат.
    Без сохранения результатов верхней границы (уже сохранено)"""
    await message.answer('Нажми кнопку д####еб', reply_markup=keyboard_rooms)
    await state.set_state(AlSettings.amount_rooms)


@router_search.callback_query(StateFilter(AlSettings.amount_rooms), F.data.in_(texts.rooms_inline))
async def rooms_and_to_database(callback: CallbackQuery, state: FSMContext):
    """Handler для сохранения количества комнат в квартире и вывода параметров поиска"""
    rooms_const = texts.rooms_inline[callback.data]
    await state.update_data(rooms=rooms_const)
    await callback.message.delete()
    user_dict[callback.from_user.id] = await state.get_data()
    await callback.message.answer(f"Район города: {user_dict[callback.from_user.id]['district']}\n"
                                  f"Ценовой диапазон: {user_dict[callback.from_user.id]['low']}"
                                  f"-{user_dict[callback.from_user.id]['high']}\n"
                                  f"Количество комнат: {user_dict[callback.from_user.id]['rooms']}")
    await insert_settings(callback.from_user.id, user_dict[callback.from_user.id]['district'], user_dict[callback.from_user.id]['rooms'],
                          user_dict[callback.from_user.id]['low'], user_dict[callback.from_user.id]['high'])
    await state.set_state(AlSettings.swipe)

@router_search.callback_query(StateFilter(AlSettings.swipe))
async def rooms_and_to_database(callback: CallbackQuery, state: FSMContext):
    pass