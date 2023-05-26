import websockets.client
import websocket
import json
import ssl

def on_message(ws, message):
    data = json.loads(message)
def on_error(ws, error):
    print(error)
def on_close(ws, *args):
    print("### closed ###")

def on_open(ws):
    print("### connected ###")
    subscribe_index = {"event":"subscribe","data":[{"tradeType":"linearPerpetual","symbol":"BTCUSDT","stream":"index"}]}
    subscribe_ticker24hr = {"event":"subscribe","data":[{"tradeType":"linearPerpetual","symbol":"BTCUSDT","stream":"ticker24hr"}]}
    subscribe_trade = {"event": "subscribe", "data": [{"tradeType": "linearPerpetual", "symbol": "BTCUSDT", "stream": "trade"}]}
    subscribe_depth0 = {"event":"subscribe","data":[{"tradeType":"linearPerpetual","symbol":"BTCUSDT","stream":"depth0"}]}
    ws.send(json.dumps(subscribe_index))
    # ws.send(json.dumps(subscribe_ticker24hr))
    # ws.send(json.dumps(subscribe_trade))
    # ws.send(json.dumps(subscribe_depth0))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-socket.qkex.com/v1/market",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


