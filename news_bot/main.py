import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from app.handlers.news import register_handlers_send
from app.handlers.basic import register_handlers_basic
from app.handlers.news import send_data
from app.lib.scrap_news.scrap_news import get_news

logger = logging.getLogger(__name__)
# CONFIG = load_config()
scheduler = AsyncIOScheduler()


def scheduler_job(dp):
    scheduler.add_job(send_data, "interval", minutes=5, args=(dp,))


async def on_startup(dp: Dispatcher):
    scheduler_job(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    logging.debug('Starting bot')

    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_basic(dp, admins=config.ADMINS)
    register_handlers_send(dp, admins=config.ADMINS)

    await on_startup(dp)
    scheduler.start()

    await dp.skip_updates()
    await dp.start_polling()

    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.run(get_news())
