# (USDT-((USDT*buyPrice-USDT*buyPrice*0,001-comBEP20)*sellPrice
#     -
# (USDT*buyPrice-USDT*buyPrice*0,001-comBEP20)*sellPrice*0,001-comBEP20))*(-1)

BTC_count = 0.2
LTC_BTC_P = 138.23611
LTC_ETH_P = 2.52871
BTC_ETH_P = 0.01894

sellPrice = 0.574
TAKER_COM = 0.001

comBEP20 = 0.3
comETH = 4

# Trade BTC to LTC
ltc_part_1 = BTC_count*LTC_BTC_P - BTC_count*LTC_BTC_P*TAKER_COM
# Trade LTC to ETH
ltc_part_2 = ltc_part_1/LTC_ETH_P - ltc_part_1/LTC_ETH_P*0.001
# Trade ETH to BTC
ltc_part_3 = ltc_part_2*BTC_ETH_P - ltc_part_2*BTC_ETH_P*0.001


print(f"BTC LTC Start value: {BTC_count}")
print(f"BTC LTC Result value: {ltc_part_3}")
print(f"BTC LTC Percent: {(ltc_part_3/BTC_count - 1) * 100} %\n")

USDT_count = 200
SOL_USDT_B = 20.83
SOL_USDT_S = 20.82
SOL_ETH_P = None
SOL_BTC_P = 0.00076
BTC_USDT_P = 27231.63
ETH_USDT_P = None

# sellPrice = 0.574
TAKER_COM = 0.001

comBEP20 = 0.3
comETH = 4

# Trade USDT to SOL
sol_part_1 = USDT_count*SOL_USDT_B - USDT_count*SOL_USDT_B*TAKER_COM
# Trade SOL to BTC
sol_part_2 = sol_part_1/SOL_BTC_P - sol_part_1/SOL_BTC_P*TAKER_COM
# Trade BTC to USDT
sol_part_3 = sol_part_2/BTC_USDT_P - sol_part_2/BTC_USDT_P*TAKER_COM


print(f"SOL Start value: {USDT_count}")
print(f"SOL Result value: {sol_part_3}")
print(f"SOL Percent: {(sol_part_3/USDT_count - 1) * 100} %\n")

# part_1 = USDT/buyPrice-0.001*USDT/buyPrice
# part_1_com = part_1 - comETH/buyPrice
# part_2 = part_1_com*sellPrice - part_1_com*sellPrice*0.001 - comBEP20
#
# formula_bsc = part_2 - USDT
#
# # formula_eth = (USDT-((USDT*buyPrice-USDT*buyPrice*0.001-comETH)*sellPrice - (USDT*buyPrice-USDT*buyPrice*0.001)*sellPrice*0.001-comBEP20))*(-1)
# percent = ((sellPrice - buyPrice) / buyPrice) * 100
#
# print(f"part 1 = {part_1}")
# print(f"part_1_com = {part_1_com}")
# print(f"part 2 = {part_2}")
# print(f"formula_bsc = {formula_bsc}")
# # print(f"formula_eth = {formula_eth}")
# print(f"percent = {percent}")

