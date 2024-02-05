from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils import texts, EasyFunc
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest
import random
from database import DatabaseCommands
from my_keyboards import KeyboardsCreateSearchSettings

"""Инициализация роутера для работы с хэндлерами настроек поиска"""
router_search = Router()


@router_search.callback_query(StateFilter(AlSettings.min_price), F.data == '/back')
@router_search.callback_query(StateFilter(AlSettings.start, AlSettings.update), F.data == '/start_s_a')
async def settings(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий на кнопку "Задать параметры поиска", перенаправляющий на выбор района города"""
    num_lets_go = random.randint(1, 7)
    user_keyboard_district = await KeyboardsCreateSearchSettings.create_district()
    await state.update_data(user_keyboard_district=user_keyboard_district)
    await callback.message.delete()
    await callback.message.answer(texts.text_for_not_start[num_lets_go])
    await callback.message.answer('Выберите район',
                                  reply_markup=user_keyboard_district)
    await state.set_state(AlSettings.metro)


@router_search.message(StateFilter(AlSettings.metro))
async def no_write_pls(message: Message, state: FSMContext):
    """Handler, срабатывающий при попытке ввести текст, вместо выбора района"""
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Выберите, пожалуйста, район города!',
                             reply_markup=get_keyboards['user_keyboard_district'])
        await state.set_state(AlSettings.metro)


@router_search.callback_query(StateFilter(AlSettings.metro), F.data.in_(texts.district_choose_inline))
async def districts(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий на выбор района города и перенаправляющий в указание нижней границы"""
    user_keyboard_back = await KeyboardsCreateSearchSettings.create_keyboard_back()
    await state.update_data(user_keyboard_back=user_keyboard_back)
    district_const = texts.district_choose_inline[callback.data]
    await state.update_data(district=district_const)
    await callback.message.delete()
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgIAAxkBAAEKz7VlYNhxT-aa5fm8AY7ALiAAAZwn3uUAAlinAAJji0YMwxSGg7Sx8SEzBA')
    await callback.message.answer('Укажите нижнюю границу цены:',
                                  reply_markup=user_keyboard_back)
    await state.set_state(AlSettings.min_price)


@router_search.callback_query(StateFilter(AlSettings.max_price), F.data == '/back')
async def districts_without_update_dict(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий при нажатии кнопки назад без обновления словаря(добавление района города)"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    await callback.message.answer('Укажите нижнюю границу цены:',
                                  reply_markup=get_keyboards['user_keyboard_back'])
    await state.set_state(AlSettings.min_price)


@router_search.message(StateFilter(AlSettings.min_price), F.text.isdigit(), lambda m: 80000 > int(m.text) > 999)
async def low(message: Message, state: FSMContext):
    """Handler для указания верхней границы поиска и обновлением словаря(добавление нижней границы)"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await state.update_data(low=message.text)
        get_dict = await state.get_data()
        await message.answer('Отлично! Теперь укажите верхнюю границу поиска:',
                             reply_markup=get_dict['user_keyboard_back'])
        await state.set_state(AlSettings.max_price)


@router_search.callback_query(StateFilter(AlSettings.amount_rooms), F.data == '/back')
async def low__without_update_dict(callback: CallbackQuery, state: FSMContext):
    """Handler, срабатывающий при нажатии кнопки "Назад" для указания верхней границы
    без обновления словаря с информацией для поиска"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    await callback.message.answer('Укажите верхнюю границу поиска:',
                                  reply_markup=get_keyboards['user_keyboard_back'])
    await state.set_state(AlSettings.max_price)


@router_search.message(StateFilter(AlSettings.min_price))
async def low_filter(message: Message, state: FSMContext):
    """
    Handler, который отлавливает значения, содержащее буквы и прочие символы для указания
    нижней границы поиска
    """
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz79lYNnjlF-eeTwDExOnBJta1VsnDQAChQEAAiteUwuroLLCvfR5lzME')
        await message.answer('Нижняя граница должна быть цифровым значением (без букв и пробелов) '
                             'и больше, чем 999. Например 1000', reply_markup=get_keyboards['user_keyboard_back'])
        await state.set_state(AlSettings.min_price)


@router_search.message(StateFilter(AlSettings.max_price), F.text.isdigit(),
                       lambda m: 100001 > int(m.text))
@EasyFunc.custom_message_filter_search_settings_high()
async def high(message: Message, state: FSMContext):
    """Handler, перенаправляющий на указание количества комнат в квартире
    и с сохранением в словаре верхней границы поиска"""
    user_keyboard_rooms = await KeyboardsCreateSearchSettings.create_rooms()
    await state.update_data(user_keyboard_rooms=user_keyboard_rooms)
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz8FlYNojVtqQblXhkWCm1pdbSBRQ7AACgwMAAm2wQgMpslbTaPw4PjME')
        await message.answer('Отлично! Сколько комнат должно быть в квартире?',
                             reply_markup=user_keyboard_rooms)
        await state.update_data(high=message.text)
        await state.set_state(AlSettings.amount_rooms)


@router_search.message(StateFilter(AlSettings.max_price))
async def high_filter(message: Message, state: FSMContext):
    """Handler, который отлавливает значения, содержащее буквы и прочие символы для указания
    нижней границы поиска"""
    get_dict = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer(f"Верхняя граница должна быть цифровым значением (без букв и пробелов). "
                             f"Меньше чем 100000 и не меньше, чем нижняя граница {int(get_dict['low'])}",
                             reply_markup=get_dict['user_keyboard_back'])
        await state.set_state(AlSettings.max_price)


@router_search.message(StateFilter(AlSettings.amount_rooms))
async def no_write_pls_choice_rooms(message: Message, state: FSMContext):
    """Handler, срабатывающий при попытке ввести текст, вместо выбора количества комнат.
    Без сохранения результатов верхней границы (уже сохранено)"""
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Выберите, пожалуйста, один из вариантов',
                             reply_markup=get_keyboards['user_keyboard_rooms'])
        await state.set_state(AlSettings.amount_rooms)


@router_search.callback_query(StateFilter(AlSettings.amount_rooms), F.data.in_(texts.rooms_inline))
async def rooms_and_to_database(callback: CallbackQuery, state: FSMContext):
    """Handler для сохранения количества комнат в квартире и вывода параметров поиска"""
    user_keyboard_swipe = await KeyboardsCreateSearchSettings.create_keyboard_swipe()
    rooms_const = texts.rooms_inline[callback.data]
    await state.update_data(rooms=rooms_const)
    await callback.message.delete()
    user_dict = await state.get_data()
    await callback.message.answer(
        f"Вы уже почти стали арендатором! Смотрим варианты?:\n"
        f"Район города: {user_dict['district']}\n"
        f"Ценовой диапазон: {user_dict['low']}"
        f"-{user_dict['high']}\n"
        f"Количество комнат: {user_dict['rooms']}",
        reply_markup=user_keyboard_swipe
    )
    await DatabaseCommands.insert_settings(
        tg_id=callback.from_user.id,
        district=user_dict["district"],
        rooms=user_dict["rooms"],
        low_price=user_dict["low"],
        high_price=user_dict["high"]
    )

    await state.set_state(AlSettings.finish_start_settings)
