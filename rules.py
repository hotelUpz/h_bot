from vars import VARIABLES

class RULESS(VARIABLES):
    def __init__(self):
        super().__init__()

    def is_close_1_pos_by_signal(self, symbol_item):
        try:
            if symbol_item["in_position_1"] and not symbol_item["in_position_2"]:
                cur_price = float(symbol_item["cur_price"])
                enter_1_pos_price = float(symbol_item["enter_1_pos_price"])
                position_1_side = symbol_item["position_1_side"]
                min_deviation_rate_for_1_position_closing = self.min_deviation_rate_for_1_position_closing / 100
                
                change_price_ratio = abs(cur_price - enter_1_pos_price) / enter_1_pos_price
                if position_1_side == "LONG":
                    if cur_price < enter_1_pos_price:
                        change_price_ratio = -change_price_ratio
                elif position_1_side == "SHORT":
                    if cur_price > enter_1_pos_price:
                        change_price_ratio = -change_price_ratio
                
                if change_price_ratio >= min_deviation_rate_for_1_position_closing:
                    print(f"Сработал тригер на продажу первой позиции по СИГНАЛУ. Монета {symbol_item.get('symbol')}")
                    return True

        except Exception as ex:
            print(ex)

        return False

    
    def close_1_pos_by_price(self, symbol_item):
        try:
            if symbol_item["in_position_1"] and not symbol_item["in_position_2"]:
                sl_condition = False
                tp_condition = False
                cur_price = float(symbol_item["cur_price"])
                enter_1_pos_price = float(symbol_item["enter_1_pos_price"])
                position_1_side = symbol_item["position_1_side"]
                
                change_price_ratio = abs(cur_price - enter_1_pos_price) / enter_1_pos_price
                if position_1_side == "LONG":
                    if cur_price < enter_1_pos_price:
                        change_price_ratio = -change_price_ratio
                elif position_1_side == "SHORT":
                    if cur_price > enter_1_pos_price:
                        change_price_ratio = -change_price_ratio

                if not self.only_take_profit_flag:
                    if change_price_ratio < 0:
                        sl_1_pos_rate = symbol_item["sl_1_pos_rate"] * symbol_item["sl_risk_reward_multiplier"]
                        sl_condition = abs(change_price_ratio) >= sl_1_pos_rate
                if not self.only_stop_loss_flag:
                    if change_price_ratio > 0:
                        tp_1_pos_rate = symbol_item["tp_1_pos_rate"] * symbol_item["tp_risk_reward_multiplier"]
                        tp_condition = change_price_ratio >= tp_1_pos_rate

                if tp_condition or sl_condition:
                    print(f"Сработал тригер на продажу первой позиции. Монета {symbol_item.get('symbol')}")
                    return True

        except Exception as ex:
            print(ex)

        return False

    
    # def position_1_averaging_conditions(self, symbol_item):
    #     is_averaging_flag = False
    #     try:
    #         if symbol_item["in_position_1"]:
    #             cur_price = symbol_item["cur_price"]
    #             position_1_side = symbol_item["position_1_side"]
    #             enter_1_pos_price = symbol_item["enter_1_pos_price"]
    #             averaging_step_rate = self.averaging_step_rate/ 100
    #             pos_1_profit_rate = abs(cur_price - enter_1_pos_price)/ enter_1_pos_price
    #             current_step_counter = int(abs(pos_1_profit_rate)/ averaging_step_rate)
    #             if position_1_side == "LONG":                    
    #                 if cur_price < enter_1_pos_price:
    #                     pos_1_profit_rate = - pos_1_profit_rate
    #             if position_1_side == "SHORT":                    
    #                 if cur_price > enter_1_pos_price:
    #                     pos_1_profit_rate = - pos_1_profit_rate
    #             if pos_1_profit_rate < 0:
    #                 if (current_step_counter > position_1_side["position_1_averaging_counter"]):
    #                     position_1_side["position_1_averaging_counter"] += 1
    #                     is_averaging_flag = True
    #     except Exception as ex:
    #         print(ex)
                    
    #     return symbol_item, is_averaging_flag
    
    # def close_both_pos_conditiond(self, cur_price, current_step_counter):
    #     if self.in_position_1 and self.in_position_2:
    #         total_tp_rate = self.total_tp_rate/ 100
    #         total_sl_rate = self.total_sl_rate/ 100
    #         pos_1_profit_rate = abs(cur_price - self.enter_1_pos_price)/ self.enter_1_pos_price
    #         pos_2_profit_rate = abs(cur_price - self.enter_2_pos_price)/ self.enter_2_pos_price

    #         if self.position_1_side == "LONG":                    
    #             if cur_price < self.enter_1_pos_price:
    #                 pos_1_profit_rate = - pos_1_profit_rate
    #         if self.position_1_side == "SHORT":                    
    #             if cur_price > self.enter_1_pos_price:
    #                 pos_1_profit_rate = - pos_1_profit_rate
    #         if self.posicion_2_side == "LONG":                    
    #             if cur_price < self.enter_2_pos_price:
    #                 pos_2_profit_rate = - pos_2_profit_rate
    #         if self.posicion_2_side == "SHORT":                    
    #             if cur_price > self.enter_2_pos_price:
    #                 pos_2_profit_rate = - pos_2_profit_rate
    #         if pos_1_profit_rate < 0 and pos_2_profit_rate < 0:
    #             # print("На текущий момент две позиции в минусе...")
    #             if abs(pos_1_profit_rate + pos_2_profit_rate) >= total_sl_rate:
    #                 return (self.position_1_side, "Sell", 1), (self.posicion_2_side, "Sell", 2)            
    #         elif pos_1_profit_rate + pos_2_profit_rate >= total_tp_rate:                
    #             return (self.position_1_side, "Sell", 1), (self.posicion_2_side, "Sell", 2)        
    #         if (current_step_counter >= self.position_1_averaging_counter_limit) and (pos_2_profit_rate > 0):
    #             return None, (self.posicion_2_side, "Sell", 2)
            
    #     return
    
    # def instruction_collector(self, symbol_item):
    #     signal = symbol_item["firts_signal"]
    #     cur_price = symbol_item["cur_price"]
    #     current_step_counter = symbol_item["current_step_counter"]
    #     position_1_averaging_counter = symbol_item["position_1_averaging_counter"]

    #     pos_1_assets = None
    #     pos_2_assets = None

    #     open_pos_conditions_resp = self.open_2_pos_conditions(signal)
    #     if open_pos_conditions_resp:
    #         pos_1_assets = open_pos_conditions_resp
    #         return None, pos_2_assets
        
    #     close_1_pos_conditiond_resp = self.close_1_pos_conditiond(signal, cur_price)
    #     if close_1_pos_conditiond_resp:
    #         pos_1_assets = close_1_pos_conditiond_resp
    #         return pos_1_assets, None
        
    #     position_1_averaging_conditions_resp = self.position_1_averaging_conditions(cur_price, current_step_counter, position_1_averaging_counter)
    #     if position_1_averaging_conditions_resp:
    #         pos_1_assets, self.current_step_counter, self.position_1_averaging_counter = position_1_averaging_conditions_resp
    #         if pos_1_assets:
    #             return pos_1_assets, None
            
    #     close_both_pos_conditiond_resp = self.close_both_pos_conditiond(cur_price, current_step_counter)
    #     if close_both_pos_conditiond_resp:
    #         pos_1_assets, pos_1_assets = close_both_pos_conditiond_resp
    #         if pos_1_assets or pos_2_assets:
    #             return pos_1_assets, pos_2_assets
            
    #     return None, None
