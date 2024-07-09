import aiohttp
import asyncio
# import time
from datetime import datetime as dttm
from ws_streams import WS_STREAMS
import os
import inspect
current_file = os.path.basename(__file__)

class TEMP(WS_STREAMS):
    def __init__(self):
        super().__init__()

    async def trade_setup_template(self, session, symbol, lev_size):
        try:
            self.handle_messagee(f'Устанавливаем тип маржи для {symbol}:')
            set_margin_resp = await self.set_margin_type(session, symbol, self.margin_type)
            self.handle_messagee(str(set_margin_resp))
            
            self.handle_messagee(f'Устанавливаем кредитное плечо для {symbol}:')
            set_leverage_resp = await self.set_leverage(session, symbol, lev_size)
            self.handle_messagee(str(set_leverage_resp))
            
        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
            
    async def make_orders_template(self, session, signals_answ_list, pos_number, fitst_init):
        try:
            tasks1 = []
            tasks2 = []
            make_order_results = []
            signals_answ_list_copy = signals_answ_list.copy()
            
            # Определение размера плеча и депозита в зависимости от позиции
            lev_size = self.lev_size_1
            depo = self.depo_1

            for symbol_item in signals_answ_list_copy:
                # Обработка сигнала для открытия позиции 1, если требуется             
                # symbol_item = self.open_1_pos_signal_handler(symbol_item) 
                if fitst_init:              
                    tasks1.append(self.trade_setup_template(session, symbol_item["symbol"], lev_size))

                # Определение цены для ордера
                pricee = symbol_item[f"cur_price"]

                # Вычисление количества на основе депозита и цены
                symbol_item["quantity_precision"], _, _ , symbol_item["min_notional"] = self.get_precisions(symbol_item["symbol"], self.exchange_data)
                print(symbol_item["quantity_precision"], symbol_item["min_notional"])
                  
                symbol_item[f"qty_{pos_number}"] = self.usdt_to_qnt_converter(depo, pricee, symbol_item["quantity_precision"], symbol_item["min_notional"])
                # print(symbol_item[f"qty_1"])

                # Добавление задачи на создание ордера
                pos_averaging_true = False
                position_side = symbol_item[f"position_{pos_number}_side"]
                tasks2.append(self.make_order(session, symbol_item["symbol"], symbol_item[f"qty_{pos_number}"], symbol_item[f"side_{pos_number}"], 'MARKET', position_side, pos_averaging_true))

            if fitst_init:
                await asyncio.gather(*tasks1)
                make_order_results = await asyncio.gather(*tasks2)

            # Обработка результатов ордеров
            if make_order_results:
                signals_answ_list_copy = self.process_order_results(make_order_results, signals_answ_list_copy, pos_number)
            else:
                self.handle_messagee("make_order_results == []")

        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

        return signals_answ_list_copy
    
    def response_order_logger(self, order_answer): 
        if order_answer is not None:
            specific_key_list = ["orderId", "symbol", "positionSide", "side", "executedQty", "avgPrice"]
            order_answer_str = ""
            try:
                now_time = dttm.now(self.local_tz)
                order_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
                for k, v in order_answer.items():
                    if k in specific_key_list:
                        order_answer_str += f"{k}: {v}\n"
                order_answer_str = 'Время создания ордера:' + ' ' + order_time + '\n' + order_answer_str 
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                
            status = order_answer.get('status')
        
            if status in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
                self.handle_messagee(order_answer_str)         
                return True

        error_message = f"При попытке создания ордера возникла ошибка. Текст ответа:\n {order_answer}"
        self.handle_messagee(error_message)
                       
        return False

    def process_order_results(self, make_order_results, signals_answ_list_copy, pos_number):
        for item_res in make_order_results:
            if item_res:
                order_logger_resp = self.response_order_logger(item_res)
                if order_logger_resp:
                    signals_answ_list_copy = self.update_position_status(signals_answ_list_copy, item_res, pos_number)
        return signals_answ_list_copy

    def update_position_status(self, signals_answ_list_copy, item_res, pos_number):
        for i, symbol_item in enumerate(signals_answ_list_copy):
            if symbol_item["symbol"] == item_res["symbol"]:
                signals_answ_list_copy[i][f"in_position_{pos_number}"] = True
                signals_answ_list_copy[i]["signal"] = None
                signals_answ_list_copy[f"enter_{pos_number}_pos_price"] = item_res.get("avgPrice", None)       
                break
        return signals_answ_list_copy

class WaitCandleLogic(TEMP):
    def __init__(self):
        super().__init__()
        self.wait_candle_flag = True
        self.is_no_signal_counter = 0
        self.show_none_signal_fraction = 5
        self.wait_for_candle_or_coins = self.log_exceptions_decorator(self.wait_for_candle_or_coins)
        self.handle_wait_for_candle = self.log_exceptions_decorator(self.handle_wait_for_candle)
        self.handle_no_signal = self.log_exceptions_decorator(self.handle_no_signal)
        self.handle_signal_search_end = self.log_exceptions_decorator(self.handle_signal_search_end)
        
    async def wait_for_candle_or_coins(self, session):
        self.candidate_symbols_list = []
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
        await asyncio.sleep(1)

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
        self.main_engin = self.log_exceptions_decorator(self.main_engin)
    
    async def main_engin(self):     
        next_trading_cycle = True
        wb_task_true = False
        self.handle_messagee("Устанавливаем режим хеджирования:")
        set_hedge_mode_answ = self.set_hedge_mode(self.hedge_mode)
        self.handle_messagee(str(set_hedge_mode_answ))

        while True:                 
            if next_trading_cycle: 
                async with aiohttp.ClientSession() as session:
                    await asyncio.sleep(0.5)                     
                    await self.wait_for_candle_or_coins(session)                  
                    recent_klines_dict = {}
                    trends_dict = {}
                    tasks = [self.fetch_and_process_symbol(session, symbol, recent_klines_dict, trends_dict) for symbol in self.candidate_symbols_list]
                    await asyncio.gather(*tasks)        

                    if self.signals_data_list:
                        next_trading_cycle = False
                        wb_task_true = True
                        self.signals_data_list = self.signals_data_list[:self.diversification_number]                                       
                        [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.signals_data_list]       
                        self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, 1, True) 
                        print(self.signals_data_list)            
                    else:
                        continue

            if wb_task_true:
                wb_task_true = False
                wb_task = [self.connect_to_websocket(self.signals_data_list, recent_klines_dict, trends_dict)]
                wb_comleted_task = asyncio.gather(*wb_task)
            
            print("tik")
            await asyncio.sleep(10)   

            async with self.lock:
                if self.is_get_new_signal:
                    print("New signal detected")
                    self.is_get_new_signal = False

            if wb_comleted_task and wb_comleted_task.done():
                next_trading_cycle = wb_comleted_task.result()

# Run the main function
if __name__ == "__main__":
    asyncio.run(MAIN().main_engin())
