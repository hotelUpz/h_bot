import asyncio
from SEC_SETTINGS import SEC_SETTINGSS
from HIDDEN.config import *

class VARIABLES(SEC_SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        # ////////////////////// инициализация ключей: ///////////////////////////////
        self.api_key = BINANCE_API_PUBLIC_KEY
        self.api_secret = BINANCE_API_PRIVATE_KEY 
        # print(self.api_key)
        self.coinMarketCup_api_token = COIN_MARKET_CUP_TOKEN
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_socks5_port = proxy_socks5_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        # ///////////////////////////////////////
        self.init_and_reset_data()

    def init_and_reset_data(self):
        self.candidate_symbols_list = []
        self.exchange_data = []
        self.trading_data_init_list = []
        self.trading_data_list = []
        self.next_trading_cycle = True
        self.interval = str(self.kline_time) + self.time_frame   
        self.only_long_trading_default = self.only_long_trading
        self.only_short_trading_default = self.only_short_trading
        self.wait_candle_flag = True
        self.is_no_signal_counter = 0
        self.show_none_signal_fraction = 5
        self.is_get_new_signal = False
        self.wb_task_true = False
        self.wb_task = []
        self.wb_completed_task = None
        self.recent_klines_dict = {}
        self.check_finish_flag = False
        self.check_finish_tik_counter = 0
        self.strategy_engin_tik_counter = 0
        self.minute_counter = 0
        self.any_moving = False
        self.lock = asyncio.Lock()
        self.next_trading_cycle_event = asyncio.Event()