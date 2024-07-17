# # import numpy as np
# # import talib
# # from settings import ema_short_period, ema_long_period, rsi_period
# # from exchange_info import get_klines

# # async def process_kline_data(kline_data, recent_klines, trends_dict, symbol):
# #     open_time = kline_data['t']
# #     open_price = float(kline_data['o'])
# #     high_price = float(kline_data['h'])
# #     low_price = float(kline_data['l'])
# #     close_price = float(kline_data['c'])
# #     volume = float(kline_data['v'])

# #     recent_klines.append([open_time, open_price, high_price, low_price, close_price, volume])

# #     if len(recent_klines) > ema_long_period:
# #         recent_klines.pop(0)

# #     if len(recent_klines) >= ema_long_period:
# #         close_prices = np.array([kline[4] for kline in recent_klines])
# #         rsi = calculate_rsi(close_prices, rsi_period)

# #         # Найти последнее пересечение EMA
# #         ema_cross = await find_last_ema_cross(close_prices)

# #         current_rsi = rsi[-1]
# #         current_close = close_prices[-1]

# #         # Determine trend
# #         trend = "None"
# #         if ema_cross == "upward":
# #             trend = "Uptrend"
# #         elif ema_cross == "downward":
# #             trend = "Downtrend"

# #         trends_dict[symbol] = trend

# #         print(f"Current trend for {symbol} at price {current_close}: {trend}")

# #         if ema_cross == "upward" and current_rsi < 30:
# #             print(f"Buy signal for {symbol} at price {current_close} with RSI {current_rsi}")
# #         elif ema_cross == "downward" and current_rsi > 70:
# #             print(f"Sell signal for {symbol} at price {current_close} with RSI {current_rsi}")

# # async def process_historical_klines(recent_klines, trends_dict, symbol, rsi_period=14):
# #     if len(recent_klines) >= ema_long_period:
# #         close_prices = np.array([kline[4] for kline in recent_klines])
# #         rsi = calculate_rsi(close_prices, rsi_period)

# #         # Найти последнее пересечение EMA
# #         ema_cross = await find_last_ema_cross(close_prices)

# #         current_rsi = rsi[-1]
# #         current_close = close_prices[-1]

# #         # Determine trend
# #         trend = "None"
# #         if ema_cross == "upward":
# #             trend = "Uptrend"
# #         elif ema_cross == "downward":
# #             trend = "Downtrend"

# #         trends_dict[symbol] = trend

# #         print(f"Initial trend for {symbol} at price {current_close}: {trend}")

# #         if ema_cross == "upward" and current_rsi < 30:
# #             print(f"Initial buy signal for {symbol} at price {current_close} with RSI {current_rsi}")
# #         elif ema_cross == "downward" and current_rsi > 70:
# #             print(f"Initial sell signal for {symbol} at price {current_close} with RSI {current_rsi}")

# # def calculate_rsi(close_prices, timeperiod=14):
# #     return talib.RSI(close_prices, timeperiod)

# # def calculate_ema(close_prices, timeperiod):
# #     return talib.EMA(close_prices, timeperiod)

# # async def fetch_and_process_symbol(session, symbol, recent_klines_dict, trends_dict):
# #     recent_klines = await get_klines(session, symbol, "1m", 100)  # Example using 1-minute interval
# #     recent_klines_dict[symbol] = recent_klines.tolist()
# #     await process_historical_klines(recent_klines_dict[symbol], trends_dict, symbol)


# # async def find_last_ema_cross(prices):
# #     # Инвертируем массив цен
# #     #prices_reversed = np.flip(prices)

# #     # Вычисляем EMA для инвертированного массива
# #     ema_short = talib.EMA(prices, timeperiod=ema_short_period)
# #     ema_long = talib.EMA(prices, timeperiod=ema_long_period)

# #     # Перебор значений начинается с самого раннего периода доступности EMA
# #     for i in range(len(prices)-1, 1, -1):
# #         current_short_ema = ema_short[i]
# #         current_long_ema = ema_long[i]
# #         previous_short_ema = ema_short[i - 1]
# #         previous_long_ema = ema_long[i - 1]

# #         # Проверяем пересечение вверх
# #         if previous_short_ema < previous_long_ema and current_short_ema > current_long_ema:
# #             return "upward"

# #         # Проверяем пересечение вниз
# #         if previous_short_ema > previous_long_ema and current_short_ema < current_long_ema:
# #             return "downward"

# #     return "no cross"





#     # async def get_all_symbols(self, session):
#     #     url = f"{BASE_URL}/fapi/v1/exchangeInfo"
#     #     async with session.get(url) as response:
#     #         data = await response.json()
#     #         return [symbol['symbol'] for symbol in data['symbols']]





# # async def collect_signals(self):
# #     self.handle_messagee("Начало поиска ")
# #     start_time = int(time.time() * 1000)
# #     signal_data = await self.fetch_all_klines(self.candidate_symbols_list, self.interval, self.klines_limit)
    
# #     symbol_info = await self.get_exchange_info()
# #     signals_answ_list = []

# #     for result in signal_data:
# #         symbol, data = result
# #         precisions = self.get_precisions(symbol, symbol_info)

# #         if precisions:
# #             signal_info = self.get_signal_engine_(symbol, data)

# #             if signal_info[1] == 0:
# #                 signals_answ_list.append({
# #                     "symbol": signal_info[0],
# #                     "cur_signal": signal_info[1],
# #                     "firts_signal": 1,
# #                     "cur_price": signal_info[2][-1][4],
# #                     "enter_price_1": signal_info[2][-1][4],
# #                     "enter_price_2": 0,
# #                     # "klines_data": signal_info[2],
# #                     "is_close_kline": False,
# #                     "quantity_precision": precisions[0],
# #                     "price_precession": precisions[1],
# #                     "min_notional": precisions[3],
# #                     "in_position_1": False,
# #                     "in_position_2": False,
# #                     "position_1_side": None,
# #                     "posicion_2_side": None,
# #                     "close_pos_1_true": False,
# #                     "close_pos_2_true": False,
# #                     "is_total_close_true": False,
# #                     "side_1": None,
# #                     "side_2": None,
# #                     "qty_1": 0,
# #                     "qty_2": 0,
# #                     "sl_1_pos_rate": self.sl_1_pos_rate/ 100,
# #                     "tp_1_pos_rate": self.tp_1_pos_rate/ 100,
# #                     "sl_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[0].strip()),
# #                     "tp_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[1].strip()),
# #                     "sl_price_1_pos": 0,
# #                     "tp_price_1_pos": 0,
# #                     "current_step_counter": self.current_step_counter,
# #                     "position_1_averaging_counter": self.position_1_averaging_counter,                     
# #                 })

# #     delta_time = int((int(time.time() * 1000) - start_time) / 1000)
# #     self.handle_signal_search_end(delta_time, signals_answ_list)
# #     return signals_answ_list


# # await self.connect_to_websocket(self.candidate_symbols_list, recent_klines_dict, trends_dict)

#             # if ema_cross == 1:
#             #     signal = 1
#             #     # print(f"Buy signal for {symbol} at price {current_close}")
#             # elif ema_cross == -1:
#             #     signal = -1
#             #     # print(f"Sell signal for {symbol} at price {current_close}")


#     # def open_1_pos_signal_handler(self, symbol_item):
#     #     try:
#     #         if not symbol_item.get("in_position_1") and not symbol_item.get("in_position_2"):   
#     #             if symbol_item.get("signal") == 1:
#     #                 symbol_item["position_1_side"] = "LONG"  
#     #                 symbol_item["side_1"] = "BUY"
#     #             elif symbol_item.get("signal") == -1:
#     #                 symbol_item["position_1_side"] = "SHORT"  
#     #                 symbol_item["side_1"] = "SELL"
#     #     except Exception as ex:
#     #         print(ex)
#     #     return symbol_item

    
#     # def open_2_pos_signal_handler(self, symbol_item):
#     #     is_open_2_pos_true = False
#     #     try:
#     #         if symbol_item.get("in_position_1") and not symbol_item.get("in_position_2"):
#     #             if symbol_item.get("signal"): 
#     #                 is_open_2_pos_true = True           
#     #                 if symbol_item.get("position_1_side") == 'LONG':
#     #                     symbol_item["position_2_side"] = "SHORT"
#     #                     symbol_item["side_2"] = "SELL"
#     #                 elif symbol_item.get("position_1_side") == 'SHORT':
#     #                     symbol_item["position_2_side"] = "LONG"
#     #                     symbol_item["side_2"] = "BUY"
#     #     except Exception as ex:
#     #         print(ex)

#     #     return symbol_item, is_open_2_pos_true


    
#     # def instruction_collector(self, symbol_item):
#     #     signal = symbol_item["firts_signal"]
#     #     cur_price = symbol_item["cur_price"]
#     #     current_step_counter = symbol_item["current_step_counter"]
#     #     position_1_averaging_counter = symbol_item["position_1_averaging_counter"]

#     #     pos_1_assets = None
#     #     pos_2_assets = None

#     #     open_pos_conditions_resp = self.open_2_pos_conditions(signal)
#     #     if open_pos_conditions_resp:
#     #         pos_1_assets = open_pos_conditions_resp
#     #         return None, pos_2_assets
        
#     #     close_1_pos_conditiond_resp = self.close_1_pos_conditiond(signal, cur_price)
#     #     if close_1_pos_conditiond_resp:
#     #         pos_1_assets = close_1_pos_conditiond_resp
#     #         return pos_1_assets, None
        
#     #     position_1_averaging_conditions_resp = self.position_1_averaging_conditions(cur_price, current_step_counter, position_1_averaging_counter)
#     #     if position_1_averaging_conditions_resp:
#     #         pos_1_assets, self.current_step_counter, self.position_1_averaging_counter = position_1_averaging_conditions_resp
#     #         if pos_1_assets:
#     #             return pos_1_assets, None
            
#     #     close_both_pos_conditiond_resp = self.close_both_pos_conditiond(cur_price, current_step_counter)
#     #     if close_both_pos_conditiond_resp:
#     #         pos_1_assets, pos_1_assets = close_both_pos_conditiond_resp
#     #         if pos_1_assets or pos_2_assets:
#     #             return pos_1_assets, pos_2_assets
            
#     #     return None, None

# # import numpy as np
# # import asyncio
# # from utils import UTILS

# # class SORT_DATA(UTILS):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.is_get_new_signal = False
# #         self.lock = asyncio.Lock()

# #     def symbol_data_reprocessing(self, symbol, signal, cur_price):  
# #         for i, symbol_item in enumerate(self.signals_data_list):            
# #             if symbol_item["symbol"] == symbol:
# #                 try:
# #                     self.signals_data_list[i]['cur_price'] = cur_price
# #                     print(f"Монета: {symbol} цена: {cur_price}")

