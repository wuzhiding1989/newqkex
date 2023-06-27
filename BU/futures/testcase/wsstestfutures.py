import time,threading
import websocket
import json



import json
import websocket

url = "wss://ws-socket.qkex.com/notification/v3"
message_data1 = {"event":"authorization","data":[{"token":"eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMWIwNjMyNi05MjI0LTQ3NzUtYmQxZC1hOWNmOGFhZTMyN2YxODk5Nzc2NTE5IiwidWlkIjoieFFVVTduOEZPSUhEWDdyVXNIVTZuUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJiSjkrbjREKzMxc0ZycUhMM0g4dTJnPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4NjkwOTQwNywiZXhwIjoxNjg2OTk1ODA3LCJpc3MiOiJ3Y3MifQ.jiM0-pUVMvsIn5DRKMI4G_rhKcnPpSelFx96qMGsOmI"}]}
#msg_str = json.dumps(msg)

#mport json
import websocket
# import protobuf
# import types
import struct
#url = "wss://ws-socket.qkex.com/v1/market"
#message_data1 = {
#     "event": "subscribe",
#     "data": [
#         {
#             "tradeType": "linearPerpetual",
#             "symbol": "BTCUSDT",
#             "stream": "kline1m"
#         }
#     ]
# }
message_data = {
    "event": "subscribe",
    "data": [{"tradeType": "linearPerpetual", "symbol": "BTCUSDT", "stream": "trade"}]}
format_str = '<12s8si5d3??Z1s'
def on_message(ws, message):
    b = message
    print(b.decode('utf-8', 'ignore'))
def on_error(ws, error):
    print("Error:", error)
def on_close(ws):
    print("### closed ###")
def on_open(ws):
    # print("### opened ###")
    # 发送订阅消息
    ws.send(json.dumps(message_data1))
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
