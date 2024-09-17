import ccxt
import ccxt.async_support as async_ccxt
from typing import Dict

import config
from app.utils.enums import Exchanges


def get_exchange() -> Dict[str, any]:
    exchanges = {}

    binance_exchange = get_binance_exchange()
    bybit_exchange = get_bybit_exchange()

    exchanges[str(Exchanges.BINANCE.value)] = binance_exchange
    exchanges[str(Exchanges.BYBIT.value)] = bybit_exchange

    return exchanges


def get_binance_exchange():
    return ccxt.binance({
        "apiKey": config.BINANCE_EXCHANGE_DATA["api_key"],
        "secret": config.BINANCE_EXCHANGE_DATA["secret_key"],
        "options": config.BINANCE_EXCHANGE_DATA["option"]
    })


def get_bybit_exchange():
    return ccxt.bybit({
        "apiKey": config.BYBIT_EXCHANGE_DATA["api_key"],
        "secret": config.BYBIT_EXCHANGE_DATA["secret_key"],
        "options": config.BYBIT_EXCHANGE_DATA["option"]
    })


async def get_async_exchange() -> Dict[str, any]:
    exchanges = {}

    async_binance_exchange = await get_async_binance_exchange()
    async_bybit_exchange = await get_async_bybit_exchange()

    exchanges[str(Exchanges.BINANCE.value)] = async_binance_exchange
    exchanges[str(Exchanges.BYBIT.value)] = async_bybit_exchange

    return exchanges


async def get_async_binance_exchange():
    return async_ccxt.binance({
        "apiKey": config.BINANCE_EXCHANGE_DATA["api_key"],
        "secret": config.BINANCE_EXCHANGE_DATA["secret_key"],
        "options": config.BINANCE_EXCHANGE_DATA["option"]
    })


async def get_async_bybit_exchange():
    return async_ccxt.bybit({
        "apiKey": config.BYBIT_EXCHANGE_DATA["api_key"],
        "secret": config.BYBIT_EXCHANGE_DATA["secret_key"],
        "options": config.BYBIT_EXCHANGE_DATA["option"]
    })

