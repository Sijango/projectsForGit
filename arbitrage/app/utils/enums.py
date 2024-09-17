import enum


class Exchanges(enum.Enum):
    BINANCE = "binance"
    BYBIT = "bybit"


class TradeSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"
    WITHDRAW = "withdraw"


class TradeStatus(enum.Enum):
    WAIT = 0
    IN_PROCESS = 1
    ERROR = 2

