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

    async def handle_close_signals(self, close_func):        
        is_any_close_pos = False
        for i, symbol_item in enumerate(self.signals_data_list):
            is_any_close_pos = self.signals_data_list[i]["is_close_pos_humanly"] = close_func(symbol_item)
        if is_any_close_pos:
            async with aiohttp.ClientSession() as session:
                is_any_close_pos = False
                pos_number = 1
                is_first_init = False             
                self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, pos_number, is_first_init)

    async def hadge_engin_1(self):
        if self.is_get_new_signal:
            self.is_get_new_signal = False
            await self.handle_close_signals(self.is_close_1_pos_by_signal)
        await self.handle_close_signals(self.close_1_pos_by_price)

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
    
    def orders_logger_hundler(self, order_answer): 
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
            
    async def make_orders_template(self, session, signals_answ_list, pos_number, fitst_init):
        try:
            tasks1 = []
            tasks2 = []
            make_order_results = []
            signals_answ_list_copy = signals_answ_list.copy()
            
            # Определение размера плеча и депозита в зависимости от позиции
            lev_size = self.lev_size_1 if pos_number == 1 else self.lev_size_2
            depo = self.depo_1 if pos_number == 1 else self.depo_2

            for symbol_item in signals_answ_list_copy:
                if fitst_init:              
                    tasks1.append(self.trade_setup_template(session, symbol_item["symbol"], lev_size))

                    # Определение цены для ордера
                    pricee = symbol_item[f"cur_price"]

                    # Вычисление количества на основе депозита и цены
                    symbol_item["quantity_precision"], _, _ , symbol_item["min_notional"] = self.get_precisions(symbol_item["symbol"], self.exchange_data)
                    print(symbol_item["quantity_precision"], symbol_item["min_notional"])
                    
                    symbol_item["qty_1"] = symbol_item["qty_2"] = self.usdt_to_qnt_converter(depo, pricee, symbol_item["quantity_precision"], symbol_item["min_notional"])
                    # print(symbol_item[f"qty_1"])
                    is_close_pos = False
                    pos_averaging_true = False
                else:
                    is_close_pos = symbol_item.get("is_close_pos_humanly")
                    pos_averaging_true = symbol_item.get("pos_averaging_true")
                
                position_side = symbol_item[f"position_{pos_number}_side"]
                if is_close_pos:
                    if position_side == "LONG":
                        side = "SELL"
                    elif position_side == "SHORT":
                        side = "BUY"
                else:
                    if position_side == "LONG":
                        side = "BUY"
                    elif position_side == "SHORT":
                        side = "SELL"

                # Добавление задачи на создание ордера
                tasks2.append(self.make_order(session, symbol_item["symbol"], symbol_item[f"qty_{pos_number}"], side, 'MARKET', position_side, pos_averaging_true))

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

    def process_order_results(self, make_order_results, signals_answ_list_copy, pos_number):
        for item_res in make_order_results:
            if item_res:
                order_logger_resp = self.orders_logger_hundler(item_res)
                if order_logger_resp:
                    signals_answ_list_copy = self.update_position_status(signals_answ_list_copy, item_res, pos_number)
        return signals_answ_list_copy

    def update_position_status(self, signals_answ_list_copy, item_res, pos_number):
        for i, symbol_item in enumerate(signals_answ_list_copy):
            if symbol_item["symbol"] == item_res["symbol"]:
                is_close = symbol_item.get("is_close_pos_humanly")
                signals_answ_list_copy[i][f"in_position_{pos_number}"] = not is_close
                signals_answ_list_copy[i][f"is_closed_{pos_number}"] = is_close                
                signals_answ_list_copy[i][f"enter_{pos_number}_pos_price"] = item_res.get("avgPrice", None)
                signals_answ_list_copy[i]["signal"] = None      
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
                    tasks = [self.fetch_and_process_symbol(session, symbol, recent_klines_dict) for symbol in self.candidate_symbols_list]
                    await asyncio.gather(*tasks)        

                    if self.signals_data_list:
                        next_trading_cycle = False
                        wb_task_true = True
                        self.signals_data_list = self.signals_data_list[:self.diversification_number]                                       
                        [self.time_signal_info(item["signal"], item["symbol"], item["cur_price"]) for item in self.signals_data_list]
                        pos_number = 1
                        is_first_init = True       
                        self.signals_data_list = await self.make_orders_template(session, self.signals_data_list, pos_number, is_first_init)
                        print(self.signals_data_list)            
                    else:
                        continue

            if wb_task_true:
                wb_task_true = False
                symbols = [x.get("symbol") for x in self.signals_data_list]
                wb_task = [self.connect_to_websocket(symbols, recent_klines_dict)]
                wb_comleted_task = asyncio.gather(*wb_task)
            
            print("tik")
            await asyncio.sleep(10)   

            async with self.lock:                
                await self.hadge_engin_1()

            if wb_comleted_task and wb_comleted_task.done():
                next_trading_cycle = wb_comleted_task.result()
                print("конец первой торговой итерации")

# Run the main function
if __name__ == "__main__":
    asyncio.run(MAIN().main_engin())


