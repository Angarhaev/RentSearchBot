from telebot.types import Message
from loader import bot

# Текстовые сообщения без состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                 f'{message.text}')