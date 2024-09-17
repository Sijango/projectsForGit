import json


CONFIG_PATH = "src/config.json"
BALANCE_PATH = "src/balance.txt"

BINANCE_RATE_URL = "https://api.binance.com/api/v3/ticker/price"
BYBIT_RATE_URL = "https://api.bybit.com/v2/public/tickers"

config = json.load(open(CONFIG_PATH, "r", encoding="utf-8"))

TOKEN = config["token"]
CHAT_ID = config["chat_id"]
MESSAGE_ID = config["message_id"]
CLIENT = config["client"]
CONTACT = config["contact"]

COM_BEP20 = config["comBEP20"]
COM_ETH = config["comETH"]
PERCENT = config["percent"]

NETWORK = config["network"]
COIN_TO_TRANSFER = config["coin_to_transfer"]

BSC_GAS_FEE = config["fees"]["bsc_gas_fee"]
BSC_GAS_FEE_USDT = BSC_GAS_FEE * config["fees"]["bsc_gas_fee_usdt"]
BUY_SELL_COMMISSION = config["fees"]["buy_sell_commission"]

ADDED_PAIRS = config["added_pairs"]
PAIR_FEES = config["pair_fees"]

BINANCE_EXCHANGE_DATA = config["binance_exchange_data"]
BYBIT_EXCHANGE_DATA = config["bybit_exchange_data"]


VIEW_REPLACES = {
    "binance": "🚸 Binance",
    "bybit": "✴️ Bybit",
    "buy": "🛍️ Покупка",
    "sell": "💰 Продажа",
    "withdraw": "✈️ Перевод",
    "binance_icon": "🚸",
    "bybit_icon": "✴️",
    "buy_icon": "🛍️",
    "sell_icon": "💰",
    "withdraw_icon": "✈️",
    "sys_icon": "🌀",
    "bal_icon": "🏦",
    "yes_icon": "✅",
    "no_icon": "❌",
    "error_icon": "❗️❗️❗️",
    "new_icon": "🆕",
    "best_icon": "💼"
}
