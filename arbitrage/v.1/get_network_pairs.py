import ccxt
import json

import config
from app.arbitrage.exchanges import get_exchange

exchanges = get_exchange()
binance_exchange: ccxt.binance = exchanges["binance"]
bybit_exchange: ccxt.bybit = exchanges["bybit"]

NETWORK = "BEP20"


def get_pair(network=NETWORK):
    all_pairs_bybit = bybit_exchange.fetch_currencies()
    all_pairs_binance = binance_exchange.fetch_currencies()
    result_pairs_usdt = []
    result_pairs_btc = []
    result_pairs_eth = []

    with open("bybit.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pairs_bybit))

    with open("binance.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(all_pairs_binance))

    for coin_name in all_pairs_bybit.keys():
        if network in all_pairs_bybit[coin_name]["networks"].keys():
            result_pairs_usdt.append(coin_name + "USDT")
            result_pairs_btc.append(coin_name + "BTC")
            result_pairs_eth.append(coin_name + "ETH")

    return result_pairs_usdt, result_pairs_btc, result_pairs_eth


def check_on_binance(pair):
    try:
        order_book = binance_exchange.fetch_order_book(pair)
        if order_book:
            return True
        else:
            return False
    except:
        return False


def check_on_bybit(pair):
    try:
        order_book = bybit_exchange.fetch_order_book(pair)
        if order_book:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    pairs_usdt, pairs_btc, pairs_eth = get_pair()

    print("\nPairs on Bybit:")
    for pair in pairs_usdt:
        if check_on_bybit(pair):
            print(f"Pair USDT: {pair}")

    print("\nPairs on Binance:")
    for pair in pairs_btc:
        if check_on_binance(pair):
            print(f"Pair BTC: {pair}")

    for pair in pairs_eth:
        if check_on_binance(pair):
            print(f"Pair ETH: {pair}")