# #                     if signal and signal != symbol_item["first_signal"]:
# #                         print(f"Монета: {symbol} сигнал: {signal} цена: {cur_price}")
# #                         self.signals_data_list[i]['signal'] = signal                           
# #                     break
# #                 except Exception as ex:
# #                     print(ex)

# #         return not signal == 0    

# #     def symbol_item_creator(self, symbol, current_close, ema_cross):
# #         signal_data = {
# #             "symbol": symbol,
# #             "cur_price": current_close,
# #             "enter_1_pos_price": None,
# #             "enter_2_pos_price": None,
# #             "signal": ema_cross,
# #             "first_signal": ema_cross,
# #             "quantity_precision": None,
# #             "min_notional": None,
# #             "qty_1": 0,
# #             "qty_2": 0,
# #             "in_position_1": False,
# #             "in_position_2": False,
# #             "pos_averaging_true": False,
# #             "is_close_pos_humanly": False,
# #             "is_closed_1": False,
# #             "is_closed_2": False,
# #             "is_total_closing": False,
# #             "position_1_side": "LONG" if ema_cross == 1 else "SHORT",
# #             "position_2_side": "LONG" if ema_cross == -1 else "SHORT",            
# #             "sl_1_pos_rate": self.sl_1_pos_rate / 100,
# #             "tp_1_pos_rate": self.tp_1_pos_rate / 100,
# #             "sl_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[0].strip()),
# #             "tp_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[1].strip()),
# #             "current_step_counter": 0,
# #             "position_1_averaging_counter": 0,
# #         }
# #         self.signals_data_list.append(signal_data)

# #     async def process_kline_data(self, kline_data, recent_klines, symbol):
# #         open_time = kline_data['t']
# #         open_price = float(kline_data['o'])
# #         high_price = float(kline_data['h'])
# #         low_price = float(kline_data['l'])
# #         close_price = float(kline_data['c'])
# #         volume = float(kline_data['v'])

# #         recent_klines.append([open_time, open_price, high_price, low_price, close_price, volume])

# #         if len(recent_klines) > self.ema2_period:
# #             recent_klines.pop(0)

# #         if len(recent_klines) >= self.ema2_period:
# #             close_prices = np.array([kline[4] for kline in recent_klines])

# #             # Найти последнее пересечение EMA
# #             ema_cross = await self.find_last_ema_cross(close_prices)
# #             current_close = close_prices[-1]

# #             async with self.lock:
# #                 self.is_get_new_signal = self.symbol_data_reprocessing(symbol, ema_cross, current_close)

# #     async def process_historical_klines(self, recent_klines, symbol):
# #         if len(recent_klines) >= self.ema2_period:
# #             close_prices = np.array([kline[4] for kline in recent_klines])

# #             # Найти последнее пересечение EMA
# #             ema_cross = await self.find_last_ema_cross(close_prices)

# #             current_close = close_prices[-1]

# #             if symbol in ["NOTUSDT", "TRXUSDT"]:  # test
# #                 ema_cross == 1

# #             if ema_cross == 1:
# #                 print(f"Initial buy signal for {symbol} at price {current_close}")
# #             elif ema_cross == -1:
# #                 print(f"Initial sell signal for {symbol} at price {current_close}")

# #             if ema_cross:
# #                 self.symbol_item_creator(symbol, current_close, ema_cross)

# #     async def fetch_and_process_symbol(self, session, symbol, recent_klines_dict, trends_dict):
# #         recent_klines = await self.get_klines(session, symbol, self.interval, self.ema1_period + self.ema2_period)
# #         recent_klines_dict[symbol] = recent_klines.tolist()
# #         await self.process_historical_klines(recent_klines_dict[symbol], symbol)

# # class MAIN(WaitCandleLogic):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
# #         self.hadge_engin = self.log_exceptions_decorator(self.hadge_engin)
# #         self.main_engin = self.log_exceptions_decorator(self.main_engin)

# #     async def hedge_or_close_analizator(self, rules_analizes_func, is_hedging_possible):        
# #         is_any_close_pos = False
# #         is_any_hedging = False
# #         is_any_close_all_pos = False
# #         for i, symbol_item in enumerate(self.signals_data_list):
# #             rules_analizes_func_repl = rules_analizes_func(symbol_item)
# #             if rules_analizes_func_repl == "close_1_pos":
# #                 is_any_close_pos = self.signals_data_list[i]["is_closing_1_pos"] = True
# #             elif is_hedging_possible and rules_analizes_func_repl == "hedging":
# #                 is_any_hedging = self.signals_data_list[i]["is_hedging"] = True
# #             elif rules_analizes_func_repl == "close_both_pos":
# #                 is_any_close_all_pos = self.signals_data_list[i]["is_closing_1_pos"] = self.signals_data_list[i]["is_closing_2_pos"] = True

# #         is_first_init = False   

# #         if is_any_close_pos or is_any_hedging or is_any_close_all_pos:
# #             async with aiohttp.ClientSession() as session:                
# #                 if is_any_close_pos:
# #                     self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, 1, is_first_init)
# #                 elif is_any_hedging:
# #                     self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, 2, is_first_init)
# #                 elif is_any_close_all_pos:
# #                     self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, 1, is_first_init)
# #                     self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, 2, is_first_init)

# #     async def hadge_engin(self):
# #         if self.is_get_new_signal:
# #             self.is_get_new_signal = False
# #             is_hedging_possible = True
# #             await self.hedge_or_close_analizator(self.is_close_1_pos_by_signal_or_hedging, is_hedging_possible)
# #         is_hedging_possible = False
# #         if any((x.get("in_position_1") and not x.get("in_position_2")) for x in self.signals_data_list):
# #             await self.hedge_or_close_analizator(self.close_1_pos_by_price, is_hedging_possible)

# #         if any((x.get("in_position_1") and x.get("in_position_2")) for x in self.signals_data_list):
# #             await self.hedge_or_close_analizator(self.close_both_pos_condition, is_hedging_possible)

# #         if all((x.get("is_closed_1") and not x.get("in_position_2")) for x in self.signals_data_list):         
# #             return True
        
# #         return False
    
# #     async def main_engin(self):     
# #         wb_task_true = False
# #         wb_task = []
# #         wb_comleted_task = None
# #         self.handle_messagee("Устанавливаем режим хеджирования:")
# #         set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
# #         self.handle_messagee(str(set_hedge_mode_answ))

# #         while True:                 
# #             if self.next_trading_cycle: 
# #                 async with aiohttp.ClientSession() as session:
# #                     await asyncio.sleep(1)                     
# #                     await self.wait_for_candle_or_coins(session)                  
# #                     recent_klines_dict = {}  
# #                     print(self.candidate_symbols_list)               
# #                     tasks = [self.fetch_and_process_symbol(session, symbol, recent_klines_dict) for symbol in self.candidate_symbols_list]
# #                     await asyncio.gather(*tasks)        

# #                     if self.signals_data_list:
# #                         self.next_trading_cycle = False
# #                         wb_task_true = True
# #                         self.signals_data_list = self.signals_data_list[:self.diversification_number]                                       
# #                         [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.signals_data_list]
# #                         pos_number = 1
# #                         is_first_init = True       
# #                         self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, pos_number, is_first_init)
# #                         self.signals_data_list = [x for x in self.signals_data_list if x.get("in_position_1")]
# #                         print(self.signals_data_list)            
# #                     else:
# #                         continue

# #             if wb_task_true:
# #                 wb_task_true = False
# #                 symbols = [x.get("symbol") for x in self.signals_data_list]
# #                 if symbols:
# #                     wb_task = [self.connect_to_websocket(symbols, recent_klines_dict)]
# #                     wb_comleted_task = asyncio.gather(*wb_task)
# #                 else:
# #                     self.next_trading_cycle = True
# #                     continue
            
# #             # print("tik")
# #             await asyncio.sleep(1)   

# #             async with self.lock:                
# #                 self.next_trading_cycle = await self.hadge_engin()               

# #             if wb_comleted_task and wb_comleted_task.done():
# #                 self.next_trading_cycle = wb_comleted_task.result()
# #                 print("конец первой торговой итерации")

# # # Run the main function
# # if __name__ == "__main__":
# #     asyncio.run(MAIN().main_engin())

# # import aiohttp
# # import asyncio
# # # import time
# # from datetime import datetime as dttm
# # from ws_streams import WS_STREAMS
# # import os
# # import inspect
# # current_file = os.path.basename(__file__)

# # class TEMP(WS_STREAMS):
# #     def __init__(self):
# #         super().__init__()

# #     def get_lev_size_and_depo(self, pos_number):
# #         lev_size = self.lev_size_1 if pos_number == 1 else self.lev_size_2
# #         depo = self.depo_1 if pos_number == 1 else self.depo_2
# #         return lev_size, depo    

# #     async def trade_setup_template(self, session, lev_size):
# #         async def trade_setup_unit(session, symbol, lev_size):
# #             try:
# #                 self.handle_messagee(f'Устанавливаем тип маржи для {symbol}:')
# #                 set_margin_resp = await self.set_margin_type(session, symbol, self.margin_type)
# #                 self.handle_messagee(f"Монета {symbol}:     {str(set_margin_resp)}")
                
# #                 self.handle_messagee(f'Устанавливаем кредитное плечо для {symbol}:')
# #                 set_leverage_resp = await self.set_leverage(session, symbol, lev_size)
# #                 self.handle_messagee(str(set_leverage_resp))
                
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
# #         tasks1 = []
# #         tasks1 = [trade_setup_unit(session, symbol_item["symbol"], lev_size) for symbol_item in self.signals_data_list if symbol_item["signal_counter"] == 1]
# #         if tasks1:
# #             await asyncio.gather(*tasks1)

# #     async def is_closing_positions_template(self, session, pos_number):
# #         tasks2 = []
# #         exception_symbol_list = []
# #         is_closing_positions_symbol_list = []
# #         tasks2 = [self.is_closing_position_true(session, symbol_item["symbol"], symbol_item[f"position_{pos_number}_side"]) for symbol_item in self.signals_data_list if symbol_item["signal"]]
# #         if tasks2:
# #             is_closing_positions_symbol_list = await asyncio.gather(*tasks2)
# #             for symbol_item in self.signals_data_list:
# #                 for is_closed, symb in is_closing_positions_symbol_list:
# #                     if symbol_item["symbol"] == symb:
# #                         if self.is_try_to_close(symbol_item) and is_closed:
# #                             exception_symbol_list.append(symb)
# #                             break
# #                         elif not self.is_try_to_close(symbol_item) and not is_closed:
# #                             exception_symbol_list.append(symb)
# #                             break
# #         return exception_symbol_list

