START_MESSAGE = """
{sys_icon} Запускаем клиента {client}
"""

PROCESS_MESSAGE = """
{process_icon} Клиент: {client}
{process} пары: {symbol}

Ордер прошёл: {status}
Биржа: {exc}
Цена: {price}
Кол-во: {amount}
"""

WITHDRAW_MESSAGE = """
{process_icon} Клиент: {client}
{process} пары: {symbol}

Ордер прошёл: {status}
{first_exc} -> {second_exc}
Кол-во: {amount}
"""

ERROR_MESSAGE = """
{error_icon} Остановка работы бота клиента {client} по причине:
{error}
"""

NEW_PAIR_MESSAGE = """
{process_icon} Клиент: {client}

Найдена новая пара: {pair}
Цена на площадке {first_exc}: {first_cast}
Цена на площадке {second_exc}: {second_cast}

Возможная прибыль: {income}
Процент разницы: {percent}
Пара допущена: {pair_status}
"""

CHECK_PAIR_MESSAGE = """
{process_icon} Клиент: {client}

Торговая пара: {pair}
Биржа-получатель: {exc}
Возможность для перевода: {status_check}
"""

BALANCE_MESSAGE = """
{process_icon} Клиент: {client}

Баланс на бирже {binance}:
{binance_balance}

Баланс на бирже {bybit}:
{bybit_balance}
"""

RESULT_MESSAGE = """
{process_icon} Клиент: {client}

{best_icon} Лучшая пара: {pair}
{withdraw_icon} Направление: {start_exc} -> {finish_exc}

{start_icon} Баланс на старте: {start_balance} USDT
{finish_icon} Баланс на выходе: {finish_balance} USDT
{profit_icon} Профит: {profit} USDT
"""

START_CYCLE = """
{sys_icon} Запуск цикла ({start_bal} USDT)
"""

STOP_CYCLE = """
{sys_icon} Завершение цикла ({finish_bal} USDT)
"""


if __name__ == '__main__':
    print(START_MESSAGE.format(client="123"))

