from vars import VARIABLES

class RULESS(VARIABLES):
    def __init__(self):
        super().__init__()

    def handle_positions_rules(self, symbol_item):
        try:
            if symbol_item.get("in_position_1") or symbol_item.get("in_position_2"):
                instruction_list = []
                for pos_num in [1, 2]:
                    if not symbol_item.get(f"in_position_{pos_num}"):                        
                        continue
                    hedg_num = 2 if pos_num == 1 else 1
                    enter_pos_price = symbol_item.get(f"enter_{pos_num}_pos_price")
                    if not isinstance(enter_pos_price, float):
                        continue

                    cur_price = float(symbol_item.get("cur_price"))
                    position_side = symbol_item.get(f"position_{pos_num}_side")
                    signal = symbol_item.get("signal")
                    change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price
                    is_two_pos_now = symbol_item.get("in_position_1") and symbol_item.get("in_position_2")

                    if position_side == "LONG":
                        if self.strong_opposite_signal_flag:
                            if signal == 1:
                                # print("signal == 1 was skiped")
                                continue
                        if cur_price < enter_pos_price:
                            change_price_ratio = -change_price_ratio
                    elif position_side == "SHORT":
                        if self.strong_opposite_signal_flag:
                            if signal == -1:
                                # print("signal == -1 was skiped")
                                continue
                        if cur_price > enter_pos_price:
                            change_price_ratio = -change_price_ratio

                    if not signal:
                        if not is_two_pos_now or self.price_triger_than_both_pos_opened_true:                       
                            sl_condition = not is_two_pos_now and not self.only_take_profit_flag and change_price_ratio < 0 and abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
                            tp_condition = not self.only_stop_loss_flag and change_price_ratio > 0 and change_price_ratio >= symbol_item.get("tp_pos_rate")

                            if tp_condition or sl_condition:
                                print(f'Сработал тригер цены на закрытие {pos_num} позиции для {symbol_item.get("symbol")}')
                                instruction_list.append(("closing", pos_num))
                    else:                        
                        if change_price_ratio >= symbol_item.get("min_deviation_rate"):
                            print(f'Поступил сигнал на закрытие {pos_num} позиции для {symbol_item.get("symbol")}')
                            instruction_list.append(("closing", pos_num))
                            continue
                        if not is_two_pos_now:
                            print(f'Поступил сигнал. Хеджируемся. Символ: {symbol_item.get("symbol")}')
                            instruction_list.append(("opening", hedg_num))
                        else:
                            print("Сигнал проигнорирован из-за несоответствия минимальному спреду для закрытия")

                return instruction_list

        except Exception as ex:
            print(f'file rules.py: {ex}')
        return []