import numpy as np
from utils import UTILS

class REFACT_DATA(UTILS):
    def __init__(self) -> None:
        super().__init__()
        self.klines_historical_lim = self.ema1_period + self.ema2_period
        self.symbol_item_creator = self.log_exceptions_decorator(self.symbol_item_creator)
        self.symbol_data_reprocessing = self.log_exceptions_decorator(self.symbol_data_reprocessing)
        self.process_trading_data = self.log_exceptions_decorator(self.process_trading_data)
        self.process_historical_klines = self.log_exceptions_decorator(self.process_historical_klines)
        self.fetch_and_process_symbol = self.log_exceptions_decorator(self.fetch_and_process_symbol)        

    def symbol_item_creator(self, symbol, current_close, ema_cross):
        signal_data = {
            "symbol": symbol,
            "cur_price": current_close,
            "enter_1_pos_price": None,
            "enter_2_pos_price": None,
            "signal": ema_cross,
            "first_trade": True,
            "quantity_precision": None,
            "min_notional": None,
            "qty": 0,
            "in_position_1": False,
            "in_position_2": False,
            "is_opening_1_pos": True,
            "is_opening_2_pos": False,
            "is_closing_1_pos": False,
            "is_closing_2_pos": False,
            "position_1_side": "LONG" if ema_cross == 1 else "SHORT",
            "position_2_side": "LONG" if ema_cross == -1 else "SHORT",
            "sl_pos_rate": (self.sl_1_pos_rate / 100) * float(self.risk_reward_ratio.split(':')[0].strip()),
            "tp_pos_rate": (self.tp_1_pos_rate / 100) * float(self.risk_reward_ratio.split(':')[1].strip()),
            "min_deviation_rate": self.min_deviation_rate / 100,
        }
        self.trading_data_init_list.append(signal_data)
     
    def symbol_data_reprocessing(self, symbol, cur_price, signal=None):
        for i, symbol_item in enumerate(self.trading_data_list):
            if symbol_item["symbol"] == symbol:
                try:
                    self.trading_data_list[i]['cur_price'] = cur_price
                    if signal:
                        print(f"Монета: {symbol} сигнал: {signal* self.is_reverse_signal} цена: {cur_price}")
                        self.trading_data_list[i]['signal'] = signal* self.is_reverse_signal
                        self.is_get_new_signal = True
                    break
                except Exception as ex:
                    print(ex)

    async def process_trading_data(self, wb_kline_data, symbol, is_kline_closed_true):        
        close_wb_price = float(wb_kline_data['c'])
        if not is_kline_closed_true:
            self.symbol_data_reprocessing(symbol, close_wb_price)
        else:
            # print("is_kline_closed")
            async with self.lock:                
                close_prices_2 = await self.get_close_prices(symbol, self.interval, self.klines_historical_lim)
                ema_cross_2 = self.find_last_ema_cross(close_prices_2)
                self.symbol_data_reprocessing(symbol, close_wb_price, ema_cross_2)

    def process_historical_klines(self, recent_klines, symbol):
        if len(recent_klines) >= self.ema2_period:
            close_prices = np.array([float(kline[4]) for kline in recent_klines], dtype=np.float64)
            ema_cross = self.find_last_ema_cross(close_prices)
            current_close = close_prices[-1]
            ema_cross = ema_cross * self.is_reverse_signal
            if ema_cross:
                if not ((self.only_long_trading and ema_cross == -1) or (self.only_short_trading and ema_cross == 1)):
                    self.symbol_item_creator(symbol, current_close, ema_cross)

    async def fetch_and_process_symbol(self, session, symbol, recent_klines_dict):
        recent_klines = await self.get_klines(session, symbol, self.interval, self.klines_historical_lim)
        recent_klines_dict[symbol] = recent_klines.tolist()
        self.process_historical_klines(recent_klines_dict[symbol], symbol)