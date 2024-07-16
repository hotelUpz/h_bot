import asyncio
from datetime import datetime as dttm
from ws_streams import WS_STREAMS
from api_binance import aiohttp_connector
import os
import inspect

current_file = os.path.basename(__file__)

class TEMP(WS_STREAMS):
    def __init__(self):
        super().__init__()

    async def trade_setup_template(self, session, lev_size):
        async def trade_setup_unit(session, symbol, lev_size):
            try:
                self.handle_messagee(f'Устанавливаем тип маржи для {symbol}:')
                set_margin_resp = await self.set_margin_type(session, symbol, self.margin_type)
                self.handle_messagee(f"Монета {symbol}: {str(set_margin_resp)}")
                
                self.handle_messagee(f'Устанавливаем кредитное плечо для {symbol}:')
                set_leverage_resp = await self.set_leverage(session, symbol, lev_size)
                self.handle_messagee(str(set_leverage_resp))
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

        tasks = [trade_setup_unit(session, symbol_item["symbol"], lev_size) for symbol_item in self.trading_data_list if symbol_item["first_trade"]]
        if tasks:
            await asyncio.gather(*tasks)

    async def is_closing_positions_template(self, session, pos_num, is_finish_flag=False):
        tasks = []
        exception_symbol_list = []
        tasks = [self.is_closing_position_true(session, symbol_item["symbol"], symbol_item[f"position_{pos_num}_side"]) for symbol_item in self.trading_data_list]

        if tasks:
            is_closing_positions_symbol_list = await asyncio.gather(*tasks)
            for symbol_item in self.trading_data_list:
                for is_closed, symb in is_closing_positions_symbol_list:
                    if symbol_item["symbol"] == symb:
                        if self.should_close_position(symbol_item) and is_closed:
                            exception_symbol_list.append(symb)
                            break
                        elif self.should_open_position(symbol_item) and not is_closed:
                            exception_symbol_list.append(symb)
                            break
                        elif is_finish_flag and is_closed:
                            exception_symbol_list.append(symb)
        return exception_symbol_list
    
    def should_open_position(self, symbol_item):
        return symbol_item.get("is_opening_1_pos") or symbol_item.get("is_opening_2_pos")

    def should_close_position(self, symbol_item):
        return symbol_item.get("is_closing_1_pos") or symbol_item.get("is_closing_2_pos")
       
    def get_side(self, symbol_item, pos_number):
        side = None
        if self.should_close_position(symbol_item) or self.should_open_position(symbol_item):
            position_side = symbol_item.get(f"position_{pos_number}_side")
            if self.should_close_position(symbol_item):
                side = "SELL" if position_side == "LONG" else "BUY"
            else:
                side = "BUY" if position_side == "LONG" else "SELL"
        return side

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

    async def make_orders_template(self, session, pos_number, exception_list):
        for i, symbol_item in enumerate(self.trading_data_list):
            if symbol_item.get("first_trade"):
                self.trading_data_list[i]["first_trade"] = False
                self.trading_data_list[i]["quantity_precision"], _, self.trading_data_list[i]["min_notional"] = self.get_precisions(symbol_item.get("symbol"), self.exchange_data)
                self.trading_data_list[i]["qty"] = self.usdt_to_qnt_converter(symbol_item.get("cur_price"), self.trading_data_list[i]["quantity_precision"], self.trading_data_list[i]["min_notional"])

        tasks = [self.make_order(session, symbol_item["symbol"], symbol_item["qty"], self.get_side(symbol_item, pos_number), 'MARKET', symbol_item.get(f"position_{pos_number}_side")) for symbol_item in self.trading_data_list if symbol_item["symbol"] not in exception_list]    
        if tasks:
            return await asyncio.gather(*tasks)
        return []

    @aiohttp_connector
    async def make_orders_total_template(self, session):
        exception_list = []
        for pos_number in [1,2]:
            if any(symbol_item.get(f"is_opening_{pos_number}_pos") or symbol_item.get(f"is_closing_{pos_number}_pos") for symbol_item in self.trading_data_list):
                try:        
                    await self.trade_setup_template(session, self.lev_size)
                    exception_list = await self.is_closing_positions_template(session, pos_number)
                    print(f"exception_list: {exception_list}")
                    make_order_results = await self.make_orders_template(session, pos_number, exception_list)
                    if make_order_results:
                        self.process_order_results(make_order_results, pos_number)
                except Exception as ex:
                    self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

    def process_order_results(self, make_order_results, pos_number):
        for item_res in make_order_results:
            if item_res:
                order_logger_resp = self.orders_logger_hundler(item_res)
                if order_logger_resp:
                    self.update_position_status(item_res, pos_number)

    def update_position_status(self, item_res, pos_number):
        for i, symbol_item in enumerate(self.trading_data_list):
            if symbol_item["symbol"] == item_res["symbol"]:
                self.trading_data_list[i][f"in_position_{pos_number}"] = not symbol_item.get(f"is_closing_{pos_number}_pos") 
                self.trading_data_list[i][f"is_opening_{pos_number}_pos"] = False
                self.trading_data_list[i][f"is_closing_{pos_number}_pos"] = False                      
                self.trading_data_list[i][f"enter_{pos_number}_pos_price"] = item_res.get("avgPrice", None)
                self.trading_data_list[i]["qty"] = item_res.get("executedQty", None)
                self.trading_data_list[i]["signal"] = None      
                break

    @aiohttp_connector
    async def is_finish_trade_cycle_true(self, session):
        print("Проверка завершения торгового цикла")

        # Проверка на закрытие всех позиций
        if all((not x.get("in_position_1") and not x.get("in_position_2")) for x in self.trading_data_list):
            print('Все позиции закрыты')
            return True

        not_active_symbol_list = []

        # Проверка позиций для каждого номера
        for pos_num in [1, 2]:
            temperary_not_active_symbol_list = await self.is_closing_positions_template(session, pos_num, True)
            if temperary_not_active_symbol_list:      
                not_active_symbol_list += [(x, pos_num) for x in temperary_not_active_symbol_list]

        # Проверка длины списка неактивных символов
        if len(not_active_symbol_list) == len(self.trading_data_list) * 2:
            print("Все позиции для всех символов закрыты")
            return True

        # Обновление списка торговых данных
        for symb, pos_n in not_active_symbol_list:
            for i, item_list in enumerate(self.trading_data_list):
                if item_list.get("symbol") == symb:
                    self.trading_data_list[i][f"in_position_{pos_n}"] = False
                    break

        return False


