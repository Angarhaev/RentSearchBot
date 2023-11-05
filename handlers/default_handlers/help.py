from telebot.types import Message
from loader import bot

@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = ("Список комманд",
            "/start - Начать диалог"
            "/help - Получить справку"
            )

    bot.reply_to(message, "\n".join(text))