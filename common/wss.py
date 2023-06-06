"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: wss
@time: 2023-05-26 
@desc: 
"""
import asyncio
import json
import ssl
import websockets
import time
import struct

async def hello():
    uri="wss://ws-socket.qkex.com/v1/market"
    async with websockets.connect(uri) as ws:
        while True:
            subscribe_index = {"event": "subscribe",
                               "data": [{"tradeType": "linearPerpetual", "symbol": "BTCUSDT", "stream": "index"}]}
            await ws.send(json.dumps(subscribe_index))
            print(f">{subscribe_index}")

            greeting=await ws.recv()
            print(f"<{greeting}")
            if "\n" in str(greeting):
                print(struct.unpack('h',greeting))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())