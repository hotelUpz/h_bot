import json
import websockets
from data_sorting import SORT_DATA

WEBSOCKET_URL = "wss://fstream.binance.com/"

class WS_STREAMS(SORT_DATA):
    def __init__(self) -> None:
        super().__init__()

    async def handle_wb_message(self, message, recent_klines_dict):
        message = json.loads(message)['data']
        if message['e'] == 'kline':
            symbol = message['s']
            if symbol not in recent_klines_dict:
                recent_klines_dict[symbol] = []
            is_closed = message['k']['x']
            await self.process_kline_data(message['k'], recent_klines_dict[symbol], symbol, is_closed)

    async def connect_to_websocket(self, symbols, recent_klines_dict):
        print("connect_to_websocket")
        stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
        is_wb_finish = False

        async def connect_and_handle(chunk):
            streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
            url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
            async with websockets.connect(url) as websocket:
                async for message in websocket:
                    await self.handle_wb_message(message, recent_klines_dict)
                    if self.next_trading_cycle_event.is_set():
                        await websocket.close()
                        return True
            return False

        for chunk in stream_chunks:
            if await connect_and_handle(chunk):
                is_wb_finish = True
                break

        # Проверяем завершение внешнего цикла после закрытия сокета
        if self.next_trading_cycle_event.is_set():
            is_wb_finish = True

        return is_wb_finish


    # async def connect_to_websocket(self, symbols, recent_klines_dict):
    #     print("connect_to_websocket")
    #     stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
    #     is_wb_finish = False

    #     for chunk in stream_chunks:
    #         streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
    #         url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"

    #         async with websockets.connect(url) as websocket:
    #             async for message in websocket:
    #                 await self.handle_wb_message(message, recent_klines_dict)

    #                 if self.next_trading_cycle_event.is_set():
    #                     is_wb_finish = True
    #                     await websocket.close()
    #                     break

    #         if is_wb_finish:
    #             break

    #     # Проверяем завершение внешнего цикла после закрытия сокета
    #     if self.next_trading_cycle_event.is_set():
    #         is_wb_finish = True

    #     return is_wb_finish


    # async def connect_to_websocket(self, symbols, recent_klines_dict):
    #     print("connect_to_websocket")
    #     stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]  # Dividing symbols into chunks
    #     is_wb_finish = False
    #     for chunk in stream_chunks:
    #         streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]  # Example using 1-minute interval
    #         url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
    #         async with websockets.connect(url) as websocket:
    #             async for message in websocket:
    #                 await self.handle_wb_message(message, recent_klines_dict)                    
    #                 if self.next_trading_cycle_event.is_set():                                                  
    #                     is_wb_finish = True 
    #                     await websocket.close()
    #                     break
    #         if self.next_trading_cycle_event.is_set():
    #             # print(f"is_wb_finish2: {is_wb_finish}")
    #             is_wb_finish = True
    #             break        
    #     return is_wb_finish
