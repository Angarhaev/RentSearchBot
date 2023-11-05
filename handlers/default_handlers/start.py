from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def start_bot(message: Message):
    bot.reply_to(message, 'Привет! Начнем поиск? Введите искомый товар')