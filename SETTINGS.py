class SETTINGSS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # /////////////// БАЗОВЫЕ ТОРГОВЫЕ ПАРАМЕТРЫ:
        self.depo = 6 # депозит в USDT
        self.lev_size = 2 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)
        self.hedge_mode = True # флаг режима хеджирования. False -- моно
        self.automatic_coin_search_mode = True # искать монеты автоматически/ввести в ручную -- True/False
        self.custom_symbol_list = ["DOGEUSDT"] # кастомный список монет для торговли. Для self.automatic_coin_search_mode = False
        self.diversification_number = 1 # количество торговых пар торгующихся одновременно

        # //////////////////////////// НАСТРОЙКИ ИНДИКАТОРА:
        self.ema_calculating_mode = 1 # способ расчета EMA. 1 -- talib, 2 -- manual
        self.ema_weighting_rate = 2.0 # скорость затухания весовых коэффициентов EMA, влияющая на чувствительность сигналов. Обычно используют = 2 ... как вариант: 2.71, 2.1... актуально только для self.ema_calculating_mode = 2
        self.ema1_period = 5 # - длина короткой волны
        self.ema2_period = 10 # - длина длинной волны
        self.is_reverse_signal = 1 # Вкл/Выкл: -1/1 # использовать обратный сигнал. Если шорт то лонг и наоборот. Чтобы активировать введите значение -1 (минус один). Актуально только для первого входа в позицию
        self.only_long_trading = False # Вкл/Выкл: True/False -- торговать только лонговые позиции. Можно пробовать под бычью фазу рынка
        self.only_short_trading = False # Вкл/Выкл: True/False -- торговать только шортовые позиции. Можно пробовать под медвежью фазу рынка
        self.defend_total_market_trend_flag = False # определять тренд рынка автоматически (бычий или медвежий)
        self.only_stop_loss_flag = False # торговать только со стопами
        self.only_take_profit_flag = True # торговать только с тейк профитом
        self.price_triger_than_both_pos_opened_true = True # когда позиция захеджирована, рассматривать закрытие одной из позиций при помощи тригера цены. False -- отключено
        self.strong_opposite_signal_flag = True # использовать для закрытия позиции только сигналы противоположной направленности  

        # //////////////////// ТАЙМ ФРЕЙМ:
        self.kline_time, self.time_frame = 5, 'm' # таймфрейм, где: челое число - период, буква - единица времени(минута, час и т.д (m, h))

        # //////////////////////////// НАСТРОЙКИ СТОП ЛОСС И ТЕЙК ПРОФИТА:
        self.min_deviation_rate = 0.51 # минимальный зазор для закрыти первой позиции по сигналу
        self.sl_1_pos_rate, self.tp_1_pos_rate = 4, 2 # % -- стоп лосс и тейк профит для 1 позиции в процентах
        self.risk_reward_ratio = '1:1'  # соотношение риска к прибыли sl/tp для первой позиции.
        # /////////////////////////////////// ДРУГОЕ:
        self.minute_counter_limit = 120 # если в течение указанного времени (в минутах) не происходит никакого движения, то все открытые позиции закрываются, сессия переходит на следующую итерацию. Отключить -- None