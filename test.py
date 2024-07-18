# # # import random
# # # from time import sleep 

# # # def foo(diversification_number):    
# # #     trade_li = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# # #     signals_stock = len(trade_li)
# # #     trade_litemp = []
# # #     trade_res = []

# # #     if signals_stock >= diversification_number:                            
# # #         step = diversification_number 
# # #     else:
# # #         step = signals_stock

# # #     for i in range(0, signals_stock, step):
# # #         trade_litemp = trade_li[i:step+i]
# # #         # print(trade_litemp)
# # #         # print(f"trade_litemp: {trade_litemp}")
# # #         cur_slice = random.randrange(0, len(trade_litemp)+1)
# # #         trade_res += trade_litemp[:cur_slice]
# # #         # print(f"trade_res: {trade_res}")

# # #         if len(trade_res) >= diversification_number:           
# # #             return True, trade_res
        
# # #         step = step - len(trade_res) if step > len(trade_res) else 1
# # #         # print(f"step: {step}")
# # #         # sleep(1)
        
# # #     if len(trade_res) > 0:            
# # #         return True, trade_res

# # #     return False, []

# # # diversification_number = 15
# # # for _ in range(10):
# # #     tr, lenn = foo(diversification_number)
# # #     print(lenn)
# # #     if len(lenn) > diversification_number:
# # #         print("Some mistake...")
# # # print("Ex!!")


# # # #     # remaining_signals = signals_stock  % diversification_number
        
# # # #     # if remaining_signals != 0:
# # # #     #     tradin_tail = remaining_signals-len(trade_res) if remaining_signals > len(trade_res) else remaining_signals
# # # #     #     cur_slice = random.randrange(1, tradin_tail+1)
# # # #     #     trade_res += trade_li[-tradin_tail: -cur_slice]


# # import random

# # def foo(diversification_number):    
# #     trade_li = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# #     signals_stock = len(trade_li)
# #     trade_res = []

# #     step = min(diversification_number, signals_stock)

# #     for i in range(0, signals_stock, step):
# #         trade_litemp = trade_li[i:step + i]
# #         cur_slice = random.randrange(0, len(trade_litemp) + 1)
# #         trade_res += trade_litemp[:cur_slice]

# #         if len(trade_res) >= diversification_number:
# #             return True, trade_res[:diversification_number]

# #         remaining_positions_needed = diversification_number - len(trade_res)
# #         step = min(max(remaining_positions_needed, 1), signals_stock - i - step)

# #     if len(trade_res) > 0:
# #         return True, trade_res

# #     return False, []

# # diversification_number = 28
# # for _ in range(3000):
# #     tr, lenn = foo(diversification_number)
# #     print(lenn)
# #     if len(lenn) > diversification_number:
# #         print("Some mistake...")
# # print("Ex!!")

# import numpy as np
# import talib

# # Данные
# close_prices = np.array([1.0279, 1.0282, 1.0279, 1.0265, 1.0254, 1.0253, 1.0255, 1.0253, 1.0262, 1.0265,
#  1.0256, 1.0257, 1.026,  1.0264, 1.0275])


# # # # Функция для вычисления EMA
# # def calculate_ema(close_prices, period):
# #     ema = np.zeros_like(close_prices)
# #     alpha = 1.6 / (period + 1)
# #     ema[0] = close_prices[0]
# #     for i in range(1, len(close_prices)):
# #         ema[i] = alpha * close_prices[i] + (1 - alpha) * ema[i-1]
# #     return ema

# def calculate_ema(prices, period):
#     return talib.EMA(prices, timeperiod=period)  

# # Вычисление EMA для периодов 5 и 10
# ema_short = calculate_ema(close_prices, 5)
# ema_long = calculate_ema(close_prices, 10)

# # Проверяем последние два значения EMA
# current_short_ema = ema_short[-1]
# current_long_ema = ema_long[-1]
# previous_short_ema = ema_short[-2]
# previous_long_ema = ema_long[-2]

# # Проверяем пересечение вверх
# if previous_short_ema < previous_long_ema and current_short_ema >= current_long_ema:
#     signal = 1  # Signal for buy

# # Проверяем пересечение вниз
# elif previous_short_ema > previous_long_ema and current_short_ema <= current_long_ema:
#     signal = -1  # Signal for sell
# else:
#     signal = 0  # No cross   

# # # Определение пересечения EMA
# # if ema_5[-1] > ema_10[-1] and ema_5[-2] < ema_10[-2]:
# #     signal = 1  # Сигнал на покупку (кроссовер вверх)
# # elif ema_5[-1] < ema_10[-1] and ema_5[-2] > ema_10[-2]:
# #     signal = -1  # Сигнал на продажу (кроссовер вниз)
# # else:
# #     signal = 0  # Нет сигнала

# # Результаты
# print("EMA 5:", ema_short)
# print("EMA 10:", ema_long)
# print("Signal:", signal)

# import time
# from time import sleep 

# s_time = time.time()
# sleep(3)

# print(time.time()- s_time)