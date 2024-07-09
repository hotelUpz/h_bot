# import numpy as np
# import talib
# from settings import ema_short_period, ema_long_period, rsi_period
# from exchange_info import get_klines

# async def process_kline_data(kline_data, recent_klines, trends_dict, symbol):
#     open_time = kline_data['t']
#     open_price = float(kline_data['o'])
#     high_price = float(kline_data['h'])
#     low_price = float(kline_data['l'])
#     close_price = float(kline_data['c'])
#     volume = float(kline_data['v'])

#     recent_klines.append([open_time, open_price, high_price, low_price, close_price, volume])

#     if len(recent_klines) > ema_long_period:
#         recent_klines.pop(0)

#     if len(recent_klines) >= ema_long_period:
#         close_prices = np.array([kline[4] for kline in recent_klines])
#         rsi = calculate_rsi(close_prices, rsi_period)

#         # Найти последнее пересечение EMA
#         ema_cross = await find_last_ema_cross(close_prices)

#         current_rsi = rsi[-1]
#         current_close = close_prices[-1]

#         # Determine trend
#         trend = "None"
#         if ema_cross == "upward":
#             trend = "Uptrend"
#         elif ema_cross == "downward":
#             trend = "Downtrend"

#         trends_dict[symbol] = trend

#         print(f"Current trend for {symbol} at price {current_close}: {trend}")

#         if ema_cross == "upward" and current_rsi < 30:
#             print(f"Buy signal for {symbol} at price {current_close} with RSI {current_rsi}")
#         elif ema_cross == "downward" and current_rsi > 70:
#             print(f"Sell signal for {symbol} at price {current_close} with RSI {current_rsi}")

# async def process_historical_klines(recent_klines, trends_dict, symbol, rsi_period=14):
#     if len(recent_klines) >= ema_long_period:
#         close_prices = np.array([kline[4] for kline in recent_klines])
#         rsi = calculate_rsi(close_prices, rsi_period)

#         # Найти последнее пересечение EMA
#         ema_cross = await find_last_ema_cross(close_prices)

#         current_rsi = rsi[-1]
#         current_close = close_prices[-1]

#         # Determine trend
#         trend = "None"
#         if ema_cross == "upward":
#             trend = "Uptrend"
#         elif ema_cross == "downward":
#             trend = "Downtrend"

#         trends_dict[symbol] = trend

#         print(f"Initial trend for {symbol} at price {current_close}: {trend}")

#         if ema_cross == "upward" and current_rsi < 30:
#             print(f"Initial buy signal for {symbol} at price {current_close} with RSI {current_rsi}")
#         elif ema_cross == "downward" and current_rsi > 70:
#             print(f"Initial sell signal for {symbol} at price {current_close} with RSI {current_rsi}")

# def calculate_rsi(close_prices, timeperiod=14):
#     return talib.RSI(close_prices, timeperiod)

# def calculate_ema(close_prices, timeperiod):
#     return talib.EMA(close_prices, timeperiod)

# async def fetch_and_process_symbol(session, symbol, recent_klines_dict, trends_dict):
#     recent_klines = await get_klines(session, symbol, "1m", 100)  # Example using 1-minute interval
#     recent_klines_dict[symbol] = recent_klines.tolist()
#     await process_historical_klines(recent_klines_dict[symbol], trends_dict, symbol)


# async def find_last_ema_cross(prices):
#     # Инвертируем массив цен
#     #prices_reversed = np.flip(prices)

#     # Вычисляем EMA для инвертированного массива
#     ema_short = talib.EMA(prices, timeperiod=ema_short_period)
#     ema_long = talib.EMA(prices, timeperiod=ema_long_period)

#     # Перебор значений начинается с самого раннего периода доступности EMA
#     for i in range(len(prices)-1, 1, -1):
#         current_short_ema = ema_short[i]
#         current_long_ema = ema_long[i]
#         previous_short_ema = ema_short[i - 1]
#         previous_long_ema = ema_long[i - 1]

#         # Проверяем пересечение вверх
#         if previous_short_ema < previous_long_ema and current_short_ema > current_long_ema:
#             return "upward"

#         # Проверяем пересечение вниз
#         if previous_short_ema > previous_long_ema and current_short_ema < current_long_ema:
#             return "downward"

