
import asyncio
import aiohttp
import datetime
from typing import Dict
from aiogram import Dispatcher

import config
from app.bot.general import send_new_pair_message
from app.utils.enums import Exchanges
from app.arbitrage.exchanges import get_async_exchange


class Pairs:
    dp: Dispatcher
    pairs_data: Dict[str, any] = None
    best_pair: Dict[str, any] = None
    current_exchange: Exchanges = None
    direction: str = None

    def __init__(self, dp: Dispatcher, current_exchange: Exchanges = Exchanges.BINANCE):
        try:
            self.dp = dp
            self.pairs_data = {}
            self.current_exchange = current_exchange

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Pairs {date}] Success create.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Pairs {date}] Error:")
            print(ex)

    async def get_pair_path(self, current_exchange=Exchanges.BINANCE, amount_usdt=0):
        try:
            await self._get_pairs_data()
            self.current_exchange = current_exchange

            if self.current_exchange == Exchanges.BINANCE:
                access = await self._get_best_binance_bybit_pair(amount_usdt)
                self.current_exchange = Exchanges.BYBIT

                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                if self.best_pair is None:
                    print(f"[SYS Pairs {date}] Dont find pair on Binance")
                    return None, False

                print(f"[SYS Pairs {date}] Success find pair: {self.best_pair['token']} on Binance")
                data = {
                    "pair": self.best_pair['token'],
                    "first_exc": "binance",
                    "first_cast": self.best_pair["price_binance"],
                    "second_exc": "bybit",
                    "second_cast": self.best_pair["price_bybit"]
                }
                await send_new_pair_message(self.dp, data=data, access=self.best_pair["access"], income=self.best_pair["income"], percent=self.best_pair["percent"])
                return self.best_pair, access

            elif self.current_exchange == Exchanges.BYBIT:
                access = await self. _get_best_bybit_binance_pair(amount_usdt)
                self.current_exchange = Exchanges.BINANCE

                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                if self.best_pair is None:
                    print(f"[SYS Pairs {date}] Dont find pair on Bybit")
                    return None, False

                print(f"[SYS Pairs {date}] Success find pair: {self.best_pair['token']} on Bybit")
                data = {
                    "pair": self.best_pair['token'],
                    "first_exc": "bybit",
                    "first_cast": self.best_pair["price_bybit"],
                    "second_exc": "binance",
                    "second_cast": self.best_pair["price_binance"]
                }
                await send_new_pair_message(self.dp, data=data, access=self.best_pair["access"], income=self.best_pair["income"], percent=self.best_pair["percent"])
                return self.best_pair, access

            # # self.best_pair = None
            # date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            # print(f"[SYS Pairs {date}] Fault to find pair.")
            # # await send_new_pair_message(self.dp, data=None)
            return None, False

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Pairs {date}] Get pair path - Error:")
            print(ex)
            return None, False

    def update_current_exchange(self, current_exchange: Exchanges):
        self.current_exchange = current_exchange

    async def _get_best_binance_bybit_pair(self, amount):
        self.best_pair = None

        if self.pairs_data is None:
            await self._get_pairs_data()

        best_difference = 0
        access = False

        for pair_name in self.pairs_data:
            pair_data = self.pairs_data[pair_name]

            # difference = ((pair_data["bybit_rate"]["bid"] - pair_data["binance_rate"]["ask"]) / pair_data["binance_rate"]["ask"]) * 100
            income = self.calc_formula(amount, buy_price=pair_data["binance_rate"]["ask"], sell_price=pair_data["bybit_rate"]["bid"])
            difference = self.calc_percent(buy_price=pair_data["binance_rate"]["ask"], sell_price=pair_data["bybit_rate"]["bid"])

            if difference > best_difference:
                best_difference = difference
                access = False
                if difference >= config.PERCENT or income > 0:
                    access = False

                self.best_pair = {
                    "token": pair_name.replace("USDT", "/USDT"),
                    "price_binance": pair_data["binance_rate"]["ask"],
                    "price_bybit": pair_data["bybit_rate"]["bid"],
                    "income": income,
                    "percent": difference,
                    "access": access
                }
        return access

    async def _get_best_bybit_binance_pair(self, amount):
        self.best_pair = None

        if self.pairs_data is None:
            await self._get_pairs_data()

        best_difference = 0
        access = False

        for pair_name in self.pairs_data:
            pair_data = self.pairs_data[pair_name]

            # difference = ((pair_data["binance_rate"]["bid"] - pair_data["bybit_rate"]["ask"]) / pair_data["bybit_rate"]["ask"]) * 100
            income = self.calc_formula(amount, buy_price=pair_data["bybit_rate"]["ask"], sell_price=pair_data["binance_rate"]["bid"])
            difference = self.calc_percent(buy_price=pair_data["bybit_rate"]["ask"], sell_price=pair_data["binance_rate"]["bid"])

            if difference > best_difference:
                best_difference = difference
                access = False
                if difference >= config.PERCENT or income > 0:
                    access = False

                self.best_pair = {
                    "token": pair_name.replace("USDT", "/USDT"),
                    "price_binance": pair_data["binance_rate"]["bid"],
                    "price_bybit": pair_data["bybit_rate"]["ask"],
                    "income": income,
                    "percent": difference,
                    "access": access
                }
        return access

    async def _get_pairs_data(self):
        exchanges = await get_async_exchange()
        tasks = []

        for pair in config.ADDED_PAIRS:
            tasks.append(self.get_async_last_price(pair, exchanges["binance"]))
            tasks.append(self.get_async_last_price(pair, exchanges["bybit"]))
        results = await asyncio.gather(*tasks)

        self.pairs_data = {}
        for i in range(0, len(results), 2):
            binance_rate = results[i]
            bybit_rate = results[i + 1]
            pair_name = config.ADDED_PAIRS[i // 2]
            self.pairs_data[pair_name] = {"binance_rate": binance_rate, "bybit_rate": bybit_rate}

        await exchanges["binance"].close()
        await exchanges["bybit"].close()

    async def _get_pairs_data_old(self):
        tasks = []
        for pair in config.ADDED_PAIRS:
            tasks.append(self._get_binance_rate(pair))
            tasks.append(self._get_bybit_rate(pair))
        results = await asyncio.gather(*tasks)

        self.pairs_data = {}
        for i in range(0, len(results), 2):
            binance_rate = results[i]
            bybit_rate = results[i + 1]
            pair_name = config.ADDED_PAIRS[i // 2]
            self.pairs_data[pair_name] = {"binance_rate": binance_rate, "bybit_rate": bybit_rate}

    @staticmethod
    def calc_formula(amount, buy_price, sell_price):
        part_1 = amount / buy_price - 0.001 * amount / buy_price
        part_1_com = part_1 - config.COM_BEP20 / buy_price
        part_2 = part_1_com * sell_price - part_1_com * sell_price * 0.001 - config.COM_BEP20

        return part_2 - amount

    @staticmethod
    def calc_percent(buy_price, sell_price):
        percent = ((sell_price - buy_price) / buy_price) * 100
        return percent

    @staticmethod
    async def get_async_last_price(pair: str, exchange):
        order_book = await exchange.fetch_order_book(pair)
        return {
            "ask": float(order_book["asks"][0][0]) if len(order_book['asks']) > 0 else None,
            "bid": float(order_book["bids"][0][0]) if len(order_book['bids']) > 0 else None
        }

    @staticmethod
    async def _get_binance_rate(pair):
        async with aiohttp.ClientSession() as session:
            async with session.get(config.BINANCE_RATE_URL, params={"symbol": pair}, ssl=False) as response:
                data = await response.json()

        return float(data["price"])
        # response = requests.get(config.BINANCE_RATE_URL, params={"symbol": pair})
        # data = response.json()
        #
        # return float(data["price"])

    @staticmethod
    async def _get_bybit_rate(pair):
        async with aiohttp.ClientSession() as session:
            async with session.get(config.BYBIT_RATE_URL, params={"symbol": pair}, ssl=False) as response:
                data = await response.json()
        # print(pair, data["price"])

        return float(data["result"][0]["last_price"])
        # response = requests.get(config.BYBIT_RATE_URL, params={"symbol": pair})
        # data = response.json()
        #
        # return float(data["result"][0]["last_price"])



