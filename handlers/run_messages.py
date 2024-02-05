from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from database import DatabaseCommands
from utils import EasyFunc
from my_keyboards import KeyboardRunCreate
from states.states import AlSettings


router_run_mes = Router()


@router_run_mes.message(F.text == "🏠")
async def lets_find(message: Message, state: FSMContext):
    await message.delete()
    keyboards_adv = await KeyboardRunCreate.keyboards_adv()
    keyboard_back = await KeyboardRunCreate.keyboard_back()
    await state.update_data(keyboards_adv=keyboards_adv)
    await state.update_data(keyboard_back=keyboard_back)
    adv_to_mes = await DatabaseCommands.select_not_viewed_adv_cache(message.from_user.id)
    if adv_to_mes:
        media = await EasyFunc.links_images(adv_to_mes[0].images.split(', '))
        await state.update_data(media=media)

        await message.bot.send_photo(chat_id=message.chat.id, photo=adv_to_mes[0].images.split(', ')[0],
                                     caption=f"Квартира, {adv_to_mes[0].district} район,\n\n"
                                             f"<b>Цена: {adv_to_mes[0].price}</b>\n\n"
                                             f"Количество комнат: {adv_to_mes[0].rooms},\n"
                                             f"Общая площадь: {adv_to_mes[0].square},\n"
                                             f"Этаж: {adv_to_mes[0].floor},\n"
                                             f"Мебель: {adv_to_mes[0].furniture},\n"
                                             f"Ремонт: {adv_to_mes[0].repair},\n"
                                             f"Телефон: {adv_to_mes[0].phone},\n"
                                             f"Адрес: {adv_to_mes[0].address},\n\n"
                                             f"Описание:{adv_to_mes[0].description}\n"
                                             f"\n<i>актуально на {adv_to_mes[0].date_adv}</i>\n"
                                             f"Источник: {adv_to_mes[0].url}", parse_mode='HTML',
                                     reply_markup=keyboards_adv)
    else:

        await message.answer('Попробуйте позже или измените параметры для поиска',
                             reply_markup=keyboard_back)

    await state.set_state(AlSettings.adv_showed)


@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed, AlSettings.adv_showed_photos,
                                           AlSettings.start, AlSettings.settings,
                                           None), F.data.in_({'/next_apart', '/run'}))
@router_run_mes.callback_query(StateFilter(AlSettings.update, AlSettings.finish_start_settings, AlSettings.start),
                               F.data == '/run')
async def gimme_one_mes(callback: CallbackQuery, state: FSMContext):
    """Функция для получения сообщения записи о непросмотренной квартире в личном сообщении от бота"""
    keyboards_adv = await KeyboardRunCreate.keyboards_adv()
    keyboard_back = await KeyboardRunCreate.keyboard_back()
    await state.update_data(keyboards_adv=keyboards_adv)
    await state.update_data(keyboard_back=keyboard_back)

    adv_to_mes = await DatabaseCommands.select_not_viewed_adv_cache(callback.from_user.id)
    if adv_to_mes:
        media = await EasyFunc.links_images(adv_to_mes[0].images.split(', '))
        await state.update_data(media=media)

        await callback.bot.send_photo(chat_id=callback.message.chat.id, photo=adv_to_mes[0].images.split(', ')[0],
                                      caption=f"Квартира, {adv_to_mes[0].district} район,\n\n"
                                              f"<b>Цена: {adv_to_mes[0].price}</b>\n\n"
                                              f"Количество комнат: {adv_to_mes[0].rooms},\n"
                                              f"Общая площадь: {adv_to_mes[0].square},\n"
                                              f"Этаж: {adv_to_mes[0].floor},\n"
                                              f"Мебель: {adv_to_mes[0].furniture},\n"
                                              f"Ремонт: {adv_to_mes[0].repair},\n"
                                              f"Телефон: {adv_to_mes[0].phone},\n"
                                              f"Адрес: {adv_to_mes[0].address},\n\n"
                                              f"Описание:{adv_to_mes[0].description}\n"
                                              f"\n<i>актуально на {adv_to_mes[0].date_adv}</i>\n"
                                              f"Источник: {adv_to_mes[0].url}", parse_mode='HTML',
                                      reply_markup=keyboards_adv)
    else:
        await callback.message.answer('Попробуйте позже или измените параметры для поиска',
                                      reply_markup=keyboard_back)
    await state.set_state(AlSettings.adv_showed)


@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed), F.data == '/more')
async def more_photo(callback: CallbackQuery, state: FSMContext):
    """Функция для отправки дополнительных фотографий квартиры"""
    keyboards_adv_more = await KeyboardRunCreate.keyboards_adv_more()
    get_dict = await state.get_data()
    media = get_dict['media']
    if len(media) == 1:
        await callback.message.answer('Арендодатель оставил только одну фотографию',
                                      reply_markup=keyboards_adv_more)
    else:
        await callback.bot.send_media_group(callback.message.chat.id, media=media)
        await callback.message.answer('Есть еще варианты',
                                      reply_markup=keyboards_adv_more)

    await state.set_state(AlSettings.adv_showed_photos)


@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed, None), F.data == '/delete')
async def delete_message(callback: CallbackQuery, state: FSMContext):
    await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(AlSettings.adv_showed)


@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed_photos, None), F.data == '/delete')
async def delete_message_media(callback: CallbackQuery, state: FSMContext):
    await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    get_dict = await state.get_data()
    media = get_dict['media']
    for i in range(1, len(media)+1):
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - i)
    await state.set_state(AlSettings.adv_showed)
