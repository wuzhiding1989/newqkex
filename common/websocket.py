import json
from ws4py.client.threadedclient import WebSocketClient

class CG_Client(WebSocketClient):

    def opened(self):
        req = '{"event":"subscribe", "channel":"eth_usdt.deep"}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        if resp['type'] == 'orderBook':
            data = resp['data']
            if type(data) is dict:
                ask = data['asks'][0]
                print('Ask:', ask)
                bid = data['bids'][0]
                print('Bid:', bid)

if __name__ == '__main__':
    ws = None
    try:
        ws = CG_Client('ws://18.143.25.66:7100')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()