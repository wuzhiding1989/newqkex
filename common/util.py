import json
import requests
from BU.spot.api import webapi
import time,datetime,random
from decimal import *
import math
import sys
from ws4py.client.threadedclient import WebSocketClient


#获取买一卖一价 和数量
def price(symbol):
    orderbook = {'bid':[1000,1],'ask':[1001,2] }
    res = webapi.orderBook(symbol=symbol)
    if res['code'] !=0:
        print("获取买卖盘接口异常，异常原因：",res['msg'])
    orderbook['bid'][0] = res['data']['bids'][0][0]
    orderbook['bid'][1] = res['data']['bids'][0][1]
    orderbook['ask'][0] = res['data']['asks'][1][0]
    orderbook['ask'][1] = res['data']['asks'][1][1]
    return orderbook
#拿到所有币对余额
def assets():
    balance = {}
    res = webapi.exchange_assets()
    if res['code'] != 0:
        print("查询余额接口异常,异常原因：", res['msg'])
    res = res['data']
    for tmp in res:
        balance[tmp['symbol']] = tmp['available']
    return balance
#获取基础币和计价币
def symbolbase(symbol=None):
    symbols = {}
    aa = symbol.rfind('_')
    base = symbol[:aa]
    quote = symbol[aa + 1:]
    symbols['base'] = base
    symbols['quote'] = quote
    return symbols

#转成decimal类型，方便计算
def d(value,y=None,length=None):
    p=len(str(int(float(value))))
    if not length:
        length=28
    mycontext = Context(prec=p+length, rounding=ROUND_DOWN)  # ROUND_UP
    setcontext(mycontext)
    if y !=None:
        digits = y
        factor = 10 ** digits
        result = math.floor(value * factor) / factor
        return result
    return Decimal(value)
#查询历史订单id
def newhisorder(orderid,symbol):
    res = webapi.hisOrders(page=1,pageSize=10,symbol=symbol)
    res = res['data']['orders']
    for tmp in res:
        if tmp['id'] == orderid:
            return tmp

def send_dingtalk(text, token):
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    headers = {"Content-Type": "application/json"}
    data = {
        'msgtype': "text",
        'text': {
            "content": text
        }
    }
    r = requests.post(url, headers=headers, json=data)
    return r




if __name__ == '__main__':
    print(assets())