# #     def is_try_to_close(self, symbol_item):
# #         if symbol_item["signal_counter"] == 1:
# #             return False
# #         return symbol_item.get("is_closing_1_pos") or  symbol_item.get("is_closing_2_pos")

# #     def get_side(self, symbol_item, pos_number):
# #         side = None
# #         if symbol_item.get("signal", None):
# #             position_side = symbol_item.get(f"position_{pos_number}_side")
# #             if self.is_try_to_close():
# #                 if position_side == "LONG":
# #                     side = "SELL" 
# #                 else:
# #                     side = "BUY"
# #             else:
# #                 if position_side == "LONG":
# #                     side = "BUY"
# #                 else:
# #                     side = "SELL"
# #         return side
    
# #     def orders_logger_hundler(self, order_answer): 
# #         if order_answer is not None:
# #             specific_key_list = ["orderId", "symbol", "positionSide", "side", "executedQty", "avgPrice"]
# #             order_answer_str = ""
# #             try:
# #                 now_time = dttm.now(self.local_tz)
# #                 order_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
# #                 for k, v in order_answer.items():
# #                     if k in specific_key_list:
# #                         order_answer_str += f"{k}: {v}\n"
# #                 order_answer_str = 'Время создания ордера:' + ' ' + order_time + '\n' + order_answer_str 
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                
# #             status = order_answer.get('status')
        
# #             if status in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
# #                 self.handle_messagee(order_answer_str)         
# #                 return True

# #         error_message = f"При попытке создания ордера возникла ошибка. Текст ответа:\n {order_answer}"
# #         self.handle_messagee(error_message)
                       
# #         return False
    
# #     async def make_orders_template(self, session, pos_number, exception_list, depo):
# #         tasks3 = []
# #         for i, symbol_item in enumerate(self.signals_data_list):
# #             if symbol_item.get("signal"):
# #                 self.signals_data_list[i]["quantity_precision"], _, self.signals_data_list[i]["min_notional"] = self.get_precisions(symbol_item.get("symbol"), self.exchange_data)
# #                 self.signals_data_list[i]["qty"] = self.usdt_to_qnt_converter(depo, symbol_item.get("cur_price"), self.signals_data_list[i]["quantity_precision"], self.signals_data_list[i]["min_notional"])

# #         task3 = [self.make_order(session, symbol_item["symbol"], symbol_item[f"qty_{pos_number}"], self.get_side(symbol_item, pos_number), 'MARKET', symbol_item.get(f"position_{pos_number}_side")) for symbol_item in self.signals_data_list if symbol_item["symbol"] not in exception_list]
# #         if task3:
# #             return await asyncio.gather(*tasks3)
# #         return []
    
# #     # ////////////////////////////////////////        
# #     async def make_orders_total_template(self, session, pos_number):
# #         exception_list = []
# #         try:                        
# #             lev_size, depo = self.get_lev_size_and_depo(pos_number)
# #             await self.trade_setup_template(session, lev_size)
# #             exception_list = await self.is_closing_positions_template(session, pos_number)
# #             print(f"exception_list: {exception_list}")
# #             make_order_results = await self.make_orders_template(session, pos_number, exception_list, depo)
# #             if make_order_results:
# #                 self.process_order_results(make_order_results, pos_number)
# #         except Exception as ex:
# #             self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
# #     # ////////////////////////////////////////  
    
# #     def process_order_results(self, make_order_results, pos_number):
# #         for item_res in make_order_results:
# #             if item_res:
# #                 order_logger_resp = self.orders_logger_hundler(item_res)
# #                 if order_logger_resp:
# #                     self.update_position_status(item_res, pos_number)

# #     def update_position_status(self, item_res, pos_number):
# #         for i, symbol_item in enumerate(self.signals_data_list):
# #             if symbol_item["symbol"] == item_res["symbol"]:
# #                 self.signals_data_list[i][f"in_position_{pos_number}"] = not symbol_item.get(f"is_closing_{pos_number}_pos")
# #                 self.signals_data_list[i][f"is_closed_{pos_number}"] = symbol_item.get(f"is_closing_{pos_number}_pos")               
# #                 self.signals_data_list[i][f"enter_{pos_number}_pos_price"] = item_res.get("avgPrice", None)
# #                 self.signals_data_list[i]["qty"] = item_res.get("executedQty", None)
# #                 self.signals_data_list[i]["signal"] = None      
# #                 break


    
#     # def close_both_pos_condition(self, symbol_item):
#     #     if symbol_item["in_position_1"] and symbol_item["in_position_2"]:
#     #         total_tp_rate = self.comulative_tp_rate/ 100
#     #         total_sl_rate = self.comulative_sl_rate/ 100
#     #         cur_price = float(symbol_item["cur_price"])
#     #         enter_1_pos_price = float(symbol_item["enter_1_pos_price"])
#     #         enter_2_pos_price = float(symbol_item["enter_2_pos_price"])
#     #         pos_1_profit_rate = abs(cur_price - enter_1_pos_price)/ enter_1_pos_price
#     #         pos_2_profit_rate = abs(cur_price - enter_2_pos_price)/ enter_2_pos_price
#     #         position_1_side = symbol_item["position_1_side"]
#     #         position_2_side = symbol_item["position_2_side"]

#     #         if position_1_side == "LONG":                    
#     #             if cur_price < enter_1_pos_price:
#     #                 pos_1_profit_rate = - pos_1_profit_rate
#     #         if position_1_side == "SHORT":                    
#     #             if cur_price > enter_1_pos_price:
#     #                 pos_1_profit_rate = - pos_1_profit_rate
#     #         if position_2_side == "LONG":                    
#     #             if cur_price < enter_2_pos_price:
#     #                 pos_2_profit_rate = - pos_2_profit_rate
#     #         if position_2_side == "SHORT":                    
#     #             if cur_price > enter_2_pos_price:
#     #                 pos_2_profit_rate = - pos_2_profit_rate
#     #         if pos_1_profit_rate < 0 and pos_2_profit_rate < 0:
#     #             # print("На текущий момент две позиции в минусе...")
#     #             if abs(pos_1_profit_rate + pos_2_profit_rate) >= total_sl_rate:
#     #                 print("Закрываем обе позиции. Фиксируем общий минус")
#     #                 return "close_both_pos"          
#     #         elif pos_1_profit_rate + pos_2_profit_rate >= total_tp_rate:  
#     #             print("Закрываем обе позиции. Фиксируем общий плюс")              
#     #             return "close_both_pos"     
            
#     #     return
    
#     # def position_1_averaging_conditions(self, symbol_item):
#     #     is_averaging_flag = False
#     #     try:
#     #         if symbol_item["in_position_1"]:
#     #             cur_price = symbol_item["cur_price"]
#     #             position_1_side = symbol_item["position_1_side"]
#     #             enter_1_pos_price = symbol_item["enter_1_pos_price"]
#     #             averaging_step_rate = self.averaging_step_rate/ 100
#     #             pos_1_profit_rate = abs(cur_price - enter_1_pos_price)/ enter_1_pos_price
#     #             current_step_counter = int(abs(pos_1_profit_rate)/ averaging_step_rate)
#     #             if position_1_side == "LONG":                    
#     #                 if cur_price < enter_1_pos_price:
#     #                     pos_1_profit_rate = - pos_1_profit_rate
#     #             if position_1_side == "SHORT":                    
#     #                 if cur_price > enter_1_pos_price:
#     #                     pos_1_profit_rate = - pos_1_profit_rate
#     #             if pos_1_profit_rate < 0:
#     #                 if (current_step_counter > position_1_side["position_1_averaging_counter"]):
#     #                     position_1_side["position_1_averaging_counter"] += 1
#     #                     is_averaging_flag = True
#     #     except Exception as ex:
#     #         print(ex)
                    
#     #     return symbol_item, is_averaging_flag

    
# # if (current_step_counter >= self.position_1_averaging_counter_limit) and (pos_2_profit_rate > 0):
# #     return None, (self.posicion_2_side, "Sell", 2)


# # class BINANCE_API(Total_Logger):
# #     def __init__(self):
# #         super().__init__()
# #         self.market_place = 'binance'
# #         self.market_type = 'futures'
        
# #         # URLs for Binance API
# #         self.create_order_url = self.cancel_order_url = 'https://fapi.binance.com/fapi/v1/order'
# #         self.change_trade_mode = 'https://fapi.binance.com/fapi/v1/positionSide/dual'
# #         self.exchangeInfo_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
# #         self.klines_url = 'https://fapi.binance.com/fapi/v1/klines'
# #         self.set_margin_type_url = 'https://fapi.binance.com/fapi/v1/marginType'
# #         self.set_leverage_url = 'https://fapi.binance.com/fapi/v1/leverage'
# #         self.positions_url = 'https://fapi.binance.com/fapi/v2/positionRisk'
# #         self.all_tikers_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
# #         self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOrders'
# #         self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
# #         self.balance_url = 'https://fapi.binance.com/fapi/v2/balance'

# #         self.session = None
        
# #         self.headers = {
# #             'X-MBX-APIKEY': self.api_key
# #         }
        
# #         if self.is_proxies_true:
# #             self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
# #             self.proxies = {
# #                 'http': self.proxy_url,
# #                 'https': self.proxy_url
# #             }
# #         else:
# #             self.proxies = None

# #     def get_signature(self, params):
# #         params['timestamp'] = int(time.time() * 1000)
# #         params_str = '&'.join([f'{k}={v}' for k, v in params.items()])
# #         signature = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256).hexdigest()
# #         params['signature'] = signature
# #         return params

# #     async def http_request(self, url, method='GET', params=None, data=None):
# #         async with aiohttp.ClientSession(headers=self.headers) as session:
# #             async with session.request(method=method, url=url, params=params, json=data, proxy=self.proxy_url if self.proxies else None) as response:
# #                 return await response.json()

# #     async def get_exchange_info(self):
# #         params = {'recvWindow': 20000}
# #         return await self.http_request(self.exchangeInfo_url, method='GET', params=params)

# #     async def get_all_tickers(self):
# #         params = {'recvWindow': 20000}
# #         return await self.http_request(self.all_tikers_url, method='GET', params=params)

# #     async def get_total_balance(self, ticker):
# #         params = {'recvWindow': 20000}
# #         params = self.get_signature(params)
# #         current_balance = await self.http_request(self.balance_url, method='GET', params=params)
# #         return float([x['balance'] for x in current_balance if x['asset'] == ticker][0])

# #     async def get_all_orders(self, symbol):
# #         params = {'symbol': symbol, 'recvWindow': 20000}
# #         params = self.get_signature(params)
# #         return await self.http_request(self.get_all_orders_url, method='GET', params=params)

