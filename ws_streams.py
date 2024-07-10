import json
import websockets
from data_sorting import SORT_DATA

WEBSOCKET_URL = "wss://fstream.binance.com/"

class WS_STREAMS(SORT_DATA):
    def __init__(self) -> None:
        super().__init__()

    async def handle_message(self, message, recent_klines_dict):
        # await asyncio.sleep(0.01)
        message = json.loads(message)['data']
        # print(message['k']['x'])
        if message['e'] == 'kline' and message['k']['x']:  # Check if the kline is closed
            symbol = message['s']
            if symbol not in recent_klines_dict:
                recent_klines_dict[symbol] = []
            await self.process_kline_data(message['k'], recent_klines_dict[symbol], symbol)

    async def connect_to_websocket(self, symbols, recent_klines_dict):
        print("connect_to_websocket")
        stream_chunks = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]  # Dividing symbols into chunks
        is_wb_finish = False
        for chunk in stream_chunks:
            streams = [f"{symbol.lower()}@kline_1m" for symbol in chunk]  # Example using 1-minute interval
            url = f"{WEBSOCKET_URL}stream?streams={'/'.join(streams)}"
            async with websockets.connect(url) as websocket:
                async for message in websocket:
                    await self.handle_message(message, recent_klines_dict)
                    if all(x.get("is_total_closing", False) for x in self.signals_data_list):
                        is_wb_finish = True 
                        break

        return is_wb_finish
                       
