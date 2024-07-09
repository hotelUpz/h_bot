from SEC_SETTINGS import SEC_SETTINGSS
from HIDDEN.config import *

class VARIABLES(SEC_SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        self.symbol = None
        self.in_position_1 = False
        self.in_position_2 = False   
        self.posicion_1_side = None 
        self.posicion_2_side = None
        self.cur_price = None
        self.enter_1_pos_price = None
        self.enter_2_pos_price = None
        # self.last_enter_1_pos_price = None
        # self.last_enter_2_pos_price = None
        self.qty = None
        self.cur_klines_data = None
        self.candidate_symbols_list = []
        self.last_signal_val = None
        self.current_signal_val = None
        self.response_trading_list = []
        self.exchange_data = []
        self.signals_data_list = []
        #///////////////////////////////////////////////
        self.position_1_accounting = {
            "win/loss": None,
            "abs_profit": None,
            "per_profit": None,
            "close_mode": None,            
        }
        self.position_1_accounting = {
            "win/loss": None,
            "abs_profit": None,
            "per_profit": None,
            "close_mode": None,            
        }

        self.losses_counter = 0
        self.daily_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов
        
        self.interval = str(self.kline_time) + self.time_frame
        self.klines_limit = int((self.ema1_period + self.ema2_period)* 1.5)
        self.ema_trend_line = 240
        self.only_long_trading_default = self.only_long_trading
        self.only_short_trading_default = self.only_short_trading

        self.current_step_counter = 0 # счетчик текущего уровня усреднения позиции
        self.position_1_averaging_counter = 0 # счетчик усреднения позиции

        # ////////////////////// инициализация ключей: ///////////////////////////////
        self.api_key = BINANCE_API_PUBLIC_KEY
        self.api_secret = BINANCE_API_PRIVATE_KEY 
        # print(self.api_key)
        self.tg_api_token = TG_TOKEN
        # print(self.tg_api_token)
        self.seq_control_token = ACESS_TOKEN
        self.coinMarketCup_api_token = COIN_MARKET_CUP_TOKEN
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_socks5_port = proxy_socks5_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
