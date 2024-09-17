import datetime
import ccxt
import time

from typing import Dict
from aiogram import Dispatcher

# import config
from app.arbitrage.exchanges import get_exchange
from app.arbitrage.pairs_execution import Pairs
from app.arbitrage.trade_execution import Trade
from app.utils.enums import TradeSide, TradeStatus, Exchanges
from app.bot.general import send_buy_message, send_sell_message, send_error_message, send_withdraw_message, \
    send_check_pair_message, send_balance_message, send_result_message, send_start_cycle_message, \
    send_stop_cycle_message


class Arbitrage:
    dp: Dispatcher = None

    exchanges: Dict[str, any] = {}
    binance_exchange: ccxt.binance = None
    bybit_exchange: ccxt.bybit = None
    main_exchange: Exchanges = None

    pairs_execution: Pairs = None
    trade_execution: Trade = None

    exchange_balances: Dict[str, any] = {}
    exchange_addresses: Dict[str, any] = {}

    order_waiting_time: int = None
    amount: int = None
    fix_amount: bool = None

    current_exchange: Exchanges = None
    trade_side: TradeSide = None
    trade_status: TradeStatus = None

    best_pair_on_binance: Dict[str, any] = None
    best_pair_on_bybit: Dict[str, any] = None

    number_loop: int = None

    start_usdt_balance: float = 0
    finish_usdt_balance: float = 0
    status_cycle: bool = False

    def __init__(
            self,
            dp,
            amount=100,
            fix_amount=False,
            order_waiting_time=30,
            current_exchange=None,
            trade_side=None,
            trade_status=None
    ):
        try:
            self.dp = dp

            self.exchanges = get_exchange()
            self.binance_exchange = self.exchanges[str(Exchanges.BINANCE.value)]
            self.bybit_exchange = self.exchanges[str(Exchanges.BYBIT.value)]

            self.amount = amount
            self.order_waiting_time = order_waiting_time
            self.fix_amount = fix_amount

            if current_exchange is not None:
                self.current_exchange = current_exchange
                self.main_exchange = current_exchange
            else:
                self.current_exchange = Exchanges.BINANCE
                self.main_exchange = Exchanges.BINANCE

            if trade_side is not None:
                self.trade_side = trade_side
            else:
                self.trade_side = TradeSide.BUY

            if trade_status is not None:
                self.trade_status = trade_status
            else:
                self.trade_status = TradeStatus.WAIT

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Success create.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Error:")
            print(ex)
            send_error_message(self.dp, error=str(ex))
            self.trade_status = TradeStatus.ERROR

    def init_parameters(self):
        try:
            if self.trade_status == TradeStatus.ERROR:
                return

            # Инициализация класса подбора пар
            self.pairs_execution = Pairs(dp=self.dp, current_exchange=self.current_exchange)

            # Инициализация торгового класса
            self.trade_execution = Trade(amount=self.amount,
                                         current_exchange=self.current_exchange)
            self.trade_execution.update_markets()       # Обновление рыночных позиций
            self.trade_execution.init_trade_params()    # Обновление торговых параметров

            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Init parameters - Success.")

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Init parameters - Error:")
            print(ex)
            send_error_message(self.dp, error=str(ex))
            self.trade_status = TradeStatus.ERROR
            return 0, False

    async def start_arbitrage(self):
        while self.trade_status != TradeStatus.ERROR and self.trade_execution.trade_status != TradeStatus.ERROR:
            status = self._get_status_command()

            # balances = self.trade_execution.get_balances()
            # await send_balance_message(dp=self.dp,
            #                            balances=balances)

            if status == "buy-binance":
                start_bal = round(float(self.trade_execution.get_binance_usdt_amount()), 3)
                if self.main_exchange == Exchanges.BINANCE:
                    if not self.status_cycle:
                        await send_start_cycle_message(dp=self.dp, start_bal=start_bal)
                        self.status_cycle = True

                self.best_pair_on_binance, pair_status = await self.pairs_execution.get_pair_path(self.current_exchange, amount_usdt=start_bal)

                if self.best_pair_on_binance is None or not pair_status:
                    solution = {
                        "first_exc": Exchanges.BINANCE.value,
                        "second_exc": Exchanges.BINANCE.value,
                        "symbol": None,
                        "side": None,
                        "amount": None,
                        "price": None
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Fault to find best pair path. Solution: {solution}")
                    time.sleep(10)
                    continue

                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         "USDT",
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BINANCE.value,
                        "second_exc": Exchanges.BINANCE.value,
                        "symbol": self.best_pair_on_binance["token"],
                        "side": self.trade_side.value,
                        "amount": None,
                        "price": self.best_pair_on_binance["price_binance"]
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                if self.main_exchange == Exchanges.BINANCE:
                    self.start_usdt_balance = self.trade_execution.get_binance_usdt_amount()

                external_address_status = self.trade_execution.checking_external_address(self.current_exchange, self.best_pair_on_binance["token"])
                await send_check_pair_message(self.dp,
                                              pair=self.best_pair_on_binance["token"],
                                              exc=Exchanges.BYBIT.value,
                                              status=external_address_status)
                if not external_address_status:
                    continue

                amount = float(amount)/float(self.best_pair_on_binance["price_binance"])

                # Создание решения по исполнению ордера
                solution = {
                    "first_exc": Exchanges.BINANCE.value,
                    "second_exc": Exchanges.BINANCE.value,
                    "symbol": self.best_pair_on_binance["token"],
                    "side": self.trade_side.value,
                    "amount": amount,
                    "price": self.best_pair_on_binance["price_binance"]
                }

                # Исполнение ордера с выводом статуса
                status_order = self.trade_execution.execute_trade(solution=solution)

                # Изменение показателей по итогам ордера
                if status_order:
                    self.trade_status = TradeStatus.IN_PROCESS
                    self.trade_side = TradeSide.WITHDRAW

                await send_buy_message(
                    dp=self.dp,
                    solution=solution,
                    trade_status=status_order
                )

            elif status == "buy-bybit":
                start_bal = round(float(self.trade_execution.get_bybit_usdt_amount()), 3)
                if self.main_exchange == Exchanges.BYBIT:
                    if not self.status_cycle:
                        await send_start_cycle_message(dp=self.dp, start_bal=start_bal)
                        self.status_cycle = True

                self.best_pair_on_bybit, pair_status = await self.pairs_execution.get_pair_path(self.current_exchange, amount_usdt=start_bal)

                if self.best_pair_on_bybit is None or not pair_status:
                    solution = {
                        "first_exc": Exchanges.BYBIT.value,
                        "second_exc": Exchanges.BYBIT.value,
                        "symbol": None,
                        "side": None,
                        "amount": None,
                        "price": None
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Fault to find best pair path. Solution: {solution}")
                    time.sleep(10)
                    continue

                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         "USDT",
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BYBIT.value,
                        "second_exc": Exchanges.BYBIT.value,
                        "symbol": self.best_pair_on_bybit["token"],
                        "side": self.trade_side.value,
                        "amount": None,
                        "price": self.best_pair_on_bybit["price_bybit"]
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                if self.main_exchange == Exchanges.BYBIT:
                    self.start_usdt_balance = self.trade_execution.get_bybit_usdt_amount()

                external_address_status = self.trade_execution.checking_external_address(self.current_exchange, self.best_pair_on_bybit["token"])
                await send_check_pair_message(self.dp,
                                              pair=self.best_pair_on_bybit["token"],
                                              exc=Exchanges.BYBIT.value,
                                              status=external_address_status)
                if not external_address_status:
                    continue

                amount = (float(amount) - 1) / float(self.best_pair_on_bybit["price_bybit"])
                # Создание решения по исполнению ордера
                solution = {
                    "first_exc": Exchanges.BYBIT.value,
                    "second_exc": Exchanges.BYBIT.value,
                    "symbol": self.best_pair_on_bybit["token"],
                    "side": self.trade_side.value,
                    "amount": amount,
                    "price": self.best_pair_on_bybit["price_bybit"]
                }

                # # Исполнение ордера с выводом статуса
                # status_order = self.trade_execution.execute_trade(solution=solution)
                #
                # # Изменение показателей по итогам ордера
                # if status_order:
                #     self.trade_status = TradeStatus.IN_PROCESS
                #     self.trade_side = TradeSide.WITHDRAW
                #
                # await send_buy_message(
                #     dp=self.dp,
                #     solution=solution,
                #     trade_status=status_order
                # )

            elif status == "sell-binance":
                token_symbol = self.best_pair_on_bybit["token"].replace("/USDT", "")
                balance = self.trade_execution.get_balances()

                if token_symbol not in balance["binance"].keys():
                    time.sleep(5)
                    continue
                elif token_symbol == "ETH":
                    if float(balance["binance"][token_symbol]) < 0.00015:
                        time.sleep(5)
                        continue
                elif token_symbol == "BNB":
                    if float(balance["binance"][token_symbol]) < 0.0015:
                        time.sleep(5)
                        continue
                elif float(balance["binance"][token_symbol]) < 20:
                    time.sleep(5)
                    continue

                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         self.best_pair_on_bybit["token"].replace("/USDT", ""),
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BINANCE.value,
                        "second_exc": Exchanges.BINANCE.value,
                        "symbol": self.best_pair_on_bybit["token"],
                        "side": self.trade_side.value,
                        "amount": None,
                        "price": self.best_pair_on_bybit["price_bybit"]
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                solution = {
                    "first_exc": Exchanges.BINANCE.value,
                    "second_exc": Exchanges.BINANCE.value,
                    "symbol": self.best_pair_on_bybit["token"],
                    "side": self.trade_side.value,
                    "amount": amount,
                    "price": self.best_pair_on_bybit["price_binance"]
                }

                # # Исполнение ордера с выводом статуса
                # status_order = self.trade_execution.execute_trade(solution=solution)

                status_order = True
                # Изменение показателей по итогам ордера
                if status_order:
                    self.trade_status = TradeStatus.IN_PROCESS
                    self.trade_side = TradeSide.BUY
                    # self.trade_status = TradeStatus.IN_PROCESS
                    # self.trade_side = TradeSide.WITHDRAW

                # await send_sell_message(
                #     dp=self.dp,
                #     solution=solution,
                #     trade_status=status_order
                # )
                if self.main_exchange == Exchanges.BINANCE:
                    time.sleep(5)

                    self.finish_usdt_balance = self.trade_execution.get_binance_usdt_amount()
                    await self._calculate_results(pair=solution["symbol"],
                                                  start_exc="bybit",
                                                  finish_exc="binance")
                    self.start_usdt_balance = 0
                    self.finish_usdt_balance = 0

                    finish_bal = self.trade_execution.get_binance_usdt_amount()
                    await send_stop_cycle_message(dp=self.dp, finish_bal=finish_bal)
                    self.status_cycle = False

            elif status == "sell-bybit":
                token_symbol = self.best_pair_on_binance["token"].replace("/USDT", "")
                balance = self.trade_execution.get_balances()

                if token_symbol not in balance["bybit"].keys():
                    time.sleep(5)
                    continue
                elif token_symbol == "ETH":
                    if float(balance["bybit"][token_symbol]) < 0.00015:
                        time.sleep(5)
                        continue
                elif token_symbol == "BNB":
                    if float(balance["bybit"][token_symbol]) < 0.0015:
                        time.sleep(5)
                        continue
                elif float(balance["bybit"][token_symbol]) < 20:
                    time.sleep(5)
                    continue

                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         self.best_pair_on_binance["token"].replace("/USDT", ""),
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BYBIT.value,
                        "second_exc": Exchanges.BYBIT.value,
                        "symbol": self.best_pair_on_binance["token"],
                        "side": self.trade_side.value,
                        "amount": None,
                        "price": self.best_pair_on_binance["price_bybit"]
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                # Создание решения по исполнению ордера
                solution = {
                    "first_exc": Exchanges.BYBIT.value,
                    "second_exc": Exchanges.BYBIT.value,
                    "symbol": self.best_pair_on_binance["token"],
                    "side": self.trade_side.value,
                    "amount": amount,
                    "price": self.best_pair_on_binance["price_bybit"]
                }

                # # Исполнение ордера с выводом статуса
                status_order = self.trade_execution.execute_trade(solution=solution)

                # status_order = True
                # Изменение показателей по итогам ордера
                if status_order:
                    self.trade_status = TradeStatus.IN_PROCESS
                    self.trade_side = TradeSide.WITHDRAW
                    # self.trade_status = TradeStatus.IN_PROCESS
                    # self.trade_side = TradeSide.BUY

                await send_sell_message(
                    dp=self.dp,
                    solution=solution,
                    trade_status=status_order
                )
                if self.main_exchange == Exchanges.BYBIT:
                    time.sleep(5)
                    self.finish_usdt_balance = self.trade_execution.get_bybit_usdt_amount()
                    await self._calculate_results(pair=solution["symbol"],
                                                  start_exc="binance",
                                                  finish_exc="bybit")
                    self.start_usdt_balance = 0
                    self.finish_usdt_balance = 0

                    finish_bal = self.trade_execution.get_binance_usdt_amount()
                    await send_stop_cycle_message(dp=self.dp, finish_bal=finish_bal)
                    self.status_cycle = False

            elif status == "withdraw-binance":
                # self.best_pair_on_binance = {
                #     "token": "USDT/USDT",
                #     "price_binance": 0,
                #     "price_bybit": 0
                # }
                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         self.best_pair_on_binance["token"].replace("/USDT", ""),
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BINANCE.value,
                        "second_exc": Exchanges.BYBIT.value,
                        "symbol": self.best_pair_on_bybit["token"],
                        "amount": None,
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                solution = {
                    "first_exc": Exchanges.BINANCE.value,
                    "second_exc": Exchanges.BYBIT.value,
                    "symbol": self.best_pair_on_binance["token"],
                    "amount": round(float(amount), 4),
                }

                # Исполнение перевода Binance -> Bybit с выводом статуса
                status_order = self.trade_execution.execute_trade(solution=solution)

                # Изменение показателей по итогам ордера
                if status_order:
                    time.sleep(30)
                    self.trade_status = TradeStatus.IN_PROCESS
                    self.trade_side = TradeSide.SELL
                    self.current_exchange = Exchanges.BYBIT

                await send_withdraw_message(
                    dp=self.dp,
                    solution=solution,
                    trade_status=status_order
                )

            elif status == "withdraw-bybit":
                self.best_pair_on_bybit = {
                    "token": "USDT/USDT",
                    "price_binance": 0,
                    "price_bybit": 0
                }
                amount, balance_status = self.trade_execution.get_amount(self.current_exchange,
                                                                         self.best_pair_on_bybit["token"].replace("/USDT", ""),
                                                                         self.amount,
                                                                         self.fix_amount)

                if not balance_status:
                    solution = {
                        "first_exc": Exchanges.BYBIT.value,
                        "second_exc": Exchanges.BINANCE.value,
                        "symbol": self.best_pair_on_bybit["token"],
                        "amount": None,
                    }
                    date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                    print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Balance status is False. Solution: {solution}")
                    continue

                solution = {
                    "first_exc": Exchanges.BYBIT.value,
                    "second_exc": Exchanges.BINANCE.value,
                    "symbol": self.best_pair_on_bybit["token"],
                    "amount": round(float(amount), 4),
                }

                # Исполнение перевода Bybit -> Binance с выводом статуса
                status_order = self.trade_execution.execute_trade(solution=solution)

                # Изменение показателей по итогам ордера
                if status_order:
                    time.sleep(30)
                    self.trade_status = TradeStatus.IN_PROCESS
                    self.trade_side = TradeSide.SELL
                    self.current_exchange = Exchanges.BINANCE

                await send_withdraw_message(
                    dp=self.dp,
                    solution=solution,
                    trade_status=status_order
                )

            else:
                break

            if status_order:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Success. Solution: {solution}")
            else:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Arbitrage {date}] Arbitrage path '{status}' - Fault. Solution: {solution}")
                # self.trade_status = TradeStatus.ERROR

    async def _calculate_results(self, pair: str, start_exc: str, finish_exc: str):
        """
        Расчёт итогов
        :param start_exc: Начальная биржа
        :param finish_exc: Конечная биржа
        :param pair: Торговая пара
        :return:
        """
        try:
            if self.start_usdt_balance == 0 or self.finish_usdt_balance == 0:
                date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
                print(f"[SYS Arbitrage {date}] Calculate results - Error. Don't have balances data.")
                return

            profit = round(float(self.finish_usdt_balance) - float(self.start_usdt_balance), 3)

            await send_result_message(dp=self.dp,
                                      pair=pair,
                                      start_exc=start_exc,
                                      finish_exc=finish_exc,
                                      start_balance=self.start_usdt_balance,
                                      finish_balance=self.finish_usdt_balance,
                                      profit=profit)

        except Exception as ex:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Calculate results - Error:\n{str(ex)}")
            return

    def _get_status_command(self):
        if self.trade_status == TradeStatus.WAIT:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] New status: buy-{self.current_exchange.value}")
            return f"buy-{self.current_exchange.value}"

        elif self.trade_status == TradeStatus.IN_PROCESS:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] New status: {self.trade_side.value}-{self.current_exchange.value}")
            return f"{self.trade_side.value}-{self.current_exchange.value}"

        else:
            date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
            print(f"[SYS Arbitrage {date}] Stop Arbitrage")
            self.trade_status = TradeStatus.ERROR
            return "stop"


if __name__ == '__main__':
    print(TradeSide.BUY.value)
