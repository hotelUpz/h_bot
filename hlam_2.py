
# #     # def should_update_klines(self, interval, unit):
# #     #     """
# #     #     interval: int, количество интервалов
# #     #     unit: str, единица времени ('m' для минут, 'h' для часов)
# #     #     """
# #     #     if unit == 'm':
# #     #         interval_seconds = (interval * 60) - 60
# #     #     elif unit == 'h':
# #     #         interval_seconds = (interval * 60 * 60) - (60 * 60)
# #     #     else:
# #     #         raise ValueError("Unsupported unit. Use 'm' for minutes or 'h' for hours.")

# #     #     elapsed_time = time.time() - self.start_time
# #     #     if elapsed_time >= interval_seconds:
# #     #         self.start_time = time.time()  # Reset start time
# #     #         return True
# #     #     return False


# # import numpy as np
# # from utils import UTILS

# # class REFACT_DATA(UTILS):
# #     def __init__(self) -> None:
# #         super().__init__()
# #         self.klines_historical_lim = self.ema1_period + self.ema2_period
# #         self.symbol_item_creator = self.log_exceptions_decorator(self.symbol_item_creator)
# #         self.symbol_data_reprocessing = self.log_exceptions_decorator(self.symbol_data_reprocessing)
# #         self.process_trading_data = self.log_exceptions_decorator(self.process_trading_data)
# #         self.process_historical_klines = self.log_exceptions_decorator(self.process_historical_klines)
# #         self.fetch_and_process_symbol = self.log_exceptions_decorator(self.fetch_and_process_symbol)        

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
# #             "sl_pos_rate": (self.sl_1_pos_rate / 100) * float(self.risk_reward_ratio.split(':')[0].strip()),
# #             "tp_pos_rate": (self.tp_1_pos_rate / 100) * float(self.risk_reward_ratio.split(':')[1].strip()),
# #             "min_deviation_rate": self.min_deviation_rate / 100,
# #         }
# #         self.trading_data_init_list.append(signal_data)
     
# #     def symbol_data_reprocessing(self, symbol, cur_price, signal=None):
# #         for i, symbol_item in enumerate(self.trading_data_list):
# #             if symbol_item["symbol"] == symbol:
# #                 try:
# #                     self.trading_data_list[i]['cur_price'] = cur_price
# #                     if signal:
# #                         print(f"Монета: {symbol} сигнал: {signal* self.is_reverse_signal} цена: {cur_price}")
# #                         self.trading_data_list[i]['signal'] = signal* self.is_reverse_signal
# #                         self.is_get_new_signal = True
# #                     break
# #                 except Exception as ex:
# #                     print(ex)

# #     async def process_trading_data(self, wb_kline_data, recent_klines, symbol, is_kline_closed_true):        
# #         close_wb_price = float(wb_kline_data['c'])
# #         if not is_kline_closed_true:
# #             self.symbol_data_reprocessing(symbol, close_wb_price)
# #         else:
# #             print("is_kline_closed")
# #             async with self.lock:
# #                 if recent_klines:
# #                     self.first_update_done = True
# #                     open_time = wb_kline_data['t']
# #                     open_price = float(wb_kline_data['o'])
# #                     high_price = float(wb_kline_data['h'])
# #                     low_price = float(wb_kline_data['l'])
# #                     volume = float(wb_kline_data['v'])

# #                     if not self.should_update_klines(self.kline_time, self.time_frame): 
# #                         print("NOT self.should_update_klines")                   
# #                         recent_klines[-1] = [open_time, open_price, high_price, low_price, close_wb_price, volume]
# #                     else:
# #                         print("IS!!! self.should_update_klines")                                             
# #                         recent_klines.append([open_time, open_price, high_price, low_price, close_wb_price, volume])             
# #                         if len(recent_klines) > self.klines_historical_lim:
# #                             del recent_klines[0]

# #                     if len(recent_klines) >= self.klines_historical_lim:                    
# #                         close_prices = np.array([float(kline[4]) for kline in recent_klines], dtype=np.float64)
# #                         print(f"close_prices_wb: {close_prices}")
# #                         ema_cross = await self.find_last_ema_cross(close_prices)
                        
# #                         close_prices_2 = await self.get_close_prices(symbol, self.interval, self.klines_historical_lim)
# #                         ema_cross_2 = await self.find_last_ema_cross(close_prices_2)
# #                         print(f"close_prices_klines: {close_prices_2}")                    
                        
# #                         print(f"ema_cross_wb: {ema_cross}")
# #                         print(f"ema_cross_klines: {ema_cross_2}")
# #                         self.symbol_data_reprocessing(symbol, close_wb_price, ema_cross_2)

# #     async def process_historical_klines(self, recent_klines, symbol):
# #         if len(recent_klines) >= self.ema2_period:
# #             close_prices = np.array([float(kline[4]) for kline in recent_klines], dtype=np.float64)
# #             # print(close_prices)
# #             ema_cross = await self.find_last_ema_cross(close_prices)
# #             current_close = close_prices[-1]
# #             ema_cross = ema_cross * self.is_reverse_signal
# #             if ema_cross:
# #                 if not ((self.only_long_trading and ema_cross == -1) or (self.only_short_trading and ema_cross == 1)):
# #                     self.symbol_item_creator(symbol, current_close, ema_cross)

# #     async def fetch_and_process_symbol(self, session, symbol, recent_klines_dict):
# #         recent_klines = await self.get_klines(session, symbol, self.interval, self.klines_historical_lim)
# #         recent_klines_dict[symbol] = recent_klines.tolist()
# #         await self.process_historical_klines(recent_klines_dict[symbol], symbol)

# import json
# import websockets
# import time
# from data_sorting import REFACT_DATA

# WEBSOCKET_URL = "wss://fstream.binance.com/"

# class WS_STREAMS(REFACT_DATA):
#     def __init__(self) -> None:
#         super().__init__()
#         self.handle_ws_message = self.log_exceptions_decorator(self.handle_ws_message)
#         self.connect_to_websocket = self.log_exceptions_decorator(self.connect_to_websocket)

#     async def handle_ws_message(self, message, recent_klines_dict):
#         message = json.loads(message)['data']
#         if message['e'] == 'kline':
#             is_kline_closed_true = message['k']['x']
#             symbol = message['s']
#             if (symbol not in recent_klines_dict) and is_kline_closed_true:
#                 recent_klines_dict[symbol] = []
#             await self.process_trading_data(message['k'], recent_klines_dict[symbol], symbol, is_kline_closed_true)

#     async def connect_to_websocket(self, symbols, recent_klines_dict):
#         print("connect_to_websocket")
#         self.start_time = time.time() 
#         self.start_time_2 = self.start_time
#         print(f"self.start_time: {self.start_time}")
#         stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
#         is_wb_finish = False

#         async def connect_and_handle(chunk):
#             streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
#             url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
#             async with websockets.connect(url) as websocket:
#                 async for message in websocket:
#                     await self.handle_ws_message(message, recent_klines_dict)
#                     if self.next_trading_cycle_event.is_set():
#                         await websocket.close()
#                         return True
#             return False

#         for chunk in stream_chunks:
#             if await connect_and_handle(chunk):
#                 is_wb_finish = True
#                 break

#         # Проверяем завершение внешнего цикла после закрытия сокета
#         if self.next_trading_cycle_event.is_set():
#             is_wb_finish = True

#         return is_wb_finish
 