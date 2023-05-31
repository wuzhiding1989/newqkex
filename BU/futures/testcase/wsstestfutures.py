import json,ssl
import websocket
#from WsDataDTO_pb2 import WsKlineDTO

# 创建 WebSocket 连接
ws_url = "wss://ws-socket.qkex.com/v1/market"
subscribe_index = {"event":"subscribe","data":[{"tradeType":"linearPerpetual","symbol":"BTCUSDT","stream":"kline1m"}]}

import asyncio
import websockets
import json


import asyncio
import websockets
import json
import ssl

ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE

async def connect():
    async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
        await websocket.send(json.dumps(subscribe_index))
        while True:
            response = await websocket.recv()
            response_dict = json.loads(response)
            if 'data' in response_dict:
                data = response_dict['data']
                for item in data:
                    if 'stream' in item and item['stream'] == 'kline1m':
                        kline_data = item['data']
                        for kline in kline_data:
                            print(f"Period: {kline['p']}")
                            print(f"Open Time: {kline['ot']}")
                            print(f"Close Time: {kline['ct']}")
                            print(f"Open Price: {kline['op']}")
                            print(f"Close Price: {kline['cp']}")
                            print(f"High Price: {kline['h']}")
                            print(f"Low Price: {kline['l']}")
                            print(f"Volume: {kline['v']}")
                            print(f"Quote Value: {kline['q']}")
                            print(f"Count: {kline['c']}")
                            print(f"Price Change: {kline['pc']}")
                            print(f"Price Change Percent: {kline['pcp']}")
                            print("\n")

asyncio.get_event_loop().run_until_complete(connect())




# ws = websocket.WebSocketApp(ws_url,
#                             on_open=on_open,
#                             on_message=on_message,
#                             on_error=lambda ws, error: print(error),
#                             on_close=lambda ws: print("WebSocket closed"))

# 运行 WebSocket 连接
# ws.run_forever()
# ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

