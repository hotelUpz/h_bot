import numpy as np
import asyncio
from utils import UTILS

class SORT_DATA(UTILS):
    def __init__(self) -> None:
        super().__init__()
        self.is_get_new_signal = False
        self.lock = asyncio.Lock()

    def symbol_data_reprocessing(self, symbol, signal, cur_price):  
        for i, symbol_item in enumerate(self.signals_data_list):            
            if symbol_item["symbol"] == symbol:
                try:
                    self.signals_data_list[i]['cur_price'] = cur_price
                    print(f"Монета: {symbol} цена: {cur_price}")

                    if signal and signal != symbol_item["first_signal"]:
                        print(f"Монета: {symbol} сигнал: {signal} цена: {cur_price}")
                        self.signals_data_list[i]['signal'] = signal 

                        if self.signals_data_list[i].get("position_1_side") == 'LONG':
                            self.signals_data_list[i]["position_2_side"] = "SHORT"
                            self.signals_data_list[i]["side_2"] = "SELL"
                        elif self.signals_data_list[i].get("position_1_side") == 'SHORT':
                            self.signals_data_list[i]["position_2_side"] = "LONG"
                            self.signals_data_list[i]["side_2"] = "BUY"
                        else:
                            print(f"Монета: {symbol} имеет неизвестное значение position_1_side: {self.signals_data_list[i].get('position_1_side')}")
                            
                    break
                except Exception as ex:
                    print(ex)

        return not signal == 0    

    def add_signal_to_list(self, symbol, current_close, ema_cross):
        signal_data = {
            "symbol": symbol,
            "cur_price": current_close,
            "enter_1_pos_price": None,
            "enter_2_pos_price": None,
            "signal": ema_cross,
            "first_signal": ema_cross,
            "quantity_precision": None,
            "min_notional": None,
            "qty_1": 0,
            "qty_2": 0,
            "in_position_1": False,
            "in_position_2": False,
            "position_1_side": "LONG" if ema_cross == 1 else "SHORT",
            "position_2_side": None,
            "is_total_closing": False,
            "side_1": "BUY" if ema_cross == 1 else "SELL",
            "side_2": None,
            "sl_1_pos_rate": self.sl_1_pos_rate / 100,
            "tp_1_pos_rate": self.tp_1_pos_rate / 100,
            "sl_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[0].strip()),
            "tp_risk_reward_multiplier": float(self.risk_reward_ratio.split(':')[1].strip()),
            "sl_price_1_pos": 0,
            "tp_price_1_pos": 0,
            "current_step_counter": self.current_step_counter,
            "position_1_averaging_counter": self.position_1_averaging_counter,
        }
        self.signals_data_list.append(signal_data)

    async def process_kline_data(self, kline_data, recent_klines, symbol):
        open_time = kline_data['t']
        open_price = float(kline_data['o'])
        high_price = float(kline_data['h'])
        low_price = float(kline_data['l'])
        close_price = float(kline_data['c'])
        volume = float(kline_data['v'])

        recent_klines.append([open_time, open_price, high_price, low_price, close_price, volume])

        if len(recent_klines) > self.ema2_period:
            recent_klines.pop(0)

        if len(recent_klines) >= self.ema2_period:
            close_prices = np.array([kline[4] for kline in recent_klines])

            # Найти последнее пересечение EMA
            ema_cross = await self.find_last_ema_cross(close_prices)
            current_close = close_prices[-1]

            async with self.lock:
                self.is_get_new_signal = self.symbol_data_reprocessing(symbol, ema_cross, current_close)

    async def process_historical_klines(self, recent_klines, symbol):
        if len(recent_klines) >= self.ema2_period:
            close_prices = np.array([kline[4] for kline in recent_klines])

            # Найти последнее пересечение EMA
            ema_cross = await self.find_last_ema_cross(close_prices)

            current_close = close_prices[-1]

            if symbol == 'NOTUSDT':  # test
                ema_cross == 1

            if ema_cross == 1:
                print(f"Initial buy signal for {symbol} at price {current_close}")
            elif ema_cross == -1:
                print(f"Initial sell signal for {symbol} at price {current_close}")

            if ema_cross:
                self.add_signal_to_list(symbol, current_close, ema_cross)

    async def fetch_and_process_symbol(self, session, symbol, recent_klines_dict, trends_dict):
        recent_klines = await self.get_klines(session, symbol, self.interval, self.ema1_period + self.ema2_period)
        recent_klines_dict[symbol] = recent_klines.tolist()
        await self.process_historical_klines(recent_klines_dict[symbol], symbol)