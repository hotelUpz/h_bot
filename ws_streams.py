import json
import websockets
from data_sorting import SORT_DATA

WEBSOCKET_URL = "wss://fstream.binance.com/"

class WS_STREAMS(SORT_DATA):
    def __init__(self) -> None:
        super().__init__()
        self.handle_wb_message = self.log_exceptions_decorator(self.handle_wb_message)
        self.connect_to_websocket = self.log_exceptions_decorator(self.connect_to_websocket)

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
