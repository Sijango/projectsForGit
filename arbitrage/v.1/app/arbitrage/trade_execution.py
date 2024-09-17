import datetime
import time
import ccxt
from typing import Dict
from aiogram import Dispatcher

import config
from app.arbitrage.exchanges import get_exchange
from app.utils.enums import Exchanges, TradeSide, TradeStatus


class Trade:
    # dp: Dispatcher = None

    exchanges: Dict[str, any] = {}
    binance_exchange: ccxt.binance = None
    bybit_exchange: ccxt.bybit = None

    exchange_balances: Dict[str, any] = {}
    exchange_addresses: Dict[str, any] = {}

    order_waiting_time: int = None
    amount: int = None
    percent: float = None

    current_exchange: Exchanges = None
    trade_side: TradeSide = None
    trade_status: TradeStatus = None

    def __init__(
            self,
            amount=100,
            percent_usdt=0.9975,
            order_waiting_time=60,
            current_exchange=Exchanges.BINANCE
    ):
        try:
            self.exchanges = get_exchange()
            self.binance_exchange = self.exchanges[str(Exchanges.BINANCE.value)]
            self.bybit_exchange = self.exchanges[str(Exchanges.BYBIT.value)]

            self.order_waiting_time = order_waiting_time
            self.amount = amount
            self.percent = percent_usdt

            self.current_exchange = current_exchange
            self.trade_side = TradeSide.BUY
            self.trade_status = TradeStatus.WAIT

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Success create.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR

    def init_trade_params(self):
        try:
            self.update_markets()
            self.get_balances()
            self.get_addresses()

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Trade params init - Success.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Trade params init - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR

    def update_markets(self):
        try:
            self.binance_exchange.load_markets()
            self.bybit_exchange.load_markets()

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Update markets - Success.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Update markets - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR

    def get_addresses(self):
        try:
            self.exchange_addresses = {
                "binance": self._get_binance_bep20_address(),
                "bybit": self._get_bybit_bep20_address()
            }

            return self.exchange_addresses

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get exchange addresses - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return {}

    def get_balances(self):
        """Получение балансов кошельков"""
        try:
            binance_balance_tmp: Dict[str, any] = self.binance_exchange.fetch_balance()
            bybit_balance_tmp: Dict[str, any] = self.bybit_exchange.fetch_balance()

            binance_balance = {}
            for coin in binance_balance_tmp['info']['balances']:
                if float(coin["free"]) > 0:
                    binance_balance[coin["asset"]] = coin["free"]

            bybit_balance = {}

            for coin in bybit_balance_tmp['info']['result']['balances']:
                if float(coin["total"]) > 0:
                    bybit_balance[coin["coin"]] = coin["total"]

            self.exchange_balances = {
                "binance": binance_balance,
                "bybit": bybit_balance
            }

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get exchange balances - Success.")
            return self.exchange_balances

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get exchange balances - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return {}

    def get_binance_usdt_amount(self):
        """Получение кол-ва USDT на кошельке Binance"""
        # if self.exchange_balances == {}:
        self.get_balances()

        if self.trade_status == TradeStatus.ERROR:
            return 0

        try:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get binance amount - Success.")
            return round(float(self.exchange_balances["binance"]["USDT"]), 3)

        except Exchanges as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get binance amount - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return 0

    def get_bybit_usdt_amount(self):
        """Получение кол-ва USDT на кошельке Bybit"""
        # if self.exchange_balances == {}:
        self.get_balances()

        if self.trade_status == TradeStatus.ERROR:
            return

        try:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get bybit amount - Success.")
            return self.exchange_balances["bybit"]["USDT"]

        except Exchanges as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get bybit amount - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return 0

    def execute_trade(self, solution):
        """Функция для выполнения одиночной сделки при заданном ключе и значении"""
        try:
            if self.trade_status == TradeStatus.ERROR:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Trade Execution {date}] Execute trade - Status Stop. Solution: {solution}")
                return False

            first_exc = solution["first_exc"]
            sec_exc = solution["second_exc"]

            if first_exc == sec_exc:
                order_info = self._intra_exc_trade(solution)
                succeed = self._wait_to_end_order(order_info, first_exc)

            else:
                self._inter_exc_trade(solution)
                succeed = True

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Execute trade - Success. Solution: {solution}")
            return succeed

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Execute trade - Error. Solution: {solution}")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return 0

    def get_amount(self, current_exchange: Exchanges, coin: str, amount=100, fix_amount=False):
        if self.trade_status == TradeStatus.ERROR:
            return 0, False
        self.get_balances()

        try:
            if coin == "USDT":
                if fix_amount:
                    if self.exchange_balances[current_exchange.value]["USDT"] > amount:
                        return amount, True
                    else:
                        return float(self.exchange_balances[current_exchange.value]["USDT"]) - float(config.PAIR_FEES["USDT"]), True
                else:
                    return float(self.exchange_balances[current_exchange.value]["USDT"]) - float(config.PAIR_FEES["USDT"]), True
            elif coin in self.exchange_balances[current_exchange.value].keys():
                return float(self.exchange_balances[current_exchange.value][coin]) - float(config.PAIR_FEES[coin]), True
            else:
                return 0, False

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Get amount - Error:")
            print(ex)
            self.trade_status = TradeStatus.ERROR
            return 0, False

    def checking_external_address(self, target_exchange, coin):
        """Проверка биржи на наличие вывода в сети BEP20"""
        try:
            if target_exchange == Exchanges.BINANCE:
                exchange = self.bybit_exchange
            elif target_exchange == Exchanges.BYBIT:
                exchange = self.binance_exchange
            else:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Trade Execution {date}] Checking external address pair: {coin} - No match address.")
                return False

            params = {
                "network": config.NETWORK
            }
            address_info = exchange.fetch_deposit_address(
                coin.split("/")[0],
                params=params
            )

            if address_info is not None:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Trade Execution {date}] Checking external address pair: {coin} - Success.")
                return True
            else:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Trade Execution {date}] Checking external address pair: {coin} - No match address.")
                return False

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Trade Execution {date}] Checking external address pair: {coin} - Error or No match address:")
            print(ex)
            return False

    def _intra_exc_trade(self, solution):
        """Создание ордеров внутри биржами"""
        exc_name = solution["first_exc"]
        exchange = self.exchanges[exc_name]

        symbol = solution["symbol"]
        type = 'market'
        side = solution["side"]
        amount = solution["amount"]
        price = solution["price"]

        if exc_name == Exchanges.BINANCE.value:
            type = "limit"
            return exchange.create_order(
                symbol=symbol,
                type=type,
                side=side,
                amount=amount,
                price=price
            )
        else:
            prices = exchange.fetch_tickers()
            price = float(prices[symbol]["ask"])

            return exchange.create_order(
                symbol=symbol,
                type=type,
                side=side,
                amount=amount,
                price=price
            )

    def _inter_exc_trade(self, solution):
        """Создание ордеров между биржами"""
        coin = solution["symbol"].split("/")[0]
        exc_name = solution["first_exc"]
        target_exc_name = solution["second_exc"]
        exchange = self.exchanges[exc_name]
        target_exchange = self.exchanges[target_exc_name]

        if target_exc_name == "binance":
            params = {
                "network": "BEP20"
            }
        else:
            params = {
                "network": config.NETWORK
            }

        address_info = target_exchange.fetch_deposit_address(
            coin,
            params=params
        )
        address = address_info['address']
        tag = address_info['tag']
        amount = round(float(solution["amount"]) * self.percent, 4)

        exchange.withdraw(
            code=coin,
            amount=amount,
            address=address,
            tag=tag,
            params=params
        )

    def _wait_to_end_order(self, order_info, exc_name):
        """
        Функция ожидания в течение определенного промежутка времени после размещения заказа.
        Если заказ был выполнен за заданный промежуток времени, он возвращает значение True.
        Если ордер не был выполнен, он отменит ордер и вернет значение False
        """
        closed = False
        id = order_info['info']['orderId']
        symbol = order_info['symbol']
        exchange = self.exchanges[exc_name]
        start = time.time()

        while time.time() - start <= self.order_waiting_time:
            if exchange.fetch_order_status(id, symbol) != 'closed':
                time.sleep(0.2)
            else:
                closed = True
                break

        if not closed:
            try:
                exchange.cancel_order(id, symbol)
                succeed = False
            except Exception as ex:
                succeed = True
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Trade Execution {date}] Wait to end order - Error:\n{str(ex)}")
        else:
            succeed = True

        return succeed

    def _get_binance_bep20_address(self):
        deposit_info = self.binance_exchange.fetch_deposit_address(
            code=config.COIN_TO_TRANSFER,
            params={
                "network": config.NETWORK
            }
        )

        return deposit_info["address"]

    def _get_bybit_bep20_address(self):
        deposit_info = self.bybit_exchange.fetch_deposit_address(
            code=config.COIN_TO_TRANSFER,
            params={
                "network": config.NETWORK
            }
        )

        return deposit_info["address"]


