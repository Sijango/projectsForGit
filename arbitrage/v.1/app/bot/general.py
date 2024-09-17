import time
import datetime
from typing import Dict
from aiogram import Dispatcher, types

import config
from app.bot import messages

TIME_SLEEP = 1.5
TIME_SLEEP_ERROR = 40


async def start_message(message: types.Message):
    topic = message.message_thread_id

    await message.reply(topic)


async def start_bot_message(dp: Dispatcher):
    message = messages.START_MESSAGE.format(sys_icon=config.VIEW_REPLACES["sys_icon"],
                                            client=config.CLIENT)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send start message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_buy_message(dp: Dispatcher, solution: Dict[str, any], trade_status: bool):
    status = config.VIEW_REPLACES["no_icon"]
    if trade_status:
        status = config.VIEW_REPLACES["yes_icon"]

    message = messages.PROCESS_MESSAGE.format(process_icon=config.VIEW_REPLACES["buy_icon"],
                                              client=config.CLIENT,
                                              process=config.VIEW_REPLACES["buy"],
                                              symbol=solution["symbol"],
                                              status=status,
                                              exc=config.VIEW_REPLACES[solution["first_exc"]],
                                              price=solution["price"],
                                              amount=solution["amount"])

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send buy message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_sell_message(dp: Dispatcher, solution: Dict[str, any], trade_status: bool):
    status = config.VIEW_REPLACES["no_icon"]
    if trade_status:
        status = config.VIEW_REPLACES["yes_icon"]

    message = messages.PROCESS_MESSAGE.format(process_icon=config.VIEW_REPLACES["sell_icon"],
                                              client=config.CLIENT,
                                              process=config.VIEW_REPLACES["sell"],
                                              symbol=solution["symbol"],
                                              status=status,
                                              exc=config.VIEW_REPLACES[solution["first_exc"]],
                                              price=solution["price"],
                                              amount=solution["amount"])

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send sell message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_withdraw_message(dp: Dispatcher, solution: Dict[str, any], trade_status: bool):
    status = config.VIEW_REPLACES["no_icon"]
    if trade_status:
        status = config.VIEW_REPLACES["yes_icon"]

    first_exc = config.VIEW_REPLACES[solution["first_exc"]]
    second_exc = config.VIEW_REPLACES[solution["second_exc"]]

    message = messages.WITHDRAW_MESSAGE.format(process_icon=config.VIEW_REPLACES["withdraw_icon"],
                                               client=config.CLIENT,
                                               process=config.VIEW_REPLACES["withdraw"],
                                               symbol=solution["symbol"],
                                               status=status,
                                               first_exc=first_exc,
                                               second_exc=second_exc,
                                               amount=solution["amount"])

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send withdraw message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_error_message(dp: Dispatcher, error: str):
    message = messages.ERROR_MESSAGE.format(error_icon=config.VIEW_REPLACES["error_icon"],
                                            client=config.CLIENT,
                                            error=error)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send error message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_new_pair_message(dp: Dispatcher, data: Dict[str, any], access: bool, income: float, percent: float):
    if data is None:
        data = {
            "pair": None,
            "first_exc": None,
            "first_cast": None,
            "second_exc": None,
            "second_cast": None
        }
    if access:
        pair_status = "✅"
    else:
        pair_status = "❌"

    message = messages.NEW_PAIR_MESSAGE.format(process_icon=config.VIEW_REPLACES["new_icon"],
                                               client=config.CLIENT,
                                               pair=data["pair"],
                                               first_exc=config.VIEW_REPLACES[data["first_exc"]],
                                               first_cast=data["first_cast"],
                                               second_exc=config.VIEW_REPLACES[data["second_exc"]],
                                               second_cast=data["second_cast"],
                                               income=round(income, 5),
                                               percent=round(percent, 5),
                                               pair_status=pair_status)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send new pair message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_check_pair_message(dp: Dispatcher, pair: str, exc: str, status: bool):
    if status:
        message = messages.CHECK_PAIR_MESSAGE.format(process_icon=config.VIEW_REPLACES["yes_icon"],
                                                     client=config.CLIENT,
                                                     pair=pair,
                                                     exc=config.VIEW_REPLACES[exc],
                                                     status_check=config.VIEW_REPLACES["yes_icon"])
    else:
        message = messages.CHECK_PAIR_MESSAGE.format(process_icon=config.VIEW_REPLACES["no_icon"],
                                                     client=config.CLIENT,
                                                     pair=pair,
                                                     exc=config.VIEW_REPLACES[exc],
                                                     status_check=config.VIEW_REPLACES["no_icon"])

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send check pair message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_balance_message(dp: Dispatcher, balances: Dict[str, any]):
    binance_balance = []
    for key, value in balances["binance"].items():
        binance_balance.append(f"{key}: {value}")

    bybit_balance = []
    for key, value in balances["bybit"].items():
        bybit_balance.append(f"{key}: {value}")

    message = messages.BALANCE_MESSAGE.format(process_icon=config.VIEW_REPLACES["bal_icon"],
                                              client=config.CLIENT,
                                              binance=config.VIEW_REPLACES["binance"],
                                              binance_balance="\n".join(binance_balance),
                                              bybit=config.VIEW_REPLACES["bybit"],
                                              bybit_balance="\n".join(bybit_balance))

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send balance message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_result_message(dp: Dispatcher,
                              pair: str,
                              start_exc: str,
                              finish_exc: str,
                              start_balance: float,
                              finish_balance: float,
                              profit: float):
    message = messages.RESULT_MESSAGE.format(process_icon=config.VIEW_REPLACES["bal_icon"],
                                             client=config.CLIENT,
                                             best_icon=config.VIEW_REPLACES["best_icon"],
                                             pair=pair,
                                             withdraw_icon=config.VIEW_REPLACES["withdraw_icon"],
                                             start_exc=config.VIEW_REPLACES[start_exc],
                                             finish_exc=config.VIEW_REPLACES[finish_exc],
                                             start_icon=config.VIEW_REPLACES["sell_icon"],
                                             start_balance=start_balance,
                                             finish_icon=config.VIEW_REPLACES["sell_icon"],
                                             finish_balance=finish_balance,
                                             profit_icon=config.VIEW_REPLACES["bal_icon"],
                                             profit=profit)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Send result message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_start_cycle_message(dp: Dispatcher, start_bal: float):
    message = messages.START_CYCLE.format(sys_icon=config.VIEW_REPLACES["sys_icon"],
                                          start_bal=start_bal)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Start cycle message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


async def send_stop_cycle_message(dp: Dispatcher, finish_bal: float):
    message = messages.STOP_CYCLE.format(sys_icon=config.VIEW_REPLACES["sys_icon"],
                                         finish_bal=finish_bal)

    time.sleep(TIME_SLEEP)
    try:
        await dp.bot.send_message(
            chat_id=config.CHAT_ID,
            text=message,
            reply_to_message_id=config.MESSAGE_ID,
            disable_notification=True,
        )
    except:
        date = datetime.datetime.now().strftime("%d.%b.%Y %H:%M")
        print(f"[SYS Aiogram - send message {date}] Stop cycle message - Flood control. Sleep {TIME_SLEEP_ERROR} sec.")
        time.sleep(TIME_SLEEP_ERROR)


def register_messages_general(dp: Dispatcher):
    dp.register_message_handler(start_message, commands='start')

