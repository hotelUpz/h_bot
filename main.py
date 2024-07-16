import asyncio
from templates import TEMP
from api_binance import aiohttp_connector
import os
import inspect
current_file = os.path.basename(__file__)

class WaitCandleLogic(TEMP):
    def __init__(self):
        super().__init__()
        self.handle_wait_for_candle = self.log_exceptions_decorator(self.handle_wait_for_candle)
        self.handle_no_signal = self.log_exceptions_decorator(self.handle_no_signal)
        self.handle_signal_search_end = self.log_exceptions_decorator(self.handle_signal_search_end)
        
    async def wait_for_candle_or_coins(self, session):
        if self.wait_candle_flag:
            self.wait_candle_flag = False
            wait_time = self.handle_wait_for_candle()
            if self.automatic_coin_search_mode:
                self.exchange_data = self.get_exchange_info()
                self.candidate_symbols_list = await self.get_top_coins_template(session)
            else:
                self.candidate_symbols_list = self.custom_symbol_list

            self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]

        else:
            wait_time = self.time_calibrator(1, 'm')
        print(f"wait_time: {wait_time} sec")
        await asyncio.sleep(wait_time)

    def handle_wait_for_candle(self):
        self.wait_candle_flag = False
        wait_time = self.time_calibrator(self.kline_time, self.time_frame)
        msg = f"Ждем закрытия последней {self.interval} свечи. Осталось {round(wait_time / 60, 2)} минут"
        self.handle_messagee(msg)
        return wait_time

    def handle_no_signal(self):
        self.handle_messagee("Нет сигнала")
        self.is_no_signal_counter += 1
        if self.is_no_signal_counter % self.show_none_signal_fraction == 0:
            msg = f"Нет сигнала на протяжение {self.is_no_signal_counter} минут"
            self.handle_messagee(msg)

    def handle_signal_search_end(self, delta_time, signals_answ_list):
        self.handle_messagee(f"Поиск сигнала занял {delta_time} сек. Найдено {len(signals_answ_list)} сигнала(-ов)")

class MAIN(WaitCandleLogic):
    def __init__(self) -> None:
        super().__init__()
        self.hedge_or_close_analizator = self.log_exceptions_decorator(self.hedge_or_close_analizator)
        self.main_engin = self.log_exceptions_decorator(self.main_engin)
        self.execute_trading_cycle = self.log_exceptions_decorator(self.execute_trading_cycle)

    async def close_pos_viewer(self):
        self.check_finish_tik_counter += 1
        
        if self.check_finish_tik_counter == 10 or self.check_finish_flag:
            # print("self.check_finish_tik_counter == 10 or self.check_finish_flag")
            self.check_finish_flag = False
            self.check_finish_tik_counter = 0
            
            async with self.lock:
                self.next_trading_cycle = await self.is_finish_trade_cycle_true()
            
            if self.next_trading_cycle:
                self.next_trading_cycle_event.set()
                
                try:
                    await asyncio.wait_for(self.wb_completed_task, timeout=13)  # Устанавливаем таймаут на ожидание
                    print("Вебсокет соединение закрыто")
                except asyncio.TimeoutError:
                    print("Не удается закрыть вебсокет в течение заданного времени")
                
                # self.next_trading_cycle_event.clear()  # Сбрасываем событие
                self.init_and_reset_data()  # Инициализируем и сбрасываем данные
                print("конец первой торговой итерации")
                return True 
        return False   

    async def hedge_or_close_analizator(self):
        is_any_close_pos = False
        is_any_opening = False

        for i, symbol_item in enumerate(self.trading_data_list):
            result = self.handle_positions_rules(symbol_item)
            if result:
                for action, pos_num in result:
                    if action == "closing":
                        is_any_close_pos = True
                        self.trading_data_list[i][f"is_closing_{pos_num}_pos"] = True
                    elif action == "opening":
                        is_any_opening = True
                        self.trading_data_list[i][f"is_opening_{pos_num}_pos"] = True

        if is_any_close_pos or is_any_opening:
            await self.make_orders_total_template()           
            return True
        return False
    
    async def is_some_triger_viewer(self):
        self.strategy_engin_tik_counter += 1
        if self.strategy_engin_tik_counter == 2 or self.is_get_new_signal:
            self.strategy_engin_tik_counter = 0
            async with self.lock:                    
                self.is_get_new_signal = False
                self.check_finish_flag = await self.hedge_or_close_analizator()

    @aiohttp_connector
    async def execute_trading_cycle(self, session):     
        await self.wait_for_candle_or_coins(session)
        tasks = [self.fetch_and_process_symbol(session, symbol, self.recent_klines_dict) for symbol in self.candidate_symbols_list]
        await asyncio.gather(*tasks)

        if self.trading_data_list:
            self.trading_data_list = self.trading_data_list[:self.diversification_number]
            [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.trading_data_list]
            await self.make_orders_total_template()
            if any(symbol_item.get("in_position_1") for symbol_item in self.trading_data_list):
                self.trading_data_list = [x for x in self.trading_data_list if x.get("in_position_1")]
                return True
        return False

    async def main_engin(self):
        self.handle_messagee("Устанавливаем режим хеджирования:")
        set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
        self.handle_messagee(str(set_hedge_mode_answ))

        while True:
            if self.next_trading_cycle:
                await asyncio.sleep(0.5)
                if not await self.execute_trading_cycle():
                    print("Продолжаем искать сигналы...")
                    continue
                self.next_trading_cycle = False
                self.wb_task_true = True
                print(self.trading_data_list)

            if self.wb_task_true:
                self.wb_task_true = False
                symbols = [x.get("symbol") for x in self.trading_data_list]
                self.wb_task = [self.connect_to_websocket(symbols, self.recent_klines_dict)]
                self.wb_completed_task = asyncio.gather(*self.wb_task)
            
            # print("tik")
            await asyncio.sleep(1)
            if await self.close_pos_viewer():
                continue

            await self.is_some_triger_viewer()

if __name__ == "__main__":
    asyncio.run(MAIN().main_engin())