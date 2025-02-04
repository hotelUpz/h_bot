import time
from datetime import datetime as dttm
import math
from indicator_strategy import COInN_FILTERR

class UTILS(COInN_FILTERR):
    def __init__(self):  
        super().__init__()
        self.milliseconds_to_datetime = self.log_exceptions_decorator(self.milliseconds_to_datetime)
        self.time_calibrator = self.log_exceptions_decorator(self.time_calibrator)
        self.count_decimal_places = self.log_exceptions_decorator(self.count_decimal_places)
        self.get_precisions = self.log_exceptions_decorator(self.get_precisions)
        self.usdt_to_qnt_converter = self.log_exceptions_decorator(self.usdt_to_qnt_converter)
                        
    def milliseconds_to_datetime(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000)
        time = dttm.utcfromtimestamp(seconds)
        return time.strftime('%Y-%m-%d %H:%M:%S')
    
    def time_calibrator(self, kline_time, time_frame):
        current_time = time.time()
        time_in_seconds = 0

        if time_frame == 'm':
            time_in_seconds = kline_time * 60
        elif time_frame == 'h':
            time_in_seconds = kline_time * 3600
        elif time_frame == 'd':
            time_in_seconds = kline_time * 86400

        next_interval = math.ceil(current_time / time_in_seconds) * time_in_seconds
        wait_time = next_interval - current_time
        return int(wait_time)

    def count_decimal_places(self, number):
        if isinstance(number, (int, float)):
            number_str = f'{number:.10f}'.rstrip('0')
            if '.' in number_str:
                return len(number_str.split('.')[1])
        return 0  
    
    def get_precisions(self, symbol, symbol_info):
        
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        if not symbol_data:
            return

        quantity_precision = int(float(symbol_data['quantityPrecision']))
        price_precision_market = int(float(symbol_data['pricePrecision']))
        min_notional = float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0))       

        return quantity_precision, price_precision_market, min_notional

    def usdt_to_qnt_converter(self, cur_price, quantity_precision, min_notional):
        quantity = 0
        depo = self.depo  # Используем оригинальный депозит
        if depo <= min_notional:
            depo = min_notional  # Используем минимальный нотионал если депозит меньше его
        quantity = round(depo / cur_price, quantity_precision)
        return quantity