# #     async def get_klines(self, symbol, interval, limit):
# #         params = {'symbol': symbol, 'interval': interval, 'limit': limit}
# #         data = await self.http_request(self.klines_url, method='GET', params=params)
# #         klines = [
# #             [float(entry[0]), float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4]), float(entry[5])]
# #             for entry in data
# #         ]
# #         return (symbol, np.array(klines))

# #     async def fetch_all_klines(self, symbols, interval, limit):
# #         tasks = [self.get_klines(symbol, interval, limit) for symbol in symbols]
# #         results = await asyncio.gather(*tasks)
# #         return results

# #     async def is_closing_position_true(self, symbol, position_side):
# #         params = {
# #             "symbol": symbol,
# #             "positionSide": position_side,
# #             'recvWindow': 20000,            
# #         }
# #         params = self.get_signature(params)
# #         positions = await self.http_request(self.positions_url, method='GET', params=params)
# #         for position in positions:
# #             if position['symbol'] == symbol and position['positionSide'] == position_side and float(position['positionAmt']) != 0:
# #                 return None
# #         return True
    
# #     # ///////////////////// post api:
# #     async def set_hedge_mode(self, true_hedg):
# #         params = {
# #             'dualSidePosition': 'true' if true_hedg else 'false',            
# #         }
# #         params = self.get_signature(params)
# #         return await self.http_request(self.change_trade_mode, method='POST', params=params)
    
# #     async def set_margin_type(self, symbol, margin_type):
# #         params = {
# #             'symbol': symbol,
# #             'margintype': margin_type,
# #             'recvWindow': 20000,
# #             'newClientOrderId': 'CHANGE_MARGIN_TYPE'
# #         }
# #         params = self.get_signature(params)
# #         return await self.http_request(self.set_margin_type_url, method='POST', params=params)

# #     async def set_leverage(self, symbol, lev_size):
# #         params = {
# #             'symbol': symbol,
# #             'recvWindow': 20000,
# #             'leverage': lev_size
# #         }
# #         params = self.get_signature(params)
# #         return await self.http_request(self.set_leverage_url, method='POST', params=params)

# #     async def make_order(self, symbol, qty, side, market_type, position_side, pos_averaging_true, target_price=None):
  
# #         params = {
# #             "symbol": symbol,
# #             "side": side,
# #             "type": market_type,
# #             "quantity": qty,
# #             "positionSide": position_side,
# #             "recvWindow": 20000,
# #             "newOrderRespType": 'RESULT'
# #         }
# #         if pos_averaging_true:
# #             params['reduceOnly'] = 'true'
        
# #         if market_type in ['STOP_MARKET', 'TAKE_PROFIT_MARKET']:
# #             params['stopPrice'] = target_price
# #             params['closePosition'] = True
# #         elif market_type == 'LIMIT':
# #             params["price"] = target_price
# #             params["timeInForce"] = 'GTC'

# #         params = self.get_signature(params)
# #         return await self.http_request(self.create_order_url, method='POST', params=params)


#     # def close_both_pos_condition(self, symbol_item):
#     #     if symbol_item["in_position_1"] and symbol_item["in_position_2"]:
#     #         total_tp_rate = self.comulative_tp_rate/ 100
#     #         cur_price = float(symbol_item["cur_price"])
#     #         enter_1_pos_price = float(symbol_item["enter_1_pos_price"])
#     #         enter_2_pos_price = float(symbol_item["enter_2_pos_price"])
#     #         pos_1_profit_rate = abs(cur_price - enter_1_pos_price)/ enter_1_pos_price
#     #         pos_2_profit_rate = abs(cur_price - enter_2_pos_price)/ enter_2_pos_price
#     #         position_1_side = symbol_item["position_1_side"]
#     #         position_2_side = symbol_item["position_2_side"]

#     #         if position_1_side == "LONG":                    
#     #             if cur_price < enter_1_pos_price:
#     #                 pos_1_profit_rate = - pos_1_profit_rate
#     #         if position_1_side == "SHORT":                    
#     #             if cur_price > enter_1_pos_price:
#     #                 pos_1_profit_rate = - pos_1_profit_rate
#     #         if position_2_side == "LONG":                    
#     #             if cur_price < enter_2_pos_price:
#     #                 pos_2_profit_rate = - pos_2_profit_rate
#     #         if position_2_side == "SHORT":                    
#     #             if cur_price > enter_2_pos_price:
#     #                 pos_2_profit_rate = - pos_2_profit_rate         
#     #         if pos_1_profit_rate + pos_2_profit_rate >= total_tp_rate:  
#     #             print("Закрываем обе позиции по процентному изменению цены. Фиксируем общий плюс")              
#     #             return "close_both_pos"     
            
#     #     return


#     # async def is_closing_positions_template(self, session, pos_num):
#     #     tasks = []
#     #     exception_symbol_list = []
#     #     tasks = [self.is_closing_position_true(session, symbol_item["symbol"], symbol_item[f"position_{pos_num}_side"]) for symbol_item in self.trading_data_list]           

#     #     if tasks:
#     #         is_closing_positions_symbol_list = await asyncio.gather(*tasks)
#     #         print(is_closing_positions_symbol_list)
#     #         for symbol_item in self.trading_data_list:
#     #             for is_closed, symb in is_closing_positions_symbol_list:
#     #                 if symbol_item["symbol"] == symb:
#     #                     if self.should_close_position(symbol_item) and is_closed:
#     #                         exception_symbol_list.append(symb)
#     #                         break
#     #                     elif self.should_open_position(symbol_item) and not is_closed:
#     #                         exception_symbol_list.append(symb)
#     #                         break
#     #     return exception_symbol_list


#     # async def is_finish_trade_cycle_true(self, session):
#     #     print("is_finish_trade_cycle_true")
#     #     if all((not x.get("in_position_1") and not x.get("in_position_2")) for x in self.trading_data_list):
#     #         print("Все позиции 1 и 2 закрыты")
#     #         return True
        
#     #     not_active_symbol_list = []
#     #     for pos_num in [1,2]:
#     #         not_active_symbol_list += await self.is_closing_positions_template(session, pos_num)
#     #         print(f"not_active_symbol_list: {not_active_symbol_list}")
#     #     if len(not_active_symbol_list) == len(self.trading_data_list):
#     #         print("len(not_active_symbol_list) == len(self.trading_data_list)")
#     #         return True
        
#     #     return False

# # import asyncio
# # from datetime import datetime as dttm
# # from ws_streams import WS_STREAMS
# # from api_binance import aiohttp_connector
# # import os
# # import inspect

# # current_file = os.path.basename(__file__)

# # class TEMP(WS_STREAMS):
# #     def __init__(self):
# #         super().__init__()

# #     async def trade_setup_template(self, session, lev_size):
# #         async def trade_setup_unit(session, symbol, lev_size):
# #             try:
# #                 self.handle_messagee(f'Устанавливаем тип маржи для {symbol}:')
# #                 set_margin_resp = await self.set_margin_type(session, symbol, self.margin_type)
# #                 self.handle_messagee(f"Монета {symbol}:     {str(set_margin_resp)}")
                
# #                 self.handle_messagee(f'Устанавливаем кредитное плечо для {symbol}:')
# #                 set_leverage_resp = await self.set_leverage(session, symbol, lev_size)
# #                 self.handle_messagee(str(set_leverage_resp))
                
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

# #         tasks = [trade_setup_unit(session, symbol_item["symbol"], lev_size) for symbol_item in self.trading_data_list if symbol_item["first_trade"]]
# #         if tasks:
# #             await asyncio.gather(*tasks)

# #     async def is_closing_positions_template(self, session, pos_num, is_finish_flag=False):
# #         tasks = []
# #         exception_symbol_list = []
# #         tasks = [self.is_closing_position_true(session, symbol_item["symbol"], symbol_item[f"position_{pos_num}_side"]) for symbol_item in self.trading_data_list]

# #         if tasks:
# #             is_closing_positions_symbol_list = await asyncio.gather(*tasks)
# #             # print(is_closing_positions_symbol_list)
# #             for symbol_item in self.trading_data_list:
# #                 for is_closed, symb in is_closing_positions_symbol_list:
# #                     if symbol_item["symbol"] == symb:
# #                         if self.should_close_position(symbol_item) and is_closed:
# #                             exception_symbol_list.append(symb)
# #                             break
# #                         elif self.should_open_position(symbol_item) and not is_closed:
# #                             exception_symbol_list.append(symb)
# #                             break
# #                         elif is_finish_flag and is_closed:
# #                             exception_symbol_list.append(symb)
# #         return exception_symbol_list
    
# #     def should_open_position(self, symbol_item):
# #         return symbol_item.get("is_opening_1_pos") or symbol_item.get("is_opening_2_pos")

# #     def should_close_position(self, symbol_item):
# #         return symbol_item.get("is_closing_1_pos") or symbol_item.get("is_closing_2_pos")
       
# #     def get_side(self, symbol_item, pos_number):
# #         side = None
# #         if self.should_close_position(symbol_item) or self.should_open_position(symbol_item):
# #             position_side = symbol_item.get(f"position_{pos_number}_side")
# #             if self.should_close_position(symbol_item):
# #                 side = "SELL" if position_side == "LONG" else "BUY"
# #             else:
# #                 side = "BUY" if position_side == "LONG" else "SELL"
# #         return side

# #     def orders_logger_hundler(self, order_answer): 
# #         if order_answer is not None:
# #             specific_key_list = ["orderId", "symbol", "positionSide", "side", "executedQty", "avgPrice"]
# #             order_answer_str = ""
# #             try:
# #                 now_time = dttm.now(self.local_tz)
# #                 order_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
# #                 for k, v in order_answer.items():
# #                     if k in specific_key_list:
# #                         order_answer_str += f"{k}: {v}\n"
# #                 order_answer_str = 'Время создания ордера:' + ' ' + order_time + '\n' + order_answer_str 
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                
# #             status = order_answer.get('status')
        
# #             if status in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
# #                 self.handle_messagee(order_answer_str)         
# #                 return True

# #         error_message = f"При попытке создания ордера возникла ошибка. Текст ответа:\n {order_answer}"
# #         self.handle_messagee(error_message)
                       
# #         return False

# #     async def make_orders_template(self, session, pos_number, exception_list):
# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             if symbol_item.get("first_trade"):
# #                 self.trading_data_list[i]["first_trade"] = False
# #                 self.trading_data_list[i]["quantity_precision"], _, self.trading_data_list[i]["min_notional"] = self.get_precisions(symbol_item.get("symbol"), self.exchange_data)
# #                 self.trading_data_list[i]["qty"] = self.usdt_to_qnt_converter(symbol_item.get("cur_price"), self.trading_data_list[i]["quantity_precision"], self.trading_data_list[i]["min_notional"])

