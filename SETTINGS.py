import math

class SETTINGSS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # /////////////// БАЗОВЫЕ ТОРГОВЫЕ ПАРАМЕТРЫ:
        self.depo_1 = 6 # депозит в USDT для первой позиции
        self.depo_2 = 6 # депозит в USDT для второй позиции
        self.lev_size_1 = 2 # размер кредитного плеча для первой позиции
        self.lev_size_2 = 2 # размер кредитного плеча для второй позиции
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)
        self.hedge_mode = True # флаг режима хеджирования. False -- моно
        self.automatic_coin_search_mode = True # искать монеты автоматически/ввести в ручную -- True/False
        self.custom_symbol_list = ["DOGEUSDT"] # кастомный список монет для торговли. Для self.automatic_coin_search_mode = False
        self.diversification_number = 2 # количество торговых пар торгующихся одновременно

        # //////////////////////////// НАСТРОЙКИ ФИЛЬТРА МОНЕТ:
        self.default_black_coins_list = self.black_coins_list = ['USDCUSDT','FDUSDUSDT','BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'LTCUSDT'] # монеты исключения
        self.price_filter_flag = 0 # фильтр по цене. Сейчас отключен. Включить/выкл: - 1/0
        self.MIN_FILTER_PRICE = 0 # минимальный порог цены. Можете указать свое значение.
        self.MAX_FILTER_PRICE = math.inf # максимальный порог цены. Можете указать свое значение.
        
        self.daily_filter_direction = 0 # 1 -- искать только которые показывают растущую динамику (зеленые графики). -1 --- для падающих (красные графики) на бинанс. 0 -- и то и другое
        
        self.slice_volum_flag = True # флаг фильтра по объему. Включить/выкл: - 1/0
        self.slice_price_change_flag = True # находить самые волатильные на бинанс. Включить/выкл: - 1/0
        self.SLICE_VOLATILITY = 200 # срез волатильности. То есть первые 40 самых волатильных
        self.min_volume_usdtFilter_flag = False # искать по минимальному объему торгов за сутки на бинанс. Включить/выкл: - 1/0
        self.MIN_VOLUM_USDT = 10000000 # размер минимального обьема в usdt. При активном флаге self.min_volume_usdtFilter_flag = 1
        self.SLICE_VOLUME_BINANCE_PAIRS = 200 # срез монет по объему торгов на бинанс То есть первые 60 самых проторгованных
        self.volume_range_true = True # ранжировать по объему. Включить/выкл: - 1/0
        self.changing_price_range_true = False # ранжировать по волатильности. Включить/выкл: - 1/0
        self.in_coinMarketCup_is = True # показывать только те монеты которые есть в топе Coin Market Cup. Включить/выкл: - 1/0
        self.TOP_MARKET_CUP = 100 # срез монет. по коин маркет кап это будет первая тридцатка
        
        # //////////////////////////// НАСТРОЙКИ ИНДИКАТОРА:
        self.atr_period = 14
        self.is_reverse_signal = 1 # Вкл/Выкл: -1/1 # использовать обратный сигнал. Если шорт то лонг и наоборот. Чтобы активировать введите значение -1 (минус один)

        self.only_long_trading = False # Вкл/Выкл: True/False -- торговать только лонговые позиции. Можно пробовать под бычью фазу рынка
        self.only_short_trading = False # Вкл/Выкл: True/False -- торговать только шортовые позиции. Можно пробовать под медвежью фазу рынка
        self.defend_total_market_trend_flag = False # определять тренд рынка автоматически
        self.only_stop_loss_flag = False # торговать только со стопами
        self.only_take_profit_flag = False # торговать только с тейк профитом
        self.closing_by_ema_crossover_flag = True # True/False Закрывать позицию по сигналу ema crossover/нет

        self.position_1_averaging_counter_limit = 3 # до скольки раз усреднять позицию
        self.averaging_step_rate = 1 # % -- размер шага для усреднения в процентах
        self.min_deviation_rate_for_1_position_closing = 0.4 # минимальный зазор для закрыти первой позиции по сигналу
        self.sl_1_pos_rate, self.tp_1_pos_rate = 0.4, 0.3 # % -- стоп лосс и тейк профит для 1 позиции в процентах
        # self.sl_1_pos_rate, self.tp_1_pos_rate = self.averaging_step_rate* (self.position_1_averaging_counter_limit + 1), 2 # % -- стоп лосс и тейк профит для 1 позиции в процентах
        self.comulative_sl_rate, self.comulative_tp_rate = 2, 4 # % -- стоп лосс и тейк профит для обоих позициий в процентах

        self.ema1_period = 5 # - длина короткой волны
        self.ema2_period = 20 # - длина длинной волны

        # //////////////////// ТАЙМ ФРЕЙМ:
        self.kline_time, self.time_frame = 1, 'm' # таймфрейм где челое число - период, а буква - сам тайм фрейм (минута, час и т.д (m, h))

        # //////////////////////////// НАСТРОЙКИ СТОП ЛОСС И ТЕЙК ПРОФИТА:

        self.risk_reward_ratio = '1:1'  # соотношение риска к прибыли.
        # //////// способы вычисления точки стоп лосса: /////////////////

        self.stop_loss_ratio_mode = 1 # Метод для расчета коэффициента стоп-лосса. 
        # '1': 'static', -- статический процент. Рекомендуется для self.stop_loss_global_type = 1 ('TRAILLING_CUSTOM')
        # '2': 'volatility_period_20', -- по волатильности последних 20 свечей
        # '3': 'last_volatility', -- по волатильности последней свечи
        # '4': 'last_candle_length', --- по длине последней свечи
        # '5': 'last_candle_length/2', --- по длине последней свечи/ 2 - почти то же что и '3': 'last_volatility'
        # '6': 'last_minimum', -- предпоследний минимум или максимум - в зависимости от направленности сигнала
        # '7': 'absolute_minimum', наибольший минимум или максимум последних 20 свечей - в зависимости от направленности сигнала
        
        self.stop_loss_ratio = None # в % Множитель стоп лосса. Для self.stop_loss_ratio_mode 2 - 8  -- расчитывается динамически -- этот параметр НЕ ТРОГАТЬ!! Он приведен для информации!
        self.static_stop_loss_ratio_val = 1 # в % Множитель стоп лосса. Только для статического стоп лосс коэффициента -- self.stop_loss_ratio_mode = 1
        self.min_default_ratio = 0.5 # в %. self.stop_loss_ratio сбрасывается к этому значению если расчетное значение self.stop_loss_ratio НИЖЕ этого порога
        self.max_default_ratio = 3.0 # в % self.stop_loss_ratio сбрасывается к этому значению если расчетное значение self.stop_loss_ratio ВЫШЕ этого порога

        # /////////// ЗАЩИТНЫЕ МЕХАНИЗМЫ:
        self.losses_protection = True # Вкл/Выкл: True/False. Стратегия защиты от потерь. Если включена то устанавливается лимит неудачных сделок. После серии таких сделок, робот отключается. Значение (количество потерь) задается ниже
        self.losses_until_value = 2 # количество неудачных сделок после которого робот выключится

        self.is_proxies_true = False # Вкл/Выкл: True/False Использовать прокси/не использовать