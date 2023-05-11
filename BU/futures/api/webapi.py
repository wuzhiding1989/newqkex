import copy
import requests
symbol='BTCUSDT';tradeType='linearPerpetual';side='buy';marginType='cross';positionSide='positionSide'
postOnly='false';reduceOnly='false';orderType='limit';priceType='optimalN';pageNum='1';pageSize='10'
headers = {"Content-Type": "application/json", "Accept-Language": "zh-CN", "source": "web", "X-Authorization": ""}
Authorization = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyN2MwNjE5Zi04N2FlLTQ4ODEtYjFkMi1lODFlZGZjNzcxZmEiLCJ1aWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJiaWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJpcCI6IkdwdHl4M01ZbzBJemNsL3pwN0ZiNXc9PSIsImRldiI6InAva3BIckF3RkJjSUZleXg0U2xkZGc9PSIsInN0cyI6MCwiaWF0IjoxNjcyNTAyNDAwLCJleHAiOjE2ODgxNDA4MDAsImlzcyI6InFrZXgifQ.7HKuzZz-IC0_Zs5hVK420jVbgpsgRP-NlYtxrUiTs0U'
Authorization1 = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNTk4ZDBiOS1lOTcyLTQ1N2MtOWRmOS1lMTAyOGQ2MmM1Y2YxOTkyNDEyMzQzIiwidWlkIjoiaDBsVXZiR0t2SkdkdGVscGYxQWRZUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJkRmxJM3RwSFdJdHpsNk9rTDRBSlBRPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4Mzc5MjQ0NiwiZXhwIjoxNjgzODc4ODQ2LCJpc3MiOiJ3Y3MifQ.IErDpB3ydg6mbOxbq6TlMA-0quPgzx6ep2uNkE0Q7nU'
headers['X-Authorization'] = Authorization
tradeurl = 'http://qraft-trade-api.qkex.com/v1'

#划转
def futures_transfer(fromAccountType=None, toAccountType=None, currency=None, amount=None):  # 合约划转
    path = '/trade/web/account/transfer'
    params = {
        "fromAccountType": fromAccountType,
        "toAccountType": toAccountType,
        "currency": currency,
        "amount": amount}
    res = requests.post(url=tradeurl + path, json=params, headers=headers).json()
    return res


def futures_order(tradeType=None, symbol=None, side=None, positionSide=None, orderType=None, reduceOnly=None,
                  marginType=None, price=None,priceType=None,orderQty=None,postOnly=None,timeInForce=None ):  # 单个下单
    path = '/trade/web/orders'
    params = {"tradeType": tradeType,
              "symbol": symbol,
              "side": side,
              "positionSide": positionSide,
              "orderType": orderType,  # market，limit
              "reduceOnly": reduceOnly,
              "marginType": marginType,
              "price": price,
              "priceType": priceType,
              "orderQty": orderQty,
              "postOnly": postOnly,
              "timeInForce": timeInForce}  # GTC/IOC/FOK
    res = requests.post(url=tradeurl + path, json=params, headers=headers).json()
    return res


def futures_oneClickClose(tradeType=None,symbol=None):  # 一键平仓
    path = '/trade/web/oneClickClose'
    params = {
        "tradeType": tradeType,
        "symbol": symbol}
    res = requests.post(url=tradeurl + path, json=params, headers=headers).json()
    return res


def futures_position(tradeType=None,symbol=None,marginType=None):  # 查询持仓
    path = '/trade/web/position'
    params = {
        "tradeType": tradeType,
        "symbol": symbol,
        "marginType": marginType}
    res = requests.get(url=tradeurl + path, params=params, headers=headers).json()
    return res


def futures_orders_cancel(tradeType=None,symbol=None,orderId=None):  # 撤销单个订单
    path = '/trade/web/orders/cancel'
    params = {
        "tradeType": tradeType,
        "symbol": symbol,
        "orderId": orderId}
    res = requests.post(url=tradeurl + path, json=params, headers=headers).json()
    return res


def futures_orders_oneClickClose(tradeType=None,symbol=None):  # 一键撤销所有订单
    path = '/trade/web/orders/oneClickCancel'
    params = {
        "tradeType": tradeType,
        "symbol": symbol}
    res = requests.post(url=tradeurl + path, json=params, headers=headers).json()
    return res


def futures_openOrders(tradeType=None,symbol=None,side=None,clOrdId=None,orderId=None,pageNum=None,pageSize=None):  # 当前委托-tradeType=linearPerpetual&side=buy&symbol=BTCUSDT&orderId=6699123456653&clOrdId=6699123456653&pageNum=1&pageSize=10
    path = '/trade/web/openOrders'
    params = {
        "tradeType": tradeType,
        "symbol": symbol,
        "side":side,
        "orderId":orderId,
        "clOrdId":clOrdId,
        "pageNum": pageNum,
        "pageSize": pageSize}
    res = requests.get(url=tradeurl + path, params=params, headers=headers).json()
    return res


if __name__ == '__main__':
    #print(futures_transfer(fromAccountType='funding', toAccountType='futures', currency='USDT', amount='200'))
    print(futures_openOrders(tradeType=tradeType,symbol=symbol))
    print(futures_position(tradeType,symbol,marginType))
