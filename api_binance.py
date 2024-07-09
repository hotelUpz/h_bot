import time
import hmac
import hashlib
import requests
import numpy as np
import os
import inspect
from log import Total_Logger
current_file = os.path.basename(__file__)  

class BINANCE_API(Total_Logger):
    def __init__(self):
        super().__init__()       
        # BASE_URL = "https://fapi.binance.com"   
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
        
        if self.is_proxies_true:
            self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
            self.proxies = {
                'http': self.proxy_url,
                'https': self.proxy_url
            }
        else:
            self.proxies = None

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

        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        async with session.get(self.klines_url, params=params) as response:
            data = await response.json()
            return np.array([[
                float(entry[0]),  # Open time
                float(entry[1]),  # Open
                float(entry[2]),  # High
                float(entry[3]),  # Low
                float(entry[4]),  # Close
                float(entry[5])  # Volume
            ] for entry in data])
        
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

    async def make_order(self, session, symbol, qty, side, market_type, position_side, pos_averaging_true, target_price=None):
  
        params = {
            "symbol": symbol,
            "side": side,
            "type": market_type,
            "quantity": qty,
            "positionSide": position_side,
            "recvWindow": 20000,
            "newOrderRespType": 'RESULT'
        }
        if pos_averaging_true:
            params['reduceOnly'] = 'true'
        
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

# class BINANCE_API(Total_Logger):
#     def __init__(self):
#         super().__init__()
#         self.market_place = 'binance'
#         self.market_type = 'futures'
        
#         # URLs for Binance API
#         self.create_order_url = self.cancel_order_url = 'https://fapi.binance.com/fapi/v1/order'
#         self.change_trade_mode = 'https://fapi.binance.com/fapi/v1/positionSide/dual'
#         self.exchangeInfo_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
#         self.klines_url = 'https://fapi.binance.com/fapi/v1/klines'
#         self.set_margin_type_url = 'https://fapi.binance.com/fapi/v1/marginType'
#         self.set_leverage_url = 'https://fapi.binance.com/fapi/v1/leverage'
#         self.positions_url = 'https://fapi.binance.com/fapi/v2/positionRisk'
#         self.all_tikers_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
#         self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOrders'
#         self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
#         self.balance_url = 'https://fapi.binance.com/fapi/v2/balance'

#         self.session = None
        
#         self.headers = {
#             'X-MBX-APIKEY': self.api_key
#         }
        
#         if self.is_proxies_true:
#             self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
#             self.proxies = {
#                 'http': self.proxy_url,
#                 'https': self.proxy_url
#             }
#         else:
#             self.proxies = None

#     def get_signature(self, params):
#         params['timestamp'] = int(time.time() * 1000)
#         params_str = '&'.join([f'{k}={v}' for k, v in params.items()])
#         signature = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256).hexdigest()
#         params['signature'] = signature
#         return params

#     async def http_request(self, url, method='GET', params=None, data=None):
#         async with aiohttp.ClientSession(headers=self.headers) as session:
#             async with session.request(method=method, url=url, params=params, json=data, proxy=self.proxy_url if self.proxies else None) as response:
#                 return await response.json()

#     async def get_exchange_info(self):
#         params = {'recvWindow': 20000}
#         return await self.http_request(self.exchangeInfo_url, method='GET', params=params)

#     async def get_all_tickers(self):
#         params = {'recvWindow': 20000}
#         return await self.http_request(self.all_tikers_url, method='GET', params=params)

#     async def get_total_balance(self, ticker):
#         params = {'recvWindow': 20000}
#         params = self.get_signature(params)
#         current_balance = await self.http_request(self.balance_url, method='GET', params=params)
#         return float([x['balance'] for x in current_balance if x['asset'] == ticker][0])

#     async def get_all_orders(self, symbol):
#         params = {'symbol': symbol, 'recvWindow': 20000}
#         params = self.get_signature(params)
#         return await self.http_request(self.get_all_orders_url, method='GET', params=params)

#     async def get_klines(self, symbol, interval, limit):
#         params = {'symbol': symbol, 'interval': interval, 'limit': limit}
#         data = await self.http_request(self.klines_url, method='GET', params=params)
#         klines = [
#             [float(entry[0]), float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4]), float(entry[5])]
#             for entry in data
#         ]
#         return (symbol, np.array(klines))

#     async def fetch_all_klines(self, symbols, interval, limit):
#         tasks = [self.get_klines(symbol, interval, limit) for symbol in symbols]
#         results = await asyncio.gather(*tasks)
#         return results

#     async def is_closing_position_true(self, symbol, position_side):
#         params = {
#             "symbol": symbol,
#             "positionSide": position_side,
#             'recvWindow': 20000,            
#         }
#         params = self.get_signature(params)
#         positions = await self.http_request(self.positions_url, method='GET', params=params)
#         for position in positions:
#             if position['symbol'] == symbol and position['positionSide'] == position_side and float(position['positionAmt']) != 0:
#                 return None
#         return True
    
#     # ///////////////////// post api:
#     async def set_hedge_mode(self, true_hedg):
#         params = {
#             'dualSidePosition': 'true' if true_hedg else 'false',            
#         }
#         params = self.get_signature(params)
#         return await self.http_request(self.change_trade_mode, method='POST', params=params)
    
#     async def set_margin_type(self, symbol, margin_type):
#         params = {
#             'symbol': symbol,
#             'margintype': margin_type,
#             'recvWindow': 20000,
#             'newClientOrderId': 'CHANGE_MARGIN_TYPE'
#         }
#         params = self.get_signature(params)
#         return await self.http_request(self.set_margin_type_url, method='POST', params=params)

#     async def set_leverage(self, symbol, lev_size):
#         params = {
#             'symbol': symbol,
#             'recvWindow': 20000,
#             'leverage': lev_size
#         }
#         params = self.get_signature(params)
#         return await self.http_request(self.set_leverage_url, method='POST', params=params)

#     async def make_order(self, symbol, qty, side, market_type, position_side, pos_averaging_true, target_price=None):
  
#         params = {
#             "symbol": symbol,
#             "side": side,
#             "type": market_type,
#             "quantity": qty,
#             "positionSide": position_side,
#             "recvWindow": 20000,
#             "newOrderRespType": 'RESULT'
#         }
#         if pos_averaging_true:
#             params['reduceOnly'] = 'true'
        
#         if market_type in ['STOP_MARKET', 'TAKE_PROFIT_MARKET']:
#             params['stopPrice'] = target_price
#             params['closePosition'] = True
#         elif market_type == 'LIMIT':
#             params["price"] = target_price
#             params["timeInForce"] = 'GTC'

#         params = self.get_signature(params)
#         return await self.http_request(self.create_order_url, method='POST', params=params)
