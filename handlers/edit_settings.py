from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from utils import texts
from utils.easy_funcs import EasyFunc
from states.states import AlSettings
from database import DatabaseCommands
from my_keyboards import KeyboardEditCreate, ReplyKeyboardCreate


router_settings = Router()


@router_settings.message(StateFilter(AlSettings.update_min, AlSettings.update_max, AlSettings.start,
                                     AlSettings.update_rooms, AlSettings.update_district,
                                     AlSettings.update_finish, AlSettings.user_settings, AlSettings.adv_showed,
                                     AlSettings.finish_start_settings, None
                                     ),
                         F.text == '/edit_settings')
async def edit_from_message(message: Message, state: FSMContext):
    """Функция для редактирования параметров поиска"""
    keyboard_settings = await KeyboardEditCreate.create_settings()
    keyboard_start_search = await KeyboardEditCreate.create_start_search()
    keyboard_back = await KeyboardEditCreate.create_keyboard_back()
    keyboard_district = await KeyboardEditCreate.create_district_edit()
    keyboard_rooms = await KeyboardEditCreate.create_rooms_edit()
    keyboard_swipe = await ReplyKeyboardCreate.create_keyboard_swipe()
    await state.update_data(keyboard_settings=keyboard_settings)
    await state.update_data(keyboard_start_search=keyboard_start_search)
    await state.update_data(keyboard_back=keyboard_back)
    await state.update_data(keyboard_district=keyboard_district)
    await state.update_data(keyboard_rooms=keyboard_rooms)
    await state.update_data(keyboard_swipe=keyboard_swipe)
    settings_check = await DatabaseCommands.select_settings_user(message.from_user.id)
    if settings_check:
        await message.answer('Выберите параметр для редактирования', reply_markup=keyboard_settings)
    else:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz8tlYNy5tQFhhaLUUPpjZIlAA0TBZwACPgMAArrAlQXle8BoEhO0GDME')
        await message.message.answer('Пора приступить к поиску квартиры!', reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.update)


@router_settings.callback_query(StateFilter(AlSettings.update_min, AlSettings.update_max,
                                            AlSettings.update_rooms, AlSettings.update_district,
                                            AlSettings.update_finish, AlSettings.user_settings, AlSettings.adv_showed),
                                F.data == '/back')
@router_settings.callback_query(StateFilter(AlSettings.start, AlSettings.adv_showed), F.data == '/settings')
async def new_settings(callback: CallbackQuery, state: FSMContext):
    """Функция для редактирования параметров поиска"""
    keyboard_settings = await KeyboardEditCreate.create_settings()
    keyboard_start_search = await KeyboardEditCreate.create_start_search()
    keyboard_back = await KeyboardEditCreate.create_keyboard_back()
    keyboard_district = await KeyboardEditCreate.create_district_edit()
    keyboard_rooms = await KeyboardEditCreate.create_rooms_edit()
    keyboard_swipe = await ReplyKeyboardCreate.create_keyboard_swipe()
    await state.update_data(keyboard_settings=keyboard_settings)
    await state.update_data(keyboard_start_search=keyboard_start_search)
    await state.update_data(keyboard_back=keyboard_back)
    await state.update_data(keyboard_district=keyboard_district)
    await state.update_data(keyboard_rooms=keyboard_rooms)
    await state.update_data(keyboard_swipe=keyboard_swipe)
    await callback.message.delete()
    settings_check = await DatabaseCommands.select_settings_user(callback.from_user.id)
    if settings_check:
        await callback.message.answer('Выберите параметр для редактирования', reply_markup=keyboard_settings)
    else:
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz8tlYNy5tQFhhaLUUPpjZIlAA0TBZwACPgMAArrAlQXle8BoEhO0GDME')
        await callback.message.answer('Пора приступить к поиску квартиры!', reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.update)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/user_settings')
async def show_user_settings(callback: CallbackQuery, state: FSMContext):
    """Функция для просмотра текущих настроек поиска из базы данных"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    user_setting = await DatabaseCommands.select_settings_user(callback.from_user.id)
    await callback.message.answer(
                                f"Район города: {user_setting[0].district}\n"
                                f"Нижняя граница цены: {user_setting[0].low_price}\n"
                                f"Верхняя граница цены:{user_setting[0].high_price}\n"
                                f"Количество комнат: {user_setting[0].rooms}",
                                reply_markup=get_keyboards['keyboard_back'])
    await state.set_state(AlSettings.user_settings)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/metro')
async def update_metro(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'Район города'"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    await callback.message.answer('Выберите район',
                                  reply_markup=get_keyboards['keyboard_district'])
    await state.set_state(AlSettings.update_district)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/rooms')
async def update_rooms(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'Количество комнат'"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    await callback.message.answer('Отлично! Сколько комнат должно быть в квартире?',
                                  reply_markup=get_keyboards['keyboard_rooms'])
    await state.set_state(AlSettings.update_rooms)


@router_settings.callback_query(StateFilter(AlSettings.update_district), F.data.in_(texts.district_choose_inline))
async def update_finish_callback(callback: CallbackQuery, state: FSMContext):
    """Функция для добавления изменений параметров 'Район города' в базу данных"""
    await callback.message.delete()
    get_keyboards = await state.get_data()
    try:
        district_const = texts.district_choose_inline[callback.data]
        await DatabaseCommands.update_district(callback.from_user.id, district_const)
        await callback.message.answer(f'Данные успешно обновлены.\nТекущий выбранный район: {district_const}',
                                      reply_markup=get_keyboards['keyboard_back'])
        await state.set_state(AlSettings.update_finish)
    except Exception as exc:
        await callback.message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
        print('Ошибка:', exc)


@router_settings.callback_query(StateFilter(AlSettings.update_rooms), F.data.in_(texts.rooms_inline))
async def update_finish_callback(callback: CallbackQuery, state: FSMContext):
    """Функция для добавления изменений параметров 'Количество комнат' в базу данных"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    try:
        rooms_const = texts.rooms_inline[callback.data]
        await DatabaseCommands.update_rooms(callback.from_user.id, rooms_const)
        await callback.message.answer(f'Данные успешно обновлены. Текущее выбранное количество комнат: '
                                      f'{rooms_const}', reply_markup=get_keyboards['keyboard_back'])
        await state.set_state(AlSettings.update_finish)
    except Exception as exc:
        await callback.message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
        print('Ошибка:', exc)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/low_price')
async def update_low_price(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'нижняя граница'"""
    get_keyboards = await state.get_data()
    await callback.message.delete()
    user_dict_set = await DatabaseCommands.select_settings_user(callback.from_user.id)
    await state.update_data(user_dict_set=user_dict_set)
    await callback.message.answer(f"Ваша текущая нижняя граница: "
                                  f"{user_dict_set[0].low_price}\n"
                                  f"Укажите нижнюю границу не менее 1000 рублей, но меньше "
                                  f"верхней границы поиска: {user_dict_set[0].high_price}",
                                  reply_markup=get_keyboards['keyboard_back'])
    await state.set_state(AlSettings.update_min)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/high_price')
async def update_high_price(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'верхняя граница'"""
    get_dict = await state.get_data()
    await callback.message.delete()
    user_dict_set = await DatabaseCommands.select_settings_user(callback.from_user.id)
    await state.update_data(user_dict_set=user_dict_set)
    print(user_dict_set)
    await callback.message.answer(f"Ваша текущая верхняя граница: "
                                  f"{user_dict_set[0].high_price}\n"
                                  f"Укажите верхнюю границу не меньше нижней "
                                  f"{user_dict_set[0].low_price}, но меньше 100000",
                                  reply_markup=get_dict['keyboard_back'])
    await state.set_state(AlSettings.update_max)


@router_settings.message(StateFilter(AlSettings.update_min), F.text != "🏠", F.text != "/swipe", F.text.isdigit(),
                         lambda m: 999 < int(m.text))
@EasyFunc.custom_message_filter_edit_settings_low()
async def update_finish_min(message: Message, state: FSMContext):
    """Функция для добавления изменений нижней границы в базу данных"""
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        try:
            await DatabaseCommands.update_low_price(message.from_user.id, message.text)
            await message.answer(f'Данные успешно обновлены.\nТекущая нижняя граница: {message.text}',
                                 reply_markup=get_keyboards['keyboard_back'])
            await state.set_state(AlSettings.update_finish)
        except Exception as exc:
            await message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
            print('Ошибка:', exc)


@router_settings.message(StateFilter(AlSettings.update_max), F.text != "🏠", F.text != "/swipe", F.text.isdigit(),
                         lambda m: int(m.text) < 100001)
@EasyFunc.custom_message_filter_edit_settings_high()
async def update_finish_max(message: Message, state: FSMContext):
    """Функция для добавления изменений верхней границы в базу данных"""
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        try:
            await DatabaseCommands.update_high_price(message.from_user.id, message.text)
            await message.answer(f'Данные успешно обновлены.\nТекущая верхняя граница: {message.text}',
                                 reply_markup=get_keyboards['keyboard_back'])
            await state.set_state(AlSettings.update_finish)
        except Exception as exc:
            await message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
            print('Ошибка:', exc)


@router_settings.message(StateFilter(AlSettings.update_min), F.text != "🏠", F.text != "/swipe")
async def error_min_price(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    get_dict = await state.get_data()
    user_dict_set = get_dict['user_dict_set']
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer(f"Неверно указан параметр 'Нижняя граница': {message.text}. "
                             f"Внимательно посмотрите диапазон значений: \n"
                             f"Ваша текущая нижняя граница: {user_dict_set[0].low_price}\n"
                             f"Ваша текущая верхняя граница: {user_dict_set[0].high_price}\n"
                             f"Выберите параметр для редактирования или начните поиск:",
                             reply_markup=get_dict['keyboard_settings'])
        await state.set_state(AlSettings.update)


@router_settings.message(StateFilter(AlSettings.update_max), F.text != "🏠", F.text != "/swipe",
                         F.text != '/edit_settings')
async def error_max_price(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    get_dict = await state.get_data()
    user_dict_set = get_dict['user_dict_set']
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer(f"Неверно указан параметр 'Верхняя граница': {message.text}. "
                             f"Внимательно посмотрите диапазон значений: \n"
                             f"Ваша текущая нижняя граница: {user_dict_set[0].low_price}\n"
                             f"Ваша текущая верхняя граница: {user_dict_set[0].high_price}\n"
                             f"Выберите параметр для редактирования или начните поиск:",
                             reply_markup=get_dict['keyboard_settings'])
        await state.set_state(AlSettings.update)


@router_settings.message(StateFilter(AlSettings.update_district, AlSettings.update_rooms, AlSettings.update),
                         F.text != "🏠", F.text != "/swipe", F.text != '/edit_settings')
async def error_rooms_district(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    get_keyboards = await state.get_data()
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.answer('Пожалуйста, воспользуйтесь клавиатурой:',
                             reply_markup=get_keyboards['keyboard_settings'])
        await state.set_state(AlSettings.update)
