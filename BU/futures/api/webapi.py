import copy
import requests

headers = {"Content-Type": "application/json","Accept-Language":"zh-CN","source":"web","X-Authorization":""}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyN2MwNjE5Zi04N2FlLTQ4ODEtYjFkMi1lODFlZGZjNzcxZmEiLCJ1aWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJiaWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJpcCI6IkdwdHl4M01ZbzBJemNsL3pwN0ZiNXc9PSIsImRldiI6InAva3BIckF3RkJjSUZleXg0U2xkZGc9PSIsInN0cyI6MCwiaWF0IjoxNjcyNTAyNDAwLCJleHAiOjE2ODgxNDA4MDAsImlzcyI6InFrZXgifQ.7HKuzZz-IC0_Zs5hVK420jVbgpsgRP-NlYtxrUiTs0U'
Authorization1='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNTk4ZDBiOS1lOTcyLTQ1N2MtOWRmOS1lMTAyOGQ2MmM1Y2YxOTkyNDEyMzQzIiwidWlkIjoiaDBsVXZiR0t2SkdkdGVscGYxQWRZUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJkRmxJM3RwSFdJdHpsNk9rTDRBSlBRPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4Mzc5MjQ0NiwiZXhwIjoxNjgzODc4ODQ2LCJpc3MiOiJ3Y3MifQ.IErDpB3ydg6mbOxbq6TlMA-0quPgzx6ep2uNkE0Q7nU'
headers['X-Authorization']=Authorization
tradeurl = 'http://qraft-trade-api.qkex.com/v1'

def futures_transfer(fromAccountType=None,toAccountType=None,currency=None,amount=None):#合约划转
    path = '/trade/web/account/transfer'
    params = {
    "fromAccountType": fromAccountType,
    "toAccountType": toAccountType,
    "currency": currency,
    "amount": amount}
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res
def futures_instruments():
    path ='/v1/public/web/instruments'
    res = requests.get(url=tradeurl+path,headers=headers)
    return res

def futures_order():#单个下单
    path = '/trade/web/orders'
    params= {  "tradeType": "linearPerpetual",
    "symbol": "BTCUSDT",
    "side": "sell",
    "positionSide": "short",
    "orderType": "limit",#market，limit
    "reduceOnly": 'false',
    "marginType": "cross",
    "price": "20000",
    "priceType": "optimalN",
    "orderQty": "1",
    "postOnly": 'false',
    "timeInForce": "GTC"}#GTC/IOC/FOK
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res

def futures_oneClickClose():#一键平仓
    path = '/trade/web/oneClickClose'
    params = {
        "tradeType": "linearPerpetual",
         "symbol": "BTCUSDT"}
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res
def futures_position():#查询持仓
    path = '/trade/web/position'
    params = {
        "tradeType": "linearPerpetual",
        "symbol": "BTCUSDT",
        "marginType": "cross"}
    res = requests.get(url=tradeurl+path,params=params,headers=headers).json()
    return  res
def futures_orders_cancel():#撤销单个订单
    path = '/trade/web/orders/cancel'
    params = {
        "tradeType": "linearPerpetual",
         "symbol": "BTCUSDT",
        "orderId": "123456023424242423"}
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res
def futures_orders_oneClickClose():#一键撤销所有订单
    path = '/trade/web/orders/oneClickCancel'
    params = {
        "tradeType": "linearPerpetual",
         "symbol": "BTCUSDT"}
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res

def futures_openOrders():#当前委托-tradeType=linearPerpetual&side=buy&symbol=BTCUSDT&orderId=6699123456653&clOrdId=6699123456653&pageNum=1&pageSize=10
    path = '/trade/web/openOrders'
    params = {
        "tradeType": "linearPerpetual",
        "symbol": "BTCUSDT",
        "pageNum":  1,
        "pageSize":  10}
    res = requests.post(url=tradeurl+path,json=params,headers=headers).json()
    return res

if __name__ == '__main__':
    print(futures_transfer(fromAccountType='funding',toAccountType='futures',currency='USDT',amount='200'))
    #print(futures_order())
    print(futures_position())