# import talib
import numpy as np
from random import choice
from datetime import datetime as dttm
from api_binance import BINANCE_API, aiohttp_connector
import math
from typing import List, Tuple
import os
import inspect
current_file = os.path.basename(__file__)

class INDICATORS_STRATEGYY(BINANCE_API):
    def __init__(self) -> None:
        super().__init__()  
        # устанавливаем функциии декораторы
        self.find_last_ema_cross = self.log_exceptions_decorator(self.find_last_ema_cross)

    def calculate_ema_(self, close_prices, period):
        ema = np.zeros_like(close_prices)
        alpha = 2 / (period + 1)
        ema[0] = close_prices[0]  # Use the first value as the starting EMA value
        for i in range(1, len(close_prices)):
            ema[i] = alpha * close_prices[i] + (1 - alpha) * ema[i-1]
        return ema

    async def find_last_ema_cross(self, prices):
        # await asyncio.sleep(0.05)
        # ema_short = talib.EMA(prices, timeperiod=self.ema1_period)
        # ema_long = talib.EMA(prices, timeperiod=self.ema2_period)

        ema_short = self.calculate_ema_(prices, self.ema1_period)
        ema_long = self.calculate_ema_(prices, self.ema2_period)

        # Проверяем последние два значения EMA
        current_short_ema = ema_short[-1]
        current_long_ema = ema_long[-1]
        previous_short_ema = ema_short[-2]
        previous_long_ema = ema_long[-2]

        # Проверяем пересечение вверх
        if previous_short_ema < previous_long_ema and current_short_ema > current_long_ema:
            return 1  # Signal for buy

        # Проверяем пересечение вниз
        if previous_short_ema > previous_long_ema and current_short_ema < current_long_ema:
            return -1  # Signal for sell

        return 0  # No cross    
    
    def time_signal_info(self, signal, symbol, cur_price):
        now_time = dttm.now(self.local_tz)
        ssignal_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
        signal_mess = 'LONG' if signal == 1 else 'SHORT'
        self.handle_messagee(f"Сигнал: {signal_mess}. Монета: {symbol}. Время сигнала: {ssignal_time}. Текущая цена: {cur_price}")

