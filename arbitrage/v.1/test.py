import datetime
import json
import time
import asyncio
from typing import Dict

import ccxt

from app.utils.enums import Exchanges
import config
from app.arbitrage.exchanges import get_async_exchange


# binance_exchange: ccxt.binance = ccxt.binance({
#     "apiKey": "WUMX5u744Gh9iZxfFeuMi5qCssMcUHXWCQ93iRjPYt50DEirHGn7uFPwGfeqvLW3",
#     "secret": "mPLHnF06mXBnLINsODKyajWrnn5LOeIT3j7nWXkwTyrzkKAvBmtjbO7EEnl2Ku7c",
#     "options": {
#         "defaultType": "spot"
#     }
#     # "verbose": True
# })
# # binance_exchange.set_sandbox_mode(True)
#
# bybit_exchange: ccxt.bybit = ccxt.bybit({
#     "apiKey": "gEaV31OjY6BjfZ31lb",
#     "secret": "0tqUARKNw1CClJLpEwB0otUUvrTBtRtbfnAZ",
#     # "options": {
#     #     "defaultType": "spot"
#     # },
#     # "verbose": True
# })


# def loads_markets():
#     binance_exchange.load_markets()
#     bybit_exchange.load_markets()
#
#
# def get_deposit_address():
#     code = "USDT"
#     params = {"network": "BEP20"}
#
#     deposit_binance = binance_exchange.fetch_deposit_address(code, params)
#     # deposit_bybit = bybit_exchange.fetch_deposit_address(code, params)
#
#     print(f"Binance deposit:\n{deposit_binance}")
#     # print(f"Bybit deposit:\n{deposit_bybit}")
#
#
# def create_order(
#         symbol="BTC/USDT",
#         order_type="market",
#         amount=1,
#         side="buy"
# ):
#     order = binance_exchange.create_order(symbol, type=order_type, side=side, amount=amount)
#     print(order)


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


def send_from_bybit(binance_exchange: ccxt.binance, bybit_exchange: ccxt.bybit):
    bybit_balance_tmp: Dict[str, any] = bybit_exchange.fetch_balance()

    deposit_info = binance_exchange.fetch_deposit_address(
        code="USDT",
        params={
            "network": "BEP20"
        }
    )
    print(f"Binance info address: \n{deposit_info}")

    bybit_balance = {}
    for coin in bybit_balance_tmp['info']['result']['balances']:
        if float(coin["total"]) > 0:
            bybit_balance[coin["coin"]] = coin["total"]

    print(f"Bybit all: \n{bybit_balance_tmp}")
    print(f"Bybit: \n{bybit_balance}")

    params = {"network": "BEP20"}
    bybit_exchange.withdraw(
        code="USDT",
        amount=round(float(bybit_balance["USDT"]) * 0.98, 4),
        address=deposit_info["address"],
        tag=deposit_info["tag"],
        params=params
    )


def get_balances(binance_exchange: ccxt.binance, bybit_exchange: ccxt.bybit):
    """Получение балансов кошельков"""
    try:
        binance_balance_tmp: Dict[str, any] = binance_exchange.fetch_balance()
        bybit_balance_tmp: Dict[str, any] = bybit_exchange.fetch_balance()

        binance_balance = {}
        for coin in binance_balance_tmp['info']['balances']:
            if float(coin["free"]) > 0:
                binance_balance[coin["asset"]] = coin["free"]

        bybit_balance = {}
        print(bybit_balance_tmp)
        for coin in bybit_balance_tmp['info']['result']['balances']:
            if float(coin["total"]) > 0:
                bybit_balance[coin["coin"]] = coin["total"]

        exchange_balances = {
            "binance": binance_balance,
            "bybit": bybit_balance
        }

        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Trade Execution {date}] Get exchange balances - Success.")
        return exchange_balances

    except Exception as ex:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Trade Execution {date}] Get exchange balances - Error:")
        print(ex)
        return {}


def send_from_binance(binance_exchange: ccxt.binance, bybit_exchange: ccxt.bybit):
    # binance_balance_tmp: Dict[str, any] = binance_exchange.fetch_balance()
    #
    # binance_balance = {}
    # for coin in binance_balance_tmp['info']['balances']:
    #     if float(coin["free"]) > 0:
    #         binance_balance[coin["asset"]] = coin["free"]

    deposit_info = bybit_exchange.fetch_deposit_address(
        code="USDT",
        params={
            "network": "BEP20"
        }
    )

    params = {"network": "BEP20"}
    binance_exchange.withdraw(
        code="USDT",
        amount=29,
        address=deposit_info["address"],
        tag=deposit_info["tag"],
        params=params
    )


def buy_binance_coin(binance_exchange: ccxt.binance):
    symbol = "BNB/USDT"
    type = 'market'
    side = "buy"
    amount = 30/300

    return binance_exchange.create_order(
        symbol=symbol,
        type=type,
        side=side,
        amount=amount
    )


def sell_binance_coin(binance_exchange: ccxt.binance):
    symbol = "BNB/USDT"
    type = 'market'
    side = "sell"
    amount = 30/300

    return binance_exchange.create_order(
        symbol=symbol,
        type=type,
        side=side,
        amount=amount
    )


def buy_bybit_coin(bybit_exchange: ccxt.bybit):
    symbol = "BNB/USDT"
    type = 'market'
    side = "buy"

    prices = bybit_exchange.fetch_tickers()
    ask = float(prices['BNB/USDT']['ask'])
    usdt_amount = 27
    amount = round(usdt_amount / ask, 4)

    return bybit_exchange.create_order(
        symbol=symbol,
        type=type,
        side=side,
        amount=amount,
        price=ask
    )


def sell_bybit_coin(bybit_exchange: ccxt.bybit):
    symbol = "BNB/USDT"
    type = 'market'
    side = "sell"

    bybit_balance_tmp: Dict[str, any] = bybit_exchange.fetch_balance()
    bybit_balance = {}
    print(bybit_balance_tmp)
    for coin in bybit_balance_tmp['info']['result']['balances']:
        if float(coin["total"]) > 0:
            bybit_balance[coin["coin"]] = coin["total"]

    prices = bybit_exchange.fetch_tickers()
    ask = float(prices['BNB/USDT']['ask'])
    # usdt_amount = 29
    # amount = round(usdt_amount / ask, 4)

    return bybit_exchange.create_order(
        symbol=symbol,
        type=type,
        side=side,
        amount=round(float(bybit_balance["BNB"]), 5),
        price=ask
    )


def get_exchange() -> Dict[str, any]:
    exchanges = {}

    # binance_exchange: ccxt.binance = ccxt.binance({
    #     "apiKey": config.BINANCE_EXCHANGE_DATA["api_key"],
    #     "secret": config.BINANCE_EXCHANGE_DATA["secret_key"],
    #     "option": config.BINANCE_EXCHANGE_DATA["option"]
    # })
    # bybit_exchange: ccxt.bybit = ccxt.bybit({
    #     "apiKey": config.BYBIT_EXCHANGE_DATA["api_key"],
    #     "secret": config.BYBIT_EXCHANGE_DATA["secret_key"],
    #     "option": config.BYBIT_EXCHANGE_DATA["option"]
    # })
    binance_exchange = get_binance_exchange()
    bybit_exchange = get_bybit_exchange()
    # print(bybit_exchange.fetch_balance())
    exchanges[str(Exchanges.BINANCE.value)] = binance_exchange
    exchanges[str(Exchanges.BYBIT.value)] = bybit_exchange

    return exchanges


def get_last_price(pair: str, exchange):
    order_book = exchange.fetch_order_book(pair)
    return {
        "ask": float(order_book["asks"][0][0]) if len(order_book['asks']) > 0 else None,
        "bid": float(order_book["bids"][0][0]) if len(order_book['bids']) > 0 else None
    }


async def get_all_async_last_price():
    exchanges = await get_async_exchange()
    tasks = []

    for pair in config.ADDED_PAIRS:
        tasks.append(get_async_last_price(pair, exchanges["binance"], "binance"))
        tasks.append(get_async_last_price(pair, exchanges["bybit"], "bybit"))
    results = await asyncio.gather(*tasks)

    pairs_data = {}
    for i in range(0, len(results), 2):
        binance_rate = results[i]
        bybit_rate = results[i + 1]
        pair_name = config.ADDED_PAIRS[i // 2]
        pairs_data[pair_name] = {"binance_rate": binance_rate, "bybit_rate": bybit_rate}

    await exchanges["binance"].close()
    await exchanges["bybit"].close()

    return pairs_data


async def get_async_last_price(pair: str, exchange, exchange_name):
    order_book = await exchange.fetch_order_book(pair)
    return {
        "exc_name": exchange_name,
        "ask": float(order_book["asks"][0][0]) if len(order_book['asks']) > 0 else None,
        "bid": float(order_book["bids"][0][0]) if len(order_book['bids']) > 0 else None
    }


def main():
    # loads_markets()
    #
    # # Get deposits
    # get_deposit_address()
    exchange = get_exchange()
    binance_exchange: ccxt.binance = exchange["binance"]
    # bybit_exchange: ccxt.bybit = get_bybit_exchange()
    # fetch = bybit_exchange.fetch_balance()
    # print(fetch)
    # binance_exchange: ccxt.binance = exchange["binance"]
    bybit_exchange: ccxt.bybit = exchange["bybit"]
    # fetch = bybit_exchange.fetch_balance()
    # print(fetch)
    # binance_exchange.load_markets()
    # bybit_exchange.load_markets()

    # buy_binance_coin(binance_exchange)
    # sell_binance_coin(binance_exchange)
    # send_from_binance(binance_exchange, bybit_exchange)
    # buy_bybit_coin(bybit_exchange)
    # sell_bybit_coin(bybit_exchange)
    # send_from_bybit(binance_exchange, bybit_exchange)
    data = binance_exchange.fetch_currencies()
    print("{")
    for key in data.keys():
        print(f"{key}: {data[key]['networks']}, ")
    print("}")
    # for pair in config.ADDED_PAIRS:
    #     binance_eth = get_last_price(pair, binance_exchange)
    #     bybit_eth = get_last_price(pair, bybit_exchange)
    #
    #     print("binance:", pair, binance_eth)
    #     print("bybit:", pair, bybit_eth)
    # bal = get_balances(binance_exchange, bybit_exchange)
    # print(bal)
    # send_from_binance(binance_exchange, bybit_exchange)
    # send_from_bybit(binance_exchange, bybit_exchange)


if __name__ == '__main__':
    # main()
    exchange = get_exchange()
    result = asyncio.run(get_all_async_last_price())

    print(result)
