from vars import VARIABLES

class RULESS(VARIABLES):
    def __init__(self):
        super().__init__()

    def handle_positions_rules(self, symbol_item):
        try:
            if symbol_item.get("in_position_1") or symbol_item.get("in_position_2"):
                instruction_list = []
                for pos_num in [1, 2]:
                    if not symbol_item[f"in_position_{pos_num}"]:
                        continue
                    hedg_num = 2 if pos_num == 1 else 1
                    enter_pos_price = float(symbol_item.get(f"enter_{pos_num}_pos_price"))
                    if not isinstance(enter_pos_price, float):
                        continue

                    cur_price = float(symbol_item.get("cur_price"))
                    position_side = symbol_item.get(f"position_{pos_num}_side")
                    signal = symbol_item.get("signal")
                    change_price_ratio = abs(cur_price - enter_pos_price) / enter_pos_price

                    if position_side == "LONG":
                        if signal == 1:
                            continue
                        if cur_price < enter_pos_price:
                            change_price_ratio = -change_price_ratio
                    elif position_side == "SHORT":
                        if signal == -1:
                            continue
                        if cur_price > enter_pos_price:
                            change_price_ratio = -change_price_ratio

                    if not signal:
                        # Check if we should close the position due to price
                        sl_condition = not self.only_take_profit_flag and change_price_ratio < 0 and abs(change_price_ratio) >= symbol_item.get("sl_pos_rate")
                        tp_condition = not self.only_stop_loss_flag and change_price_ratio > 0 and change_price_ratio >= symbol_item.get("tp_pos_rate")

                        if tp_condition or sl_condition:
                            print(f"Triggered closing position {pos_num} due to price for {symbol_item.get('symbol')}.")
                            instruction_list.append(("closing", pos_num))
                    else:
                        # Check if we should close the position due to signal
                        if change_price_ratio >= symbol_item.get("min_deviation_rate"):
                            print(f"Triggered closing position {pos_num} due to signal for {symbol_item.get('symbol')}.")
                            instruction_list.append(("closing", pos_num))
                            continue
                        print(f"Triggered hedging position {pos_num} due to signal for {symbol_item.get('symbol')}.")
                        instruction_list.append(("opening", hedg_num))

                return instruction_list

        except Exception as ex:
            print(ex)
        return []

