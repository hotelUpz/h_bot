import json
import websockets
import time
from data_sorting import REFACT_DATA

WEBSOCKET_URL = "wss://fstream.binance.com/"

class WS_STREAMS(REFACT_DATA):
    def __init__(self) -> None:
        super().__init__()
        self.handle_ws_message = self.log_exceptions_decorator(self.handle_ws_message)
        self.connect_to_websocket = self.log_exceptions_decorator(self.connect_to_websocket)

    async def handle_ws_message(self, message):
        message = json.loads(message)['data']
        if message['e'] == 'kline':
            is_kline_closed_true = message['k']['x']
            symbol = message['s']
            await self.process_trading_data(message['k'], symbol, is_kline_closed_true)

    async def connect_to_websocket(self, symbols):
        print("connect_to websocket")
        self.start_time = time.time() 
        stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
        is_wb_finish = False

        async def connect_and_handle(chunk):
            streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]
            url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
            async with websockets.connect(url) as websocket:
                async for message in websocket:
                    await self.handle_ws_message(message)
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