# #         tasks = [self.make_order(session, symbol_item["symbol"], symbol_item["qty"], self.get_side(symbol_item, pos_number), 'MARKET', symbol_item.get(f"position_{pos_number}_side")) for symbol_item in self.trading_data_list if symbol_item["symbol"] not in exception_list]    
# #         if tasks:
# #             return await asyncio.gather(*tasks)
# #         return []
    
# #     @aiohttp_connector
# #     async def make_orders_total_template(self, session):
# #         exception_list = []
# #         for pos_number in [1,2]:
# #             if any(symbol_item.get(f"is_opening_{pos_number}_pos") or symbol_item.get(f"is_closing_{pos_number}_pos") for symbol_item in self.trading_data_list):
# #                 try:        
# #                     await self.trade_setup_template(session, self.lev_size)
# #                     exception_list = await self.is_closing_positions_template(session, pos_number)
# #                     print(f"exception_list: {exception_list}")
# #                     make_order_results = await self.make_orders_template(session, pos_number, exception_list)
# #                     if make_order_results:
# #                         self.process_order_results(make_order_results, pos_number)
# #                 except Exception as ex:
# #                     self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

# #     def process_order_results(self, make_order_results, pos_number):
# #         for item_res in make_order_results:
# #             if item_res:
# #                 order_logger_resp = self.orders_logger_hundler(item_res)
# #                 if order_logger_resp:
# #                     self.update_position_status(item_res, pos_number)

# #     def update_position_status(self, item_res, pos_number):
# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             if symbol_item["symbol"] == item_res["symbol"]:
# #                 self.trading_data_list[i][f"in_position_{pos_number}"] = not symbol_item.get(f"is_closing_{pos_number}_pos") 
# #                 self.trading_data_list[i][f"is_opening_{pos_number}_pos"] = False
# #                 self.trading_data_list[i][f"is_closing_{pos_number}_pos"] = False                      
# #                 self.trading_data_list[i][f"enter_{pos_number}_pos_price"] = item_res.get("avgPrice", None)
# #                 self.trading_data_list[i]["qty"] = item_res.get("executedQty", None)
# #                 self.trading_data_list[i]["signal"] = None      
# #                 break

# #     @aiohttp_connector
# #     async def is_finish_trade_cycle_true(self, session):
# #         print("Проверка завершения торгового цикла")

# #         # Проверка на закрытие всех позиций
# #         if all((not x.get("in_position_1") and not x.get("in_position_2")) for x in self.trading_data_list):
# #             print('Все позиции закрыты')
# #             return True

# #         not_active_symbol_list = []

# #         # Проверка позиций для каждого номера
# #         for pos_num in [1, 2]:
# #             temperary_not_active_symbol_list = await self.is_closing_positions_template(session, pos_num, True)
# #             if temperary_not_active_symbol_list:      
# #                 not_active_symbol_list += [(x, pos_num) for x in temperary_not_active_symbol_list]

# #         # Проверка длины списка неактивных символов
# #         if len(not_active_symbol_list) == len(self.trading_data_list) * 2:
# #             print("Все позиции для всех символов закрыты")
# #             return True

# #         # Обновление списка торговых данных
# #         for symb, pos_n in not_active_symbol_list:
# #             for i, item_list in enumerate(self.trading_data_list):
# #                 if item_list.get("symbol") == symb:
# #                     self.trading_data_list[i][f"in_position_{pos_n}"] = False
# #                     break

# #         return False

# # WEBSOCKET_URL = "wss://fstream.binance.com/"

# # class WS_STREAMS(SORT_DATA):
# #     def __init__(self) -> None:
# #         super().__init__()

# #     async def handle_message(self, message, recent_klines_dict):
# #         # await asyncio.sleep(0.01)
# #         message = json.loads(message)['data']
# #         if message['e'] == 'kline':  # Check if the kline is closed
# #             symbol = message['s']
# #             if symbol not in recent_klines_dict:
# #                 recent_klines_dict[symbol] = []
# #             await self.process_prices_data(message['k'], symbol)
# #             if message['k']['x']:
# #                 await self.process_kline_data(message['k'], recent_klines_dict[symbol], symbol)

# #     async def connect_to_websocket(self, symbols, recent_klines_dict):
# #         print("connect_to_websocket")
# #         stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]  # Dividing symbols into chunks
# #         is_wb_finish = False
# #         for chunk in stream_chunks:
# #             streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]  # Example using 1-minute interval
# #             url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
# #             async with websockets.connect(url) as websocket:
# #                 async for message in websocket:
# #                     await self.handle_message(message, recent_klines_dict)                    
# #                     if self.next_trading_cycle_event.is_set():                            
# #                         is_wb_finish = True 
# #                         break
# #             if is_wb_finish:
# #                 # print(f"is_wb_finish: {is_wb_finish}")
# #                 break
# #         self.next_trading_cycle_event.clear()
# #         return is_wb_finish


# # import numpy as np
# # from utils import UTILS

# # class SORT_DATA(UTILS):
# #     def __init__(self) -> None:
# #         super().__init__()

# #     def symbol_item_creator(self, symbol, current_close, ema_cross):
# #         signal_data = {
# #             "symbol": symbol,
# #             "cur_price": current_close,
# #             "enter_1_pos_price": None,
# #             "enter_2_pos_price": None,
# #             "signal": ema_cross,
# #             "first_trade": True,
# #             "quantity_precision": None,
# #             "min_notional": None,
# #             "qty": 0,      
# #             "in_position_1": False,
# #             "in_position_2": False,
# #             "is_opening_1_pos": True,
# #             "is_opening_2_pos": False,
# #             "is_closing_1_pos": False,
# #             "is_closing_2_pos": False,
# #             "position_1_side": "LONG" if ema_cross == 1 else "SHORT",
# #             "position_2_side": "LONG" if ema_cross == -1 else "SHORT",            
# #             "sl_pos_rate": (self.sl_1_pos_rate / 100)* float(self.risk_reward_ratio.split(':')[0].strip()),
# #             "tp_pos_rate": (self.tp_1_pos_rate / 100)* float(self.risk_reward_ratio.split(':')[1].strip()),
# #             "min_deviation_rate": self.min_deviation_rate/ 100,
# #         }
# #         self.trading_data_list.append(signal_data)

# #     def symbol_data_reprocessing(self, symbol, signal, cur_price):  
# #         for i, symbol_item in enumerate(self.trading_data_list):            
# #             if symbol_item["symbol"] == symbol:
# #                 try:
# #                     self.trading_data_list[i]['cur_price'] = cur_price                    
# #                     if signal:
# #                         print(f"Монета: {symbol} сигнал: {signal} цена: {cur_price}")                        
# #                         self.trading_data_list[i]['signal'] = signal
# #                         self.is_get_new_signal = True                      
# #                     break
# #                 except Exception as ex:
# #                     print(ex)

# #     async def process_prices_data(self, kline_data, symbol):
# #         close_price = float(kline_data['c'])
# #         for i, symbol_item in enumerate(self.trading_data_list):            
# #             if symbol_item.get("symbol") == symbol:
# #                 try:
# #                     self.trading_data_list[i]['cur_price'] = close_price
# #                     # print(f"Монета: {symbol} цена: {close_price}")                    
# #                     break
# #                 except Exception as ex:
# #                     print(ex)

# #     async def process_kline_data(self, kline_data, recent_klines, symbol):
# #         open_time = kline_data['t']
# #         open_price = float(kline_data['o'])
# #         high_price = float(kline_data['h'])
# #         low_price = float(kline_data['l'])
# #         close_price = float(kline_data['c'])
# #         volume = float(kline_data['v'])
# #         recent_klines.append([open_time, open_price, high_price, low_price, close_price, volume])

# #         if len(recent_klines) > self.ema2_period:
# #             recent_klines.pop(0)
# #         if len(recent_klines) >= self.ema2_period:
# #             close_prices = np.array([float(kline[4]) for kline in recent_klines], dtype=np.float64)
# #             ema_cross = await self.find_last_ema_cross(close_prices)
# #             current_close = close_prices[-1]

# #             async with self.lock:
# #                 self.symbol_data_reprocessing(symbol, ema_cross, current_close)

# #     async def process_historical_klines(self, recent_klines, symbol):
# #         if len(recent_klines) >= self.ema2_period:
# #             close_prices = np.array([float(kline[4]) for kline in recent_klines], dtype=np.float64)
# #             ema_cross = await self.find_last_ema_cross(close_prices)
# #             current_close = close_prices[-1]
# #             # if symbol in ["NOTUSDT", "TRXUSDT"]:  # test
# #             #     ema_cross = 1
# #             if ema_cross == 1:
# #                 print(f"Initial buy signal for {symbol} at price {current_close}")
# #             elif ema_cross == -1:
# #                 print(f"Initial sell signal for {symbol} at price {current_close}")
# #             if ema_cross:
# #                 self.symbol_item_creator(symbol, current_close, ema_cross* self.is_reverse_signal)

# #     async def fetch_and_process_symbol(self, session, symbol, recent_klines_dict):
# #         recent_klines = await self.get_klines(session, symbol, self.interval, self.ema1_period + self.ema2_period)
# #         recent_klines_dict[symbol] = recent_klines.tolist()
# #         await self.process_historical_klines(recent_klines_dict[symbol], symbol)


# # class RULESS(VARIABLES):
# #     def __init__(self):
# #         super().__init__()

# #     def is_close_some_pos_by_signal_or_hedging(self, symbol_item):
# #         try:
# #             if (symbol_item.get("in_position_1") and not symbol_item.get("in_position_2")) or (symbol_item.get("in_position_2") and not symbol_item.get("in_position_1")):
# #                 pos_num = 1 if symbol_item.get("in_position_1") else 2
# #                 hedg_num = 2 if symbol_item.get("in_position_1") else 1                
# #                 enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #                 if not isinstance(enter_pos_price, float):
# #                     return None
# #                 signal = symbol_item.get("signal")
# #                 cur_price = float(symbol_item.get("cur_price"))
# #                 position_side = symbol_item.get(f"position_{pos_num}_side")                           
# #                 change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #                 if position_side == "LONG":
# #                     if signal == 1:
# #                         return None
# #                     if cur_price < enter_pos_price:
# #                         change_price_ratio = -change_price_ratio
# #                 elif position_side == "SHORT":
# #                     if signal == -1:
# #                         return None
# #                     if cur_price > enter_pos_price:
# #                         change_price_ratio = -change_price_ratio
                
# #                 if change_price_ratio >= symbol_item.get("min_deviation_rate"):
# #                     print(f"Сработал тригер на продажу первой позиции по СИГНАЛУ. Монета {symbol_item.get('symbol')}. позиция {pos_num}")
# #                     return "closing", pos_num
# #                 print(f"Хеджируем позицию {hedg_num} по монете {symbol_item.get('symbol')}")
# #                 return "opening", hedg_num

# #         except Exception as ex:
# #             print(ex)
            
# #         return None
    
# #     def close_any_pos_by_signal(self, symbol_item):
# #         try:
# #             if symbol_item.get("in_position_1") and symbol_item.get("in_position_2"):
# #                 for pos_num in [1,2]:
# #                     enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #                     if not isinstance(enter_pos_price, float):
# #                         continue
# #                     signal = symbol_item.get("signal")
# #                     cur_price = float(symbol_item.get("cur_price"))
# #                     position_side = symbol_item.get(f"position_{pos_num}_side")                    
# #                     change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price
                    
# #                     if position_side == "LONG":
# #                         if signal == 1:
# #                             continue
# #                         if cur_price < enter_pos_price:
# #                             change_price_ratio = -change_price_ratio
# #                     elif position_side == "SHORT":
# #                         if signal == -1:
# #                             continue
# #                         if cur_price > enter_pos_price:
# #                             change_price_ratio = -change_price_ratio
                    
# #                     if change_price_ratio >= symbol_item.get("min_deviation_rate"):
# #                         print(f"Сработал тригер на продажу {pos_num} позиции по СИГНАЛУ. Монета {symbol_item.get('symbol')}")
# #                         return "closing", pos_num

# #         except Exception as ex:
# #             print(ex)

# #         return None
        
# #     def close_any_pos_by_price(self, symbol_item):
# #         try:
# #             if any([not self.only_take_profit_flag, not self.only_stop_loss_flag]):
# #                 if (symbol_item.get("in_position_1") and not symbol_item.get("in_position_2")) or (symbol_item.get("in_position_2") and not symbol_item.get("in_position_1")):
# #                     sl_condition = False
# #                     tp_condition = False
# #                     pos_num = 1 if symbol_item.get("in_position_1") else 2
# #                     enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #                     if not isinstance(enter_pos_price, float):
# #                         print("not isinstance(enter_pos_price, float)")
# #                         return None
# #                     cur_price = float(symbol_item.get("cur_price"))
# #                     position_side = symbol_item.get(f"position_{pos_num}_side")
# #                     change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #                     if position_side == "LONG":
# #                         if cur_price < enter_pos_price:
# #                             change_price_ratio = -change_price_ratio
# #                     elif position_side == "SHORT":
# #                         if cur_price > enter_pos_price:
# #                             change_price_ratio = -change_price_ratio

# #                     if not self.only_take_profit_flag:
# #                         if change_price_ratio < 0:
# #                             # print(change_price_ratio, symbol_item.get("tp_pos_rate"))                       
# #                             sl_condition = abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
# #                     if not self.only_stop_loss_flag:
# #                         if change_price_ratio > 0:   
# #                             # print(change_price_ratio, symbol_item.get("tp_pos_rate"))                         
# #                             tp_condition = change_price_ratio >= symbol_item.get("tp_pos_rate")

# #                     if tp_condition or sl_condition:
# #                         print(f"Сработал тригер на продажу {pos_num} позиции. Монета {symbol_item.get('symbol')}")
# #                         return "closing", pos_num

# #         except Exception as ex:
# #             print(ex)

# #         return  None

# # class RULESS(VARIABLES):
# #     def __init__(self):
# #         super().__init__()

# #     def analyze_and_handle_positions(self, symbol_item):
# #         try:
# #             pos_num, hedg_num = (1, 2) if symbol_item.get("in_position_1") else (2, 1)
# #             enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #             if not isinstance(enter_pos_price, float):
# #                 return None

# #             signal = symbol_item.get("signal")
# #             cur_price = float(symbol_item.get("cur_price"))
# #             position_side = symbol_item.get(f"position_{pos_num}_side")
# #             change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #             if position_side == "LONG":
# #                 if signal == 1:
# #                     return None
# #                 if cur_price < enter_pos_price:
# #                     change_price_ratio = -change_price_ratio
# #             elif position_side == "SHORT":
# #                 if signal == -1:
# #                     return None
# #                 if cur_price > enter_pos_price:
# #                     change_price_ratio = -change_price_ratio

# #             if change_price_ratio >= symbol_item.get("min_deviation_rate"):
# #                 print(f"Triggered closing position {pos_num} due to signal for {symbol_item.get('symbol')}.")
# #                 return "closing", pos_num
# #             print(f"Hedging position {hedg_num} for {symbol_item.get('symbol')}")
# #             return "opening", hedg_num

# #         except Exception as ex:
# #             print(ex)
# #             return None

# #     def close_position_by_price(self, symbol_item):
# #         try:
# #             pos_num = 1 if symbol_item.get("in_position_1") else 2
# #             enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #             if not isinstance(enter_pos_price, float):
# #                 return None

# #             cur_price = float(symbol_item.get("cur_price"))
# #             position_side = symbol_item.get(f"position_{pos_num}_side")
# #             change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #             if position_side == "LONG":
# #                 if cur_price < enter_pos_price:
# #                     change_price_ratio = -change_price_ratio
# #             elif position_side == "SHORT":
# #                 if cur_price > enter_pos_price:
# #                     change_price_ratio = -change_price_ratio

# #             sl_condition = not self.only_take_profit_flag and change_price_ratio < 0 and abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
# #             tp_condition = not self.only_stop_loss_flag and change_price_ratio > 0 and change_price_ratio >= symbol_item.get("tp_pos_rate")

# #             if tp_condition or sl_condition:
# #                 print(f"Triggered closing position {pos_num} due to price for {symbol_item.get('symbol')}.")
# #                 return "closing", pos_num

# #         except Exception as ex:
# #             print(ex)
# #             return None

# #     def handle_positions(self, symbol_item):
# #         result = self.analyze_and_handle_positions(symbol_item)
# #         if not result:
# #             result = self.close_position_by_price(symbol_item)
# #         return result

# # class RULESS(VARIABLES):
# #     def __init__(self):
# #         super().__init__()

# #     def analyze_and_handle_positions(self, symbol_item):
# #         try:
# #             pos_num, hedg_num = (1, 2) if symbol_item.get("in_position_1") else (2, 1)
# #             enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #             if not isinstance(enter_pos_price, float):
# #                 return None

# #             signal = symbol_item.get("signal")
# #             cur_price = float(symbol_item.get("cur_price"))
# #             position_side = symbol_item.get(f"position_{pos_num}_side")
# #             change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #             if position_side == "LONG":
# #                 if signal == 1:
# #                     return None
# #                 if cur_price < enter_pos_price:
# #                     change_price_ratio = -change_price_ratio
# #             elif position_side == "SHORT":
# #                 if signal == -1:
# #                     return None
# #                 if cur_price > enter_pos_price:
# #                     change_price_ratio = -change_price_ratio

# #             if change_price_ratio >= symbol_item.get("min_deviation_rate"):
# #                 print(f"Triggered closing position {pos_num} due to signal for {symbol_item.get('symbol')}.")
# #                 return "closing", pos_num
# #             print(f"Hedging position {hedg_num} for {symbol_item.get('symbol')}")
# #             return "opening", hedg_num

# #         except Exception as ex:
# #             print(ex)
# #             return None

# #     def close_position_by_price(self, symbol_item):
# #         try:
# #             pos_num = 1 if symbol_item.get("in_position_1") else 2
# #             enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #             if not isinstance(enter_pos_price, float):
# #                 return None

# #             cur_price = float(symbol_item.get("cur_price"))
# #             position_side = symbol_item.get(f"position_{pos_num}_side")
# #             change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #             if position_side == "LONG":
# #                 if cur_price < enter_pos_price:
# #                     change_price_ratio = -change_price_ratio
# #             elif position_side == "SHORT":
# #                 if cur_price > enter_pos_price:
# #                     change_price_ratio = -change_price_ratio

# #             sl_condition = not self.only_take_profit_flag and change_price_ratio < 0 and abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
# #             tp_condition = not self.only_stop_loss_flag and change_price_ratio > 0 and change_price_ratio >= symbol_item.get("tp_pos_rate")

# #             if tp_condition or sl_condition:
# #                 print(f"Triggered closing position {pos_num} due to price for {symbol_item.get('symbol')}.")
# #                 return "closing", pos_num

# #         except Exception as ex:
# #             print(ex)
# #             return None

# #     def handle_positions(self, symbol_item):
# #         result = self.analyze_and_handle_positions(symbol_item)
# #         if not result:
# #             result = self.close_position_by_price(symbol_item)
# #         return result


# # class MAIN(WaitCandleLogic):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
# #         self.strategy_engin = self.log_exceptions_decorator(self.strategy_engin)
# #         self.main_engin = self.log_exceptions_decorator(self.main_engin)
# #         self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
# #         self.execute_trading_cycle = self.log_exceptions_decorator(self.execute_trading_cycle)

# #     async def hedge_or_close_analizator(self, rules_analizes_func):
# #         is_any_close_pos = False
# #         is_any_opening = False

# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             rules_analizes_func_repl = rules_analizes_func(symbol_item)
# #             if rules_analizes_func_repl:
# #                 opeing_or_closing, pos_num = rules_analizes_func_repl
# #                 if opeing_or_closing == "closing":
# #                     is_any_close_pos = self.trading_data_list[i][f"is_closing_{pos_num}_pos"] = True
# #                 elif opeing_or_closing == "opening":
# #                     is_any_opening = True
# #                     self.trading_data_list[i][f"is_opening_{pos_num}_pos"] = True
# #         if is_any_close_pos or is_any_opening:
# #             await self.make_orders_total_template()
# #             self.check_finish_flag = True
# #             return True
# #         return False

# #     async def strategy_engin(self):
# #         if self.is_get_new_signal:
# #             self.is_get_new_signal = False          
# #             if not await self.hedge_or_close_analizator(self.is_close_some_pos_by_signal_or_hedging):
# #                 await self.hedge_or_close_analizator(self.close_any_pos_by_signal)
# #             return
# #         await self.hedge_or_close_analizator(self.close_any_pos_by_price)

# #     @aiohttp_connector
# #     async def execute_trading_cycle(self, session):     
# #         await self.wait_for_candle_or_coins(session)
# #         tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
# #         await asyncio.gather(*tasks)

# #         if self.trading_data_list:                
# #             self.trading_data_list = self.trading_data_list[:self.diversification_number]
# #             [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
# #             # make initial orders:
# #             await self.make_orders_total_template()
# #             if any(symbol_item.get("in_position_1") for symbol_item in self.trading_data_list):
# #                 self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
# #                 return True        
# #         return False

# #     async def main_engin(self):
# #         self.handle_messagee("Устанавливаем режим хеджирования:")
# #         set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
# #         self.handle_messagee(str(set_hedge_mode_answ))

# #         while True:
# #             if self.next_trading_cycle:
# #                 await asyncio.sleep(0.5)
# #                 if not await self.execute_trading_cycle():
# #                     print("На данный момент нет ни одного сигнала...")
# #                     continue
# #                 self.next_trading_cycle = False
# #                 self.wb_task_true = True 
# #                 print(self.trading_data_list)

# #             if self.wb_task_true:               
# #                 self.wb_task_true = False
# #                 symbols = [x.get("symbol") for x in self.trading_data_list]
# #                 self.wb_task = [self.connect_to_websocket(symbols, self.recent_klines_dict)]
# #                 self.wb_completed_task = asyncio.gather(*self.wb_task)

# #             # print("tik")
# #             await asyncio.sleep(1)
# #             self.check_finish_tik_counter += 1
# #             if self.check_finish_tik_counter == 10 or self.check_finish_flag:
# #                 print("self.check_finish_tik_counter == 10 or self.check_finish_flag")
# #                 self.check_finish_flag = False
# #                 self.check_finish_tik_counter = 0
# #                 async with self.lock:                    
# #                     self.next_trading_cycle = await self.is_finish_trade_cycle_true()
# #                     if self.next_trading_cycle:
# #                         self.next_trading_cycle_event.set()                        
# #                         while True:
# #                             if self.wb_completed_task and self.wb_completed_task.done():                             
# #                                 print("конец первой торговой итерации")
# #                                 break 
# #                             # print("Не удается закрыть вебсокет соединение")
# #                             await asyncio.sleep(2)
# #                         self.init_and_reset_data()
# #                         continue

# #             self.strategy_engin_tik_counter += 1
# #             if (self.strategy_engin_tik_counter == 2 or self.is_get_new_signal):
# #                 self.strategy_engin_tik_counter = 0
# #                 async with self.lock:
# #                     await self.strategy_engin()

# # if __name__ == "__main__":
# #     asyncio.run(MAIN().main_engin())

# # class MAIN(WaitCandleLogic):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
# #         self.strategy_engin = self.log_exceptions_decorator(self.strategy_engin)
# #         self.main_engin = self.log_exceptions_decorator(self.main_engin)
# #         self.execute_trading_cycle = self.log_exceptions_decorator(self.execute_trading_cycle)

# #     async def hedge_or_close_analizator(self):
# #         is_any_close_pos = False
# #         is_any_opening = False

# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             result = self.handle_positions(symbol_item)
# #             if result:
# #                 action, pos_num = result
# #                 if action == "closing":
# #                     is_any_close_pos = self.trading_data_list[i][f"is_closing_{pos_num}_pos"] = True
# #                 elif action == "opening":
# #                     is_any_opening = True
# #                     self.trading_data_list[i][f"is_opening_{pos_num}_pos"] = True

# #         if is_any_close_pos or is_any_opening:
# #             await self.make_orders_total_template()
# #             self.check_finish_flag = True
# #             return True
# #         return False

# #     async def strategy_engin(self):
# #         if self.is_get_new_signal:
# #             self.is_get_new_signal = False
# #             if not await self.hedge_or_close_analizator():
# #                 await self.hedge_or_close_analizator()
# #             return
# #         await self.hedge_or_close_analizator()

# #     @aiohttp_connector
# #     async def execute_trading_cycle(self, session):     
# #         await self.wait_for_candle_or_coins(session)
# #         tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
# #         await asyncio.gather(*tasks)

# #         if self.trading_data_list:
# #             self.trading_data_list = self.trading_data_list[:self.diversification_number]
# #             [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
# #             await self.make_orders_total_template()
# #             if any(symbol_item.get("in_position_1") for symbol_item in self.trading_data_list):
# #                 self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
# #                 return True
# #         return False

# #     async def main_engin(self):
# #         self.handle_messagee("Устанавливаем режим хеджирования:")
# #         set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
# #         self.handle_messagee(str(set_hedge_mode_answ))

# #         while True:
# #             if self.next_trading_cycle:
# #                 await asyncio.sleep(0.5)
# #                 if not await self.execute_trading_cycle():
# #                     print("На данный момент нет ни одного сигнала...")
# #                     continue
# #                 self.next_trading_cycle = False
# #                 self.wb_task_true = True
# #                 print(self.trading_data_list)

# #             if self.wb_task_true:
# #                 self.wb_task_true = False
# #                 symbols = [x.get("symbol") for x in self.trading_data_list]
# #                 self.wb_task = [self.connect_to_websocket(symbols, self.recent_klines_dict)]
# #                 self.wb_completed_task = asyncio.gather(*self.wb_task)

# #             await asyncio.sleep(1)
# #             self.check_finish_tik_counter += 1
# #             if self.check_finish_tik_counter == 10 or self.check_finish_flag:
# #                 print("self.check_finish_tik_counter == 10 or self.check_finish_flag")
# #                 self.check_finish_flag = False
# #                 self.check_finish_tik_counter = 0
# #                 async with self.lock:
# #                     self.next_trading_cycle = await self.is_finish_trade_cycle_true()
# #                     if self.next_trading_cycle:
# #                         self.next_trading_cycle_event.set()
# #                         while True:
# #                             if self.wb_completed_task and self.wb_completed_task.done():
# #                                 print("конец первой торговой итерации")
# #                                 break
# #                             await asyncio.sleep(2)
# #                         self.init_and_reset_data()
# #                         continue

# #             self.strategy_engin_tik_counter += 1
# #             if self.strategy_engin_tik_counter == 2 or self.is_get_new_signal:
# #                 self.strategy_engin_tik_counter = 0
# #                 async with self.lock:
# #                     await self.strategy_engin()

# # if __name__ == "__main__":
# #     asyncio.run(MAIN().main_engin())


# # from vars import VARIABLES

# # class RULESS(VARIABLES):
# #     def __init__(self):
# #         super().__init__()

# #     def handle_positions_rules(self, symbol_item):
# #         try:
# #             if symbol_item.get("in_position_1") or symbol_item.get("in_position_2"):
# #                 instruction_list = []
# #                 for pos_num in [1,2]:
# #                     if not symbol_item[f"in_position_{pos_num}"]:
# #                         continue
# #                     hedg_num = 2 if pos_num == 1 else 1
# #                     enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
# #                     if not isinstance(enter_pos_price, float):
# #                         continue

# #                     cur_price = float(symbol_item.get("cur_price"))
# #                     position_side = symbol_item.get(f"position_{pos_num}_side")
# #                     signal = symbol_item.get("signal")
# #                     change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

# #                     if position_side == "LONG":
# #                         if signal == 1:
# #                             continue
# #                         if cur_price < enter_pos_price:
# #                             change_price_ratio = -change_price_ratio
# #                     elif position_side == "SHORT":
# #                         if signal == -1:
# #                             continue
# #                         if cur_price > enter_pos_price:
# #                             change_price_ratio = -change_price_ratio

# #                     if not signal:
# #                         # Check if we should close the position due to price
# #                         sl_condition = not self.only_take_profit_flag and change_price_ratio < 0 and abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
# #                         tp_condition = not self.only_stop_loss_flag and change_price_ratio > 0 and change_price_ratio >= symbol_item.get("tp_pos_rate")

# #                         if tp_condition or sl_condition:
# #                             print(f"Triggered closing position {pos_num} due to price for {symbol_item.get('symbol')}.")
# #                             instruction_list.append(("closing", pos_num))                    
# #                     else:
# #                         # Check if we should close the position due to signal
# #                         if change_price_ratio >= symbol_item.get("min_deviation_rate"):
# #                             print(f"Triggered closing position {pos_num} due to signal for {symbol_item.get('symbol')}.")
# #                             instruction_list.append(("closing", pos_num))
# #                             continue
# #                         print(f"Triggered hedging position {pos_num} due to signal for {symbol_item.get('symbol')}.")
# #                         instruction_list.append(("opening", hedg_num))

# #                 return instruction_list

# #         except Exception as ex:
# #             print(ex)
# #         return []



        
#     # async def is_closing_position_true(self, session, symbol, position_side):
#     #     params = {
#     #         "symbol": symbol,
#     #         "positionSide": position_side,
#     #         'recvWindow': 20000,            
#     #     }
#     #     try:
#     #         params = self.get_signature(params)
#     #         async with session.get(self.positions_url, headers=self.headers, params=params) as response:
#     #             positions = await response.json()
#     #         for position in positions:
#     #             if position['symbol'] == symbol and position['positionSide'] == position_side and float(position['positionAmt']) != 0:
#     #                 return False, symbol
#     #         return True, symbol
#     #     except Exception as ex:
#     #         print(ex)
#     #     return False, symbol



# # class MAIN(WaitCandleLogic):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
# #         self.main_engin = self.log_exceptions_decorator(self.main_engin)
# #         self.execute_trading_cycle = self.log_exceptions_decorator(self.execute_trading_cycle)

# #     async def hedge_or_close_analizator(self):
# #         is_any_close_pos = False
# #         is_any_opening = False

# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             result = self.handle_positions_rules(symbol_item)
# #             if result:
# #                 for action, pos_num in result:
# #                     if action == "closing":
# #                         is_any_close_pos = self.trading_data_list[i][f"is_closing_{pos_num}_pos"] = True
# #                     elif action == "opening":
# #                         is_any_opening = True
# #                         self.trading_data_list[i][f"is_opening_{pos_num}_pos"] = True

# #         if is_any_close_pos or is_any_opening:
# #             await self.make_orders_total_template()           
# #             return True
# #         return False

# #     @aiohttp_connector
# #     async def execute_trading_cycle(self, session):     
# #         await self.wait_for_candle_or_coins(session)
# #         tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
# #         await asyncio.gather(*tasks)

# #         if self.trading_data_list:
# #             self.trading_data_list = self.trading_data_list[:self.diversification_number]
# #             [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
# #             await self.make_orders_total_template()
# #             if any(symbol_item.get("in_position_1") for symbol_item in self.trading_data_list):
# #                 self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
# #                 return True
# #         return False

# #     async def main_engin(self):
# #         self.handle_messagee("Устанавливаем режим хеджирования:")
# #         set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
# #         self.handle_messagee(str(set_hedge_mode_answ))

# #         while True:
# #             if self.next_trading_cycle:
# #                 await asyncio.sleep(0.5)
# #                 if not await self.execute_trading_cycle():
# #                     print("Продолжаем искать сигналы...")
# #                     continue
# #                 self.next_trading_cycle = False
# #                 self.wb_task_true = True
# #                 print(self.trading_data_list)

# #             if self.wb_task_true:
# #                 self.wb_task_true = False
# #                 symbols = [x.get("symbol") for x in self.trading_data_list]
# #                 self.wb_task = [self.connect_to_websocket(symbols, self.recent_klines_dict)]
# #                 self.wb_completed_task = asyncio.gather(*self.wb_task)

