import time,threading
import websocket
import json

acca = None

def on_message(ws, message):
    global acca
    data = json.loads(message)
    if 'data' in data:
        ticker_data = data['data'][0]
        acca = ticker_data[3]
        print(acca)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # 发送第一条订阅消息
    msg = {"event":"sub","params":{"biz":"exchange","type":"ticker","pairCode":"ETH_USDT","zip":False}}
    ws.send(json.dumps(msg))

    # 定时发送 ping 消息
    def send_ping():
        while True:
            ws.send(json.dumps({"event": "ping"}))
            time.sleep(5)

    # 开始发送 ping 消息
    send_ping_thread = threading.Thread(target=send_ping)
    send_ping_thread.start()

if __name__ == "__main__":
    url = "wss://candle.qkex.com/"
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
