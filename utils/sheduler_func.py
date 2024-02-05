from utils import texts
from database.database_services import DatabaseCommands


class ShedulerFunc:
    """Класс для метод sheduler'а"""
    @staticmethod
    async def sheduler_send_adv(bot):
        """Метод автоматической рассылки сообщений для sheduler'a"""

        await bot.send_message(300844218, texts.time_adv['adv'])
        # в chat_id номера чата из базы

    @staticmethod
    async def sheduler_update_base_adv():
        """Метод старых и добавление новых объявлений"""
        await DatabaseCommands.delete_old_adv()
        await DatabaseCommands.update_adv_base()