from aiogram import Bot
from utils import texts


async def send_adv(bot: Bot):
    """Функция отправки сообщений для sheduler'a"""
    await bot.send_message(300844218, texts.time_adv['adv'])
    #в chat_id номера чата из базы
