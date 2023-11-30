from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from database import Requests
from utils import texts, links_images
from my_keyboards import create_inline_keyboard
from states.states import AlSettings
from aiogram.exceptions import TelegramBadRequest

router_run_mes = Router()

keyboards_adv = create_inline_keyboard(width=2, buttons_dict=texts.adv_buttons)
keyboards_adv_without_del = create_inline_keyboard(width=1, buttons_dict=texts.adv_buttons_without_del)
photo_dict: dict = {}


@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed), F.data == '/next_apart')
@router_run_mes.callback_query(StateFilter(AlSettings.update, AlSettings.finish_start_settings, AlSettings.start),
                               F.data == '/run')
async def gimme_one_mes(callback: CallbackQuery, state: FSMContext):
    """Функция для получения сообщения записи о непросмотренной квартире в сообщении"""
    adv_to_mes = await Requests.get_entry_apart(callback.from_user.id)
    if adv_to_mes:
        await Requests.insert_adv_to_viewed(callback.from_user.id, adv_to_mes['adv_id'])
        # print(adv_to_mes)
        media = links_images(adv_to_mes['adv_id'])
        photo_dict[callback.from_user.id] = media

        await callback.bot.send_photo(chat_id=callback.message.chat.id, photo=adv_to_mes['images'][0]['imgurl'],
                                      caption=f"Квартира, {adv_to_mes['metro']} район,\n\n"
                                              f"<b>Цена: {adv_to_mes['price']}</b>\n\n"
                                              f"Количество комнат: {adv_to_mes['rooms']},\n"
                                              f"Общая площадь: {adv_to_mes['square']},\n"
                                              f"Этаж: {adv_to_mes['floor']},\n"
                                              f"Мебель: {adv_to_mes['furniture']},\n"
                                              f"Ремонт: {adv_to_mes['repair']},\n"
                                              f"Телефон: {adv_to_mes['phone']},\n"
                                              f"Адрес: {adv_to_mes['address']},\n\n"
                                              f"Описание:{adv_to_mes['description']}\n"
                                              f"\n<i>актуально на {adv_to_mes['date_adv']}</i>\n"
                                              f"Источник: {adv_to_mes['url']}", parse_mode='HTML',
                                      reply_markup=keyboards_adv)
    else:
        await callback.message.answer('Вариантов больше нет')
    await state.set_state(AlSettings.adv_showed)


# @router_run_mes.callback_query(StateFilter(AlSettings.adv_showed),
#                                F.data == '/favorite')
# async def mes_without_del(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text()

@router_run_mes.callback_query(StateFilter(AlSettings.adv_showed), F.data == '/more')
async def more_photo(callback: CallbackQuery, state: FSMContext):
    media = photo_dict[callback.from_user.id]
    if len(media) == 1:
        await callback.message.answer('Арендодатель оставил только одну фотографию')
    else:
        await callback.bot.send_media_group(callback.message.chat.id, media=media)