# #             await asyncio.sleep(1)
# #             self.check_finish_tik_counter += 1
# #             if self.check_finish_tik_counter == 10 or self.check_finish_flag:
# #                 print("self.check_finish_tik_counter == 10 or self.check_finish_flag")
# #                 self.check_finish_flag = False
# #                 self.check_finish_tik_counter = 0
# #                 async with self.lock:
# #                     self.next_trading_cycle = await self.is_finish_trade_cycle_true()
# #                     if self.next_trading_cycle:
# #                         self.next_trading_cycle_event.set()
# #                         while True:
# #                             if self.wb_completed_task and self.wb_completed_task.done():
# #                                 print("конец первой торговой итерации")
# #                                 break
# #                             await asyncio.sleep(1)
# #                         self.init_and_reset_data()
# #                         continue

# #             self.strategy_engin_tik_counter += 1
# #             if self.strategy_engin_tik_counter == 2 or self.is_get_new_signal:
# #                 self.strategy_engin_tik_counter = 0
# #                 async with self.lock:                    
# #                     self.is_get_new_signal = False
# #                     self.check_finish_flag = await self.hedge_or_close_analizator()            

# # if __name__ == "__main__":
# #     asyncio.run(MAIN().main_engin())





#     # async def connect_to_websocket(self, symbols, recent_klines_dict):
#     #     print("connect_to_websocket")
#     #     stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
#     #     is_wb_finish = False
#     #     for chunk in stream_chunks:
#     #         streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
#     #         url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
#     #         async with websockets.connect(url) as websocket:
#     #             async for message in websocket:
#     #                 await self.handle_wb_message(message, recent_klines_dict)
#     #                 # if self.next_trading_cycle_event.is_set(): 
#     #                 if self.next_trading_cycle:
#     #                     # is_wb_finish = True
#     #                     break
#     #         # if is_wb_finish:
#     #         if self.next_trading_cycle:
#     #             break
#     #     # self.next_trading_cycle_event.clear()
#     #     return is_wb_finish



#             # self.check_finish_tik_counter += 1
#             # if self.check_finish_tik_counter == 10 or self.check_finish_flag:
#             #     print("self.check_finish_tik_counter == 10 or self.check_finish_flag")
#             #     self.check_finish_flag = False
#             #     self.check_finish_tik_counter = 0
#             #     async with self.lock:
#             #         self.next_trading_cycle = await self.is_finish_trade_cycle_true()
#             #     if self.next_trading_cycle:
#             #         self.next_trading_cycle_event.set()
#             #         while True:
#             #             if self.wb_completed_task and self.wb_completed_task.done():
#             #                 print("конец первой торговой итерации")
#             #                 break
#             #             print("Не удается закрыть вебсокет")
#             #             await asyncio.sleep(2)
#             #         # self.next_trading_cycle_event.clear()
#             #         self.init_and_reset_data()
#             #         continue







#     # @aiohttp_connector
#     # async def execute_trading_cycle(self, session):
#     #     await self.wait_for_candle_or_coins(session)
#     #     tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
#     #     await asyncio.gather(*tasks)

#     #     if self.trading_data_list:
#     #         print(f"total_init_signal_counter: {len(self.trading_data_list)}")            
#     #         [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
            
#     #         signals_stock = max(len(self.trading_data_list), self.diversification_number + 1)
#     #         data_in_action_len = 0

#     #         for i in range(0, signals_stock, self.diversification_number):
#     #             self.trading_data_list = self.trading_data_list[i:self.diversification_number + i]
#     #             await self.make_orders_total_template()
#     #             data_in_action_len += sum(1 for x in self.trading_data_list if x.get("in_position_1"))

#     #             if data_in_action_len >= self.diversification_number:
#     #                 self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
#     #                 return True

#     #         # Если после всех попыток не удалось набрать достаточное количество позиций
#     #         self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
#     #         if self.trading_data_list:
#     #             return True

#     #     return False


#     # @aiohttp_connector
#     # async def execute_trading_cycle(self, session):     
#     #     await self.wait_for_candle_or_coins(session)
#     #     tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
#     #     await asyncio.gather(*tasks)

#     #     if self.trading_data_list:
#     #         trading_data_list_not_hidden = self.trading_data_list
#     #         print(f"total_init_signal_counter: {len(trading_data_list_not_hidden)}")            
#     #         [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
#     #         signals_stock = len(trading_data_list_not_hidden)-self.diversification_number
#     #         signals_stock = len(trading_data_list_not_hidden) + 1 if signals_stock > 0 else self.diversification_number + 1
#     #         data_in_action_len = 0
#     #         for i in range(0, signals_stock, self.diversification_number):
#     #             self.trading_data_list = self.trading_data_list[i:self.diversification_number+i-1]
#     #             await self.make_orders_total_template()
#     #             data_in_action_len += sum(1 for x in self.trading_data_list if x.get("in_position_1"))
#     #             if data_in_action_len == self.diversification_number:
#     #                 self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
#     #                 return True
#     #     return False

# # s = {
# #     's': 1,
# #     'f': 2
# # }
# # n = {}
# # b_li = ['s']

# # for i, item in enumerate(s.items()):
# #     if item[0] in b_li:
# #         n[item[0]] = item[1]
        
# # print(n)


# # s = {
# #     's': 1,
# #     'f': 2
# # }
# # b_li = ['s']

# # n = {k: v for k, v in s.items() if k in b_li}

# # print(n)

# import random

# def foo():
#     diversification_number = 5
#     trade_li = [1,2,3,4,5,6,7,8,9,10,11,12,13]
#     signals_stock = len(trade_li)

#     if signals_stock >= diversification_number:                            
#         step = diversification_number 
#     else:
#         step = signals_stock

#     for i in range(0, signals_stock, step):
#         print(trade_li[i:step+i])
#         data_in_action_len = random.randrange(i, step+i)

#         if data_in_action_len >= diversification_number:             
            
#             return True
        
#         step = diversification_number - data_in_action_len

#             remaining_signals = len(self.trading_data_init_list) % self.diversification_number
                
#             if remaining_signals != 0:
#                 tradin_tail = remaining_signals-data_in_action_len if remaining_signals - data_in_action_len > 0 else remaining_signals
#                 self.trading_data_list = self.trading_data_init_list[-tradin_tail]
#                 await self.make_orders_total_template()
#                 trading_data_asum_list += [x for x in self.trading_data_list if x.get("in_position_1")]
                            
#             if len(trading_data_asum_list) > 0:
#                 self.trading_data_list = trading_data_asum_list
#                 return True

#         return False





    # @aiohttp_connector
    # async def execute_trading_cycle(self, session):
    #     await self.wait_for_candle_or_coins(session)
    #     tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
    #     await asyncio.gather(*tasks)

    #     if self.trading_data_init_list:
    #         print(f"total_init_signal_counter: {len(self.trading_data_init_list)}")            
    #         [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_init_list]

    #         trading_data_asum_list = []
    #         signals_stock = len(self.trading_data_init_list)
    #         step = min(self.diversification_number, signals_stock)

    #         for i in range(0, signals_stock, step):
    #             self.trading_data_list = self.trading_data_init_list[i:step + i]
    #             await self.make_orders_total_template()
    #             trading_data_asum_list += [x for x in self.trading_data_list if x.get("in_position_1")]

    #             if len(trading_data_asum_list) >= self.diversification_number:
    #                 self.trading_data_list = trading_data_asum_list[:self.diversification_number]
    #                 return True

    #             # Обновление шага для следующей итерации, чтобы учитывать оставшиеся позиции
    #             step = min(self.diversification_number - len(trading_data_asum_list), signals_stock - i - step)

    #         if len(trading_data_asum_list) > 0:
    #             self.trading_data_list = trading_data_asum_list
    #             return True

    #     return False


    # @aiohttp_connector
    # async def execute_trading_cycle(self, session):
    #     await self.wait_for_candle_or_coins(session)
    #     tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
    #     await asyncio.gather(*tasks)

    #     if self.trading_data_init_list:
    #         print(f"total_init_signal_counter: {len(self.trading_data_init_list)}")            
    #         [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_init_list]

    #         trading_data_asum_list = []
    #         signals_stock = len(self.trading_data_init_list)
    #         if signals_stock >= self.diversification_number:                            
    #             step = self.diversification_number 
    #         else:
    #             step = signals_stock                   

    #         for i in range(0, signals_stock, step):
    #             self.trading_data_list = self.trading_data_init_list[i:step + i]
    #             await self.make_orders_total_template()
    #             trading_data_asum_list += [x for x in self.trading_data_list if x.get("in_position_1")]
    #             len(trading_data_asum_list)

    #             if len(trading_data_asum_list) >= self.diversification_number:                    
    #                 self.trading_data_list = trading_data_asum_list
    #                 return True

    #             step = step - len(trading_data_asum_list) if step > len(trading_data_asum_list) else 1

    #         if len(trading_data_asum_list) > 0:
    #             self.trading_data_list = trading_data_asum_list
    #             return True

    #     return False



            # if ema_cross == 1:
            #     print(f"Initial buy signal for {symbol} at price {current_close}")
            # elif ema_cross == -1:
            #     print(f"Initial sell signal for {symbol} at price {current_close}")




    # async def connect_to_websocket(self, symbols, recent_klines_dict):
    #     print("connect_to_websocket")
    #     stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
    #     is_wb_finish = False

    #     for chunk in stream_chunks:
    #         streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
    #         url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"

    #         async with websockets.connect(url) as websocket:
    #             async for message in websocket:
    #                 await self.handle_wb_message(message, recent_klines_dict)

    #                 if self.next_trading_cycle_event.is_set():
    #                     is_wb_finish = True
    #                     await websocket.close()
    #                     break

    #         if is_wb_finish:
    #             break

    #     # Проверяем завершение внешнего цикла после закрытия сокета
    #     if self.next_trading_cycle_event.is_set():
    #         is_wb_finish = True

    #     return is_wb_finish


    # async def connect_to_websocket(self, symbols, recent_klines_dict):
    #     print("connect_to_websocket")
    #     stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]  # Dividing symbols into chunks
    #     is_wb_finish = False
    #     for chunk in stream_chunks:
    #         streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]  # Example using 1-minute interval
    #         url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
    #         async with websockets.connect(url) as websocket:
    #             async for message in websocket:
    #                 await self.handle_wb_message(message, recent_klines_dict)                    
    #                 if self.next_trading_cycle_event.is_set():                                                  
    #                     is_wb_finish = True 
    #                     await websocket.close()
    #                     break
    #         if self.next_trading_cycle_event.is_set():
    #             # print(f"is_wb_finish2: {is_wb_finish}")
    #             is_wb_finish = True
    #             break        
    #     return is_wb_finish