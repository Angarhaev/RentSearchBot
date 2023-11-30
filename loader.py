import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from config_data import config
from handlers import router, router_settings, router_search, router_echo, router_run_mes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.time_message import send_adv
from datetime import datetime
#from database.create_tables import start_create_table
from database import async_main

storage = MemoryStorage()
logger = logging.getLogger(__name__)

log_format = ('%(filename)s:%(lineno)d #%(levelname)-8s'
              '[%(asctime)s] - %(name)s - %(message)s')


async def load() -> None:
    logging.basicConfig(
        level=logging.INFO, format=log_format)

    """Инициализация базы данных"""
    await async_main()
    #start_create_table()

    """Инициализация бота и диспетчера"""
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    """Ежедневная автоматическая отправка варианта квартиры"""
    scheduler = AsyncIOScheduler(timezone="Asia/Irkutsk")
    scheduler.add_job(send_adv, trigger='cron', hour=12, minute=0, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()

    """Регистрируем хэндлеры"""
    dp.include_router(router)
    dp.include_router(router_settings)
    dp.include_router(router_search)
    dp.include_router(router_run_mes)

    dp.include_router(router_echo)

    """Игнорирование старых сообщений"""
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)
