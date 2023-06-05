
import websocket
import json
import ssl

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### connected ###")
    ws.send(json.dumps(subscribe_index))

if __name__ == "__main__":
    ws_url = "wss://ws-socket.qkex.com/v1/market"
    subscribe_index = {"event":"subscribe","data":[{"tradeType":"linearPerpetual","symbol":"BTCUSDT","stream":"trade"}]}
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open,
                                )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})



