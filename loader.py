import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from config_data import config
from handlers import router, router_settings, router_search, router_echo, router_run_mes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import ShedulerFunc
from datetime import datetime
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

    """Инициализация бота и диспетчера"""
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    """Автоматическая рассылка сообщений и обновление базы"""
    scheduler = AsyncIOScheduler(timezone="Asia/Irkutsk")
    scheduler.add_job(ShedulerFunc.sheduler_send_adv, trigger='cron', hour=12, minute=00, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(ShedulerFunc.sheduler_update_base_adv, trigger='cron', hour=8, minute=0, start_date=datetime.now())
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
