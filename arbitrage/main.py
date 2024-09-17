import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from app.arbitrage.arbitrage import Arbitrage
from app.bot.general import start_bot_message
from app.utils.enums import Exchanges

logger = logging.getLogger(__name__)


async def on_startup(dp: Dispatcher):
    await start_bot_message(dp)
    arbitrage = Arbitrage(dp=dp, current_exchange=Exchanges.BINANCE)
    arbitrage.init_parameters()
    await arbitrage.start_arbitrage()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    logging.debug('Starting bot')

    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # register_messages_general(dp)

    task_skip_updates = asyncio.create_task(dp.skip_updates())
    task_start_polling = asyncio.create_task(dp.start_polling())
    task_on_startup = asyncio.create_task(on_startup(dp))

    await task_on_startup
    await task_skip_updates
    await task_start_polling


if __name__ == '__main__':
    asyncio.run(main())

