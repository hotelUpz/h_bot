# # import random
# # from time import sleep 

# # def foo(diversification_number):    
# #     trade_li = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# #     signals_stock = len(trade_li)
# #     trade_litemp = []
# #     trade_res = []

# #     if signals_stock >= diversification_number:                            
# #         step = diversification_number 
# #     else:
# #         step = signals_stock

# #     for i in range(0, signals_stock, step):
# #         trade_litemp = trade_li[i:step+i]
# #         # print(trade_litemp)
# #         # print(f"trade_litemp: {trade_litemp}")
# #         cur_slice = random.randrange(0, len(trade_litemp)+1)
# #         trade_res += trade_litemp[:cur_slice]
# #         # print(f"trade_res: {trade_res}")

# #         if len(trade_res) >= diversification_number:           
# #             return True, trade_res
        
# #         step = step - len(trade_res) if step > len(trade_res) else 1
# #         # print(f"step: {step}")
# #         # sleep(1)
        
# #     if len(trade_res) > 0:            
# #         return True, trade_res

# #     return False, []

# # diversification_number = 15
# # for _ in range(10):
# #     tr, lenn = foo(diversification_number)
# #     print(lenn)
# #     if len(lenn) > diversification_number:
# #         print("Some mistake...")
# # print("Ex!!")


# # #     # remaining_signals = signals_stock  % diversification_number
        
# # #     # if remaining_signals != 0:
# # #     #     tradin_tail = remaining_signals-len(trade_res) if remaining_signals > len(trade_res) else remaining_signals
# # #     #     cur_slice = random.randrange(1, tradin_tail+1)
# # #     #     trade_res += trade_li[-tradin_tail: -cur_slice]


# import random

# def foo(diversification_number):    
#     trade_li = [1,2,3,4,5,6,7,8,9,10,11,12,13]
#     signals_stock = len(trade_li)
#     trade_res = []

#     step = min(diversification_number, signals_stock)

#     for i in range(0, signals_stock, step):
#         trade_litemp = trade_li[i:step + i]
#         cur_slice = random.randrange(0, len(trade_litemp) + 1)
#         trade_res += trade_litemp[:cur_slice]

#         if len(trade_res) >= diversification_number:
#             return True, trade_res[:diversification_number]

#         remaining_positions_needed = diversification_number - len(trade_res)
#         step = min(max(remaining_positions_needed, 1), signals_stock - i - step)

#     if len(trade_res) > 0:
#         return True, trade_res

#     return False, []

# diversification_number = 28
# for _ in range(3000):
#     tr, lenn = foo(diversification_number)
#     print(lenn)
#     if len(lenn) > diversification_number:
#         print("Some mistake...")
# print("Ex!!")

d = 0*-1

if d:
    print(d)