class COInN_FILTERR(INDICATORS_STRATEGYY):
    def __init__(self) -> None:
        super().__init__()
        # Set decorators for functions
        self.top_coins_engin = self.log_exceptions_decorator(self.top_coins_engin)
        self.coin_market_cup_top = self.log_exceptions_decorator(self.coin_market_cup_top)
        self.go_filter = self.log_exceptions_decorator(self.go_filter)
        self.get_top_coins_template = self.log_exceptions_decorator(self.get_top_coins_template)

    @aiohttp_connector
    async def top_coins_engin(self, session, limit: int) -> List[dict]:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.coinMarketCup_api_token,
        }
        params = {
            'start': '1',
            'limit': limit,
            'convert': 'USD',
        }

        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('data', [])
            return []

    async def coin_market_cup_top(self, limit: int) -> List[str]:
        top_coins_total_list = []
        top_coins = await self.top_coins_engin(limit)
        
        if top_coins:
            for coin in top_coins:
                symbol = coin.get('symbol', '')
                if symbol:
                    top_coins_total_list.append(f"{symbol}USDT")
            return top_coins_total_list
        return []

    async def go_filter(self, all_binance_tickers: List[dict], coinsMarket_tickers: List[str]) -> Tuple[List[str], List[str], List[str], List[str]]:
        top_pairs_total: List[dict] = []
        top_pairs_by_volum: List[dict] = []
        top_pairs_by_positive_price: List[dict] = []
        top_pairs_by_negative_price: List[dict] = []

        exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR'] + self.default_black_coins_list

        # Filter conditions
        if not self.price_filter_flag:
            self.MIN_FILTER_PRICE = 0
            self.MAX_FILTER_PRICE = math.inf

        def is_valid_ticker(ticker: dict) -> bool:
            symbol = ticker['symbol'].upper()
            last_price = float(ticker['lastPrice'])
            
            common_conditions = (
                symbol.endswith('USDT') and
                all(exclusion not in symbol for exclusion in exclusion_contains_list) and
                self.MIN_FILTER_PRICE <= last_price <= self.MAX_FILTER_PRICE
            )
            
            if self.in_coinMarketCup_is:
                return common_conditions and symbol in coinsMarket_tickers
            else:
                return common_conditions

        top_pairs_total = [
            ticker for ticker in all_binance_tickers
            if is_valid_ticker(ticker)
        ]

        # Additional filters
        if self.slice_volum_flag:
            top_pairs_by_volum = sorted(top_pairs_total, key=lambda x: float(x['quoteVolume']), reverse=True)[:self.SLICE_VOLUME_BINANCE_PAIRS]

        if self.min_volume_usdtFilter_flag:
            top_pairs_total = [x for x in top_pairs_total if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

        if self.slice_price_change_flag:
            top_pairs_total = sorted(top_pairs_total, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)[:self.SLICE_VOLATILITY]

        top_pairs_by_positive_price = [x for x in top_pairs_total if float(x['priceChange']) > 0]
        top_pairs_by_negative_price = [x for x in top_pairs_total if float(x['priceChange']) < 0]

        if self.daily_filter_direction == 1 and not self.defend_total_market_trend_flag:
            top_pairs_total = top_pairs_by_positive_price
        elif self.daily_filter_direction == -1 and not self.defend_total_market_trend_flag:
            top_pairs_total = top_pairs_by_negative_price
        else:
            top_pairs_total = top_pairs_by_positive_price + top_pairs_by_negative_price

        if self.volume_range_true:
            top_pairs_total = sorted(top_pairs_total, key=lambda x: float(x['quoteVolume']), reverse=True)

        if self.changing_price_range_true:
            top_pairs_total = sorted(top_pairs_total, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)

        top_pairs_total = [x['symbol'] for x in top_pairs_total]
        top_pairs_by_volum = [x['symbol'] for x in top_pairs_by_volum]
        top_pairs_by_positive_price = [x['symbol'] for x in top_pairs_by_positive_price]
        top_pairs_by_negative_price = [x['symbol'] for x in top_pairs_by_negative_price]

        return top_pairs_total, top_pairs_by_volum, top_pairs_by_positive_price, top_pairs_by_negative_price
    
    async def get_top_coins_template(self, session):
        self.handle_messagee("Ищем монеты по фильтру...")
        # Получение всех тикеров и тикеров с CoinMarketCap, если требуется
        all_binance_tickers = await self.get_all_tickers(session)
        # print(all_binance_tickers)    
        coinsMarket_tickers = await self.coin_market_cup_top(self.TOP_MARKET_CUP) if self.in_coinMarketCup_is else []

        # Фильтрация тикеров
        total_coin_list, _, coin_list_by_positive_price, coin_list_by_negative_price = await self.go_filter(all_binance_tickers, coinsMarket_tickers)
        
        # Обработка флага рыночного тренда
        pos_len = len(coin_list_by_positive_price)
        neg_len = len(coin_list_by_negative_price)
        
        if pos_len == 0 and neg_len == 0:
            self.only_long_trading = False
            self.only_short_trading = False
        elif pos_len == 0 and neg_len != 0:
            self.only_long_trading = False
            self.only_short_trading = True
        elif neg_len == 0 and pos_len != 0:
            self.only_long_trading = True
            self.only_short_trading = False
        else:
            ratio = pos_len / neg_len
            if ratio >= 2:
                self.only_long_trading = True
                self.only_short_trading = False
            elif ratio <= 0.5:
                self.only_long_trading = False
                self.only_short_trading = True
            else:
                self.only_long_trading = False
                self.only_short_trading = False
        if not self.defend_total_market_trend_flag:
            self.only_long_trading = self.only_long_trading_default
            self.only_short_trading = self.only_short_trading_default

        try:
            print(f"Кол-во Растущих | Падающих: {pos_len} | {neg_len}")
            print(f"Отношение Растущих / Падающих: {pos_len / neg_len}")
        except ZeroDivisionError:
            pass
        
        print(f"self.only_long_trading: {self.only_long_trading}")
        print(f"self.only_short_trading: {self.only_short_trading}")

        return total_coin_list 