from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from utils import texts
from my_keyboards import create_one, create_inline_keyboard, create_reply
from states.states import AlSettings
from database import (update_high_db, update_district_db, update_low_db, update_rooms_db, Requests)
import random


router_settings = Router()
user_dict_set: dict[int, dict[str]] = {}


keyboard_start_search = create_one(button_one=texts.first)
keyboard_settings = create_inline_keyboard(width=1, buttons_dict=texts.params_inline, button_back=texts.back)
keyboard_back = create_one(button_one=texts.back, button_back=None)
keyboard_district = create_inline_keyboard(width=2, buttons_dict=texts.district_choose_inline, button_back=texts.back)
keyboard_rooms = create_inline_keyboard(width=3, buttons_dict=texts.rooms_inline, button_back=texts.back)
keyboards_swipe = create_reply(width=1, buttons_dict=texts.swipe)


@router_settings.callback_query(StateFilter(AlSettings.update_min, AlSettings.update_max,
                                            AlSettings.update_rooms, AlSettings.update_district,
                                            AlSettings.update_finish, AlSettings.user_settings), F.data == '/back')
@router_settings.callback_query(StateFilter(AlSettings.start), F.data == '/settings')
async def new_settings(callback: CallbackQuery, state: FSMContext):
    """Функция для редактирования параметров поиска"""
    await callback.message.delete()
    settings_check = await Requests.check_settings(callback.from_user.id)
    if settings_check:
        choice_stick = random.randint(1, 9)
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker=texts.stick_in_edit_settings[choice_stick])
        await callback.message.answer('Выберите параметр для редактирования', reply_markup=keyboard_settings)
    else:
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz8tlYNy5tQFhhaLUUPpjZIlAA0TBZwACPgMAArrAlQXle8BoEhO0GDME')
        await callback.message.answer('Пора приступить к поиску квартиры!', reply_markup=keyboard_start_search)
    await state.set_state(AlSettings.update)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/user_settings')
async def show_user_settings(callback: CallbackQuery, state: FSMContext):
    """Функция для просмотра текущих настроек поиска из базы данных"""
    await callback.message.delete()
    user_setting = await Requests.check_settings(callback.from_user.id)
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgIAAxkBAAEKz9ZlYN1zv7mqjK0Z2Nu2xHMcnJLXpwACGwcAAoVBMhCl7D-zI1BPSjME')
    await callback.message.answer(
                                f"Район города: {user_setting['district']}\n"
                                f"Нижняя граница цены: {user_setting['low_price']}\n"
                                f"Верхняя граница цены:{user_setting['high_price']}\n"
                                f"Количество комнат: {user_setting['rooms']}",
                                reply_markup=keyboard_back)
    await state.set_state(AlSettings.user_settings)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/metro')
async def update_metro(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'Район города'"""
    await callback.message.delete()
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgIAAxkBAAEKz9xlYN3ulRMcGpM3OxnnoYEl1HLulQACYBYAAuwAAehKBQ_sZqpEeJUzBA')
    await callback.message.answer('Выберите район', reply_markup=keyboard_district)
    await state.set_state(AlSettings.update_district)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/rooms')
async def update_rooms(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'Количество комнат'"""
    await callback.message.delete()
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgIAAxkBAAEKz-JlYN6OVV_SMH6wHZs1ggGAXw9QqQACGAcAAoVBMhDJR5HP7c8lKzME')
    await callback.message.answer('Отлично! Сколько комнат должно быть в квартире?', reply_markup=keyboard_rooms)
    await state.set_state(AlSettings.update_rooms)


@router_settings.callback_query(StateFilter(AlSettings.update_district), F.data.in_(texts.district_choose_inline))
async def update_finish_callback(callback: CallbackQuery, state: FSMContext):
    """Функция для добавления изменений параметров 'Район города' в базу данных"""
    await callback.message.delete()
    try:
        district_const = texts.district_choose_inline[callback.data]
        await update_district_db(callback.from_user.id, district_const)
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz-RlYN6vrrFgDWrBBnGByiZut6AKSAACYwMAAm2wQgPhSS-1qxgIzDME')
        await callback.message.answer(f'Данные успешно обновлены.\nТекущий выбранный район: {district_const}',
                                      reply_markup=keyboard_back)
        await state.set_state(AlSettings.update_finish)
    except Exception as exc:
        await callback.message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
        print('Ошибка:', exc)


@router_settings.callback_query(StateFilter(AlSettings.update_rooms), F.data.in_(texts.rooms_inline))
async def update_finish_callback(callback: CallbackQuery, state: FSMContext):
    """Функция для добавления изменений параметров 'Количество комнат' в базу данных"""
    await callback.message.delete()
    try:
        rooms_const = texts.rooms_inline[callback.data]
        await update_rooms_db(callback.from_user.id, rooms_const)
        await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                        sticker='CAACAgIAAxkBAAEKz-RlYN6vrrFgDWrBBnGByiZut6AKSAACYwMAAm2wQgPhSS-1qxgIzDME')
        await callback.message.answer(f'Данные успешно обновлены. Текущее выбранное количество комнат: '
                                      f'{rooms_const}', reply_markup=keyboard_back)
        await state.set_state(AlSettings.update_finish)
    except Exception as exc:
        await callback.message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
        print('Ошибка:', exc)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/low_price')
async def update_low_price(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'нижняя граница'"""
    await callback.message.delete()
    user_dict_set[callback.from_user.id] = await Requests.check_settings(callback.from_user.id)
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgEAAxkBAAEKz-ZlYN77MJDQrzU6_7RsnBUhno3y8gACHQEAAjgOghHhhIkhaufuiTME')
    await callback.message.answer(f"Ваша текущая нижняя граница: "
                                  f"{user_dict_set[callback.from_user.id]['low_price']}\n"
                                  f"Укажите нижнюю границу не менее 1000 рублей, но меньше "
                                  f"верхней границы поиска: {user_dict_set[callback.from_user.id]['high_price']}",
                                  reply_markup=keyboard_back)
    await state.set_state(AlSettings.update_min)


@router_settings.callback_query(StateFilter(AlSettings.update), F.data == '/high_price')
async def update_high_price(callback: CallbackQuery, state: FSMContext):
    """Функция для изменения параметра 'верхняя граница'"""
    await callback.message.delete()
    user_dict_set[callback.from_user.id] = await Requests.check_settings(callback.from_user.id)
    await callback.bot.send_sticker(chat_id=callback.message.chat.id,
                                    sticker='CAACAgIAAxkBAAEKz-hlYN8dQoeIVTFeh9F8u6bHnD-A1wACfQMAAm2wQgO9Ey75tk26UzME')
    await callback.message.answer(f"Ваша текущая верхняя граница: "
                                  f"{user_dict_set[callback.from_user.id]['high_price']}\n"
                                  f"Укажите верхнюю границу не меньше нижней "
                                  f"{user_dict_set[callback.from_user.id]['low_price']}, но меньше 100000",
                                  reply_markup=keyboard_back)
    await state.set_state(AlSettings.update_max)


@router_settings.message(StateFilter(AlSettings.update_min), F.text.isdigit(),
                         lambda m: 999 < int(m.text) < user_dict_set[m.from_user.id]['high_price'])
async def update_finish_min(message: Message, state: FSMContext):
    """Функция для добавления изменений нижней границы в базу данных"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        try:
            await update_low_db(message.from_user.id, message.text)
            await message.bot.send_sticker(chat_id=message.chat.id,
                                           sticker='CAACAgIAAxkBAAEKz-RlYN6vrrFgDWrBBnGByiZut6AKSAACYwMAAm2wQgPhSS-1qxgIzDME')
            await message.answer(f'Данные успешно обновлены.\nТекущая нижняя граница: {message.text}',
                                 reply_markup=keyboard_back)
            await state.set_state(AlSettings.update_finish)
        except Exception as exc:
            await message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
            print('Ошибка:', exc)


@router_settings.message(StateFilter(AlSettings.update_max), F.text.isdigit(),
                         lambda m: user_dict_set[m.from_user.id]['low_price'] < int(m.text) < 100000)
async def update_finish_max(message: Message, state: FSMContext):
    """Функция для добавления изменений верхней границы в базу данных"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        try:
            await update_high_db(message.from_user.id, message.text)
            await message.bot.send_sticker(chat_id=message.chat.id,
                                           sticker='CAACAgIAAxkBAAEKz-RlYN6vrrFgDWrBBnGByiZut6AKSAACYwMAAm2wQgPhSS-1qxgIzDME')
            await message.answer(f'Данные успешно обновлены.\nТекущая верхняя граница: {message.text}',
                                 reply_markup=keyboard_back)
            await state.set_state(AlSettings.update_finish)
        except Exception as exc:
            await message.answer('Ошибка соединения с базой данных. Попробуйте еще раз')
            print('Ошибка:', exc)


@router_settings.message(StateFilter(AlSettings.update_min))
async def error_min_price(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz-plYN-maXTD8R8m3g1byrVLF7OCiAACHwcAAoVBMhAdNjqaDvbgqzME')
        await message.answer(f"Неверно указан параметр 'Нижняя граница': {message.text}. "
                             f"Внимательно посмотрите диапазон значений: \n"
                             f"Ваша текущая нижняя граница: {user_dict_set[message.from_user.id]['low_price']}\n"
                             f"Ваша текущая нижняя граница: {user_dict_set[message.from_user.id]['high_price']}\n"
                             f"Выберите параметр для редактирования или начните поиск:",
                             reply_markup=keyboard_settings)
        await state.set_state(AlSettings.update)


@router_settings.message(StateFilter(AlSettings.update_max))
async def error_max_price(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz-plYN-maXTD8R8m3g1byrVLF7OCiAACHwcAAoVBMhAdNjqaDvbgqzME')
        await message.answer(f"Неверно указан параметр 'Верхняя граница': {message.text}. "
                             f"Внимательно посмотрите диапазон значений: \n"
                             f"Ваша текущая нижняя граница: {user_dict_set[message.from_user.id]['low_price']}\n"
                             f"Ваша текущая нижняя граница: {user_dict_set[message.from_user.id]['high_price']}\n"
                             f"Выберите параметр для редактирования или начните поиск:",
                             reply_markup=keyboard_settings)
        await state.set_state(AlSettings.update)


@router_settings.message(StateFilter(AlSettings.update_district, AlSettings.update_rooms, AlSettings.update))
async def error_rooms_district(message: Message, state: FSMContext):
    """Функция для отлавливания некорректного ввода пользователя"""
    try:
        for i in range(message.message_id, 0, -1):
            await message.bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest:
        await message.bot.send_sticker(chat_id=message.chat.id,
                                       sticker='CAACAgIAAxkBAAEKz-xlYN_7gD_IKDz5oQpWPGHIwhMJsQACaQADwZxgDE4zEm9SERyMMwQ')
        await message.answer('Не пишите, пожалуйста, сообщение. Выберите один из вариантов:',
                             reply_markup=keyboard_settings)
        await state.set_state(AlSettings.update)