#     return "no cross"





    # async def get_all_symbols(self, session):
    #     url = f"{BASE_URL}/fapi/v1/exchangeInfo"
    #     async with session.get(url) as response:
    #         data = await response.json()
    #         return [symbol['symbol'] for symbol in data['symbols']]





# async def collect_signals(self):
#     self.handle_messagee("Начало поиска ")
#     start_time = int(time.time() * 1000)
#     signal_data = await self.fetch_all_klines(self.candidate_symbols_list, self.interval, self.klines_limit)
    
#     symbol_info = await self.get_exchange_info()
#     signals_answ_list = []

#     for result in signal_data:
#         symbol, data = result
#         precisions = self.get_precisions(symbol, symbol_info)

#         if precisions:
#             signal_info = self.get_signal_engine_(symbol, data)

#             if signal_info[1] == 0:
#                 signals_answ_list.append({
#                     "symbol": signal_info[0],
#                     "cur_signal": signal_info[1],
#                     "firts_signal": 1,
#                     "cur_price": signal_info[2][-1][4],
#                     "enter_price_1": signal_info[2][-1][4],
#                     "enter_price_2": 0,
#                     # "klines_data": signal_info[2],
#                     "is_close_kline": False,
#                     "quantity_precision": precisions[0],
#                     "price_precession": precisions[1],
#                     "min_notional": precisions[3],
#                     "in_position_1": False,
#                     "in_position_2": False,
#                     "position_1_side": None,
#                     "posicion_2_side": None,
#                     "close_pos_1_true": False,
#                     "close_pos_2_true": False,
#                     "is_total_close_true": False,
#                     "side_1": None,
#                     "side_2": None,
#                     "qty_1": 0,
#                     "qty_2": 0,
#                     "sl_1_pos_rate": self.sl_1_pos_rate/ 100,
#                     "tp_1_pos_rate": self.tp_1_pos_rate/ 100,
#                     "sl_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[0].strip()),
#                     "tp_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[1].strip()),
#                     "sl_price_1_pos": 0,
#                     "tp_price_1_pos": 0,
#                     "current_step_counter": self.current_step_counter,
#                     "position_1_averaging_counter": self.position_1_averaging_counter,                     
#                 })

#     delta_time = int((int(time.time() * 1000) - start_time) / 1000)
#     self.handle_signal_search_end(delta_time, signals_answ_list)
#     return signals_answ_list


# await self.connect_to_websocket(self.candidate_symbols_list, recent_klines_dict, trends_dict)

            # if ema_cross == 1:
            #     signal = 1
            #     # print(f"Buy signal for {symbol} at price {current_close}")
            # elif ema_cross == -1:
            #     signal = -1
            #     # print(f"Sell signal for {symbol} at price {current_close}")


    # def open_1_pos_signal_handler(self, symbol_item):
    #     try:
    #         if not symbol_item.get("in_position_1") and not symbol_item.get("in_position_2"):   
    #             if symbol_item.get("signal") == 1:
    #                 symbol_item["position_1_side"] = "LONG"  
    #                 symbol_item["side_1"] = "BUY"
    #             elif symbol_item.get("signal") == -1:
    #                 symbol_item["position_1_side"] = "SHORT"  
    #                 symbol_item["side_1"] = "SELL"
    #     except Exception as ex:
    #         print(ex)
    #     return symbol_item

    
    # def open_2_pos_signal_handler(self, symbol_item):
    #     is_open_2_pos_true = False
    #     try:
    #         if symbol_item.get("in_position_1") and not symbol_item.get("in_position_2"):
    #             if symbol_item.get("signal"): 
    #                 is_open_2_pos_true = True           
    #                 if symbol_item.get("position_1_side") == 'LONG':
    #                     symbol_item["position_2_side"] = "SHORT"
    #                     symbol_item["side_2"] = "SELL"
    #                 elif symbol_item.get("position_1_side") == 'SHORT':
    #                     symbol_item["position_2_side"] = "LONG"
    #                     symbol_item["side_2"] = "BUY"
    #     except Exception as ex:
    #         print(ex)

    #     return symbol_item, is_open_2_pos_true