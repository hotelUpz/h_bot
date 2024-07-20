import time
import hmac
import hashlib
import requests
import aiohttp
import pandas as pd
from functools import wraps
import os
from log import Total_Logger
current_file = os.path.basename(__file__)

def aiohttp_connector(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(self, session, *args, **kwargs)
    return wrapper

class BINANCE_API(Total_Logger):
    def __init__(self):
        super().__init__()       
        self.create_order_url = self.cancel_order_url = 'https://fapi.binance.com/fapi/v1/order'
        self.change_trade_mode = 'https://fapi.binance.com/fapi/v1/positionSide/dual'
        self.exchangeInfo_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        self.klines_url = 'https://fapi.binance.com/fapi/v1/klines'
        self.set_margin_type_url = 'https://fapi.binance.com/fapi/v1/marginType'
        self.set_leverage_url = 'https://fapi.binance.com/fapi/v1/leverage'
        self.positions_url = 'https://fapi.binance.com/fapi/v2/positionRisk'
        self.all_tikers_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOrders'
        self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
        self.balance_url = 'https://fapi.binance.com/fapi/v2/balance'

        self.headers = {
            'X-MBX-APIKEY': self.api_key
        }

        self.get_exchange_info = self.log_exceptions_decorator(self.get_exchange_info)
        self.get_all_tickers = self.log_exceptions_decorator(self.get_all_tickers)
        self.get_klines = self.log_exceptions_decorator(self.get_klines)
        self.is_closing_position_true = self.log_exceptions_decorator(self.is_closing_position_true)
        self.set_hedge_mode = self.log_exceptions_decorator(self.set_hedge_mode)
        self.set_margin_type = self.log_exceptions_decorator(self.set_margin_type)
        self.set_leverage = self.log_exceptions_decorator(self.set_leverage)
        self.make_order = self.log_exceptions_decorator(self.make_order)
        self.get_close_prices = self.log_exceptions_decorator(self.get_close_prices)

    def get_signature(self, params):
        params['timestamp'] = int(time.time() * 1000)
        params_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params
    
    def get_exchange_info(self):
        params = {'recvWindow': 20000}
        response = requests.get(self.exchangeInfo_url, headers=self.headers, params=params)      
        return response.json()

    async def get_all_tickers(self, session):
        data = None
        params = {'recvWindow': 20000}
        async with session.get(self.all_tikers_url, params=params) as response:
            data = await response.json()
        return data
    
    async def get_klines(self, session, symbol, interval, limit):
        klines = None       
        params = {}
        params["symbol"] = symbol
        params['recvWindow'] = 20000
        params["interval"] = interval
        params["limit"] = limit
        params = self.get_signature(params)

        async with session.get(self.klines_url, params=params) as response:
            klines = await response.json()

        if klines:
            data = pd.DataFrame(klines).iloc[:, :6]
            data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            data = data.set_index('Time')
            data.index = pd.to_datetime(data.index, unit='ms')
            return data.astype(float)        
        return

    @aiohttp_connector
    async def get_klines_connector(self, session, symbol, interval, limit):
        return await self.get_klines(session, symbol, interval, limit)        
              
    async def is_closing_position_true(self, session, symbol, position_side):
        params = {
            "symbol": symbol,
            "positionSide": position_side,
            'recvWindow': 20000,
        }
        try:
            params = self.get_signature(params)
            async with session.get(self.positions_url, headers=self.headers, params=params) as response:
                positions = await response.json()
            for position in positions:
                if position['symbol'] == symbol and position['positionSide'] == position_side and float(position['positionAmt']) != 0:
                    return False, symbol
            return True, symbol
        except Exception as ex:
            print(ex)
        return False, symbol
        
    def set_hedge_mode(self, true_hedg):
        params = {
            'dualSidePosition': 'true' if true_hedg else 'false',            
        }
        params = self.get_signature(params)
        response = requests.post(self.change_trade_mode, headers=self.headers, params=params)
        return response.json()
    
    async def set_margin_type(self, session, symbol, margin_type):
        params = {
            'symbol': symbol,
            'margintype': margin_type,
            'recvWindow': 20000,
            'newClientOrderId': 'CHANGE_MARGIN_TYPE'
        }
        params = self.get_signature(params)
        async with session.post(self.set_margin_type_url, headers=self.headers, params=params) as response:
            data = await response.json()
        return data

    async def set_leverage(self, session, symbol, lev_size):
        params = {
            'symbol': symbol,
            'recvWindow': 20000,
            'leverage': lev_size
        }
        params = self.get_signature(params)
        async with session.post(self.set_leverage_url, headers=self.headers, params=params) as response:
            data = await response.json()
        return data        

    async def make_order(self, session, symbol, qty, side, market_type, position_side, target_price=None):
  
        params = {
            "symbol": symbol,
            "side": side,
            "type": market_type,
            "quantity": qty,
            "positionSide": position_side,
            "recvWindow": 20000,
            "newOrderRespType": 'RESULT'
        }
        
        if market_type in ['STOP_MARKET', 'TAKE_PROFIT_MARKET']:
            params['stopPrice'] = target_price
            params['closePosition'] = True
        elif market_type == 'LIMIT':
            params["price"] = target_price
            params["timeInForce"] = 'GTC'

        params = self.get_signature(params)
        async with session.post(self.create_order_url, headers=self.headers, params=params) as response:
            data = await response.json()
        return data