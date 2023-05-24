import copy
import json

import requests
from werkzeug.sansio.multipart import MultipartEncoder

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2OWE4M2EyNS1mZDdkLTQ0YjMtOWVmMi1iYWY0NTQ2YThkYmQyMDE1NjYwNTQyIiwidWlkIjoieUdxdFQwbzMvZmdwN08wRlcvR1pZQT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJXWU5oVGYvdXNWUkFQb3BFenpra0RnPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4NDgxMzc3NSwiZXhwIjoxNjg0OTAwMTc1LCJpc3MiOiJ3Y3MifQ.zEQVXWWqnqbwtYlVBSU40ZxJpNB5mvS7WLBgr09e8TE'
Authorization1='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyYTJmZjgzOC1iZjY3LTQ5ZjktYjA0Ny03MGE2ODU0NzQzNGYzNTIwMDQ2NDMiLCJ1aWQiOiJWbDhaZ3lJWWkxZ2w1L1BDRjE1RlN3PT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6ImpwTE9wdlFUMzF1djJyNlo3S0FjeFE9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjg0MzE5MDcwLCJleHAiOjE2ODQ0MDU0NzAsImlzcyI6IndjcyJ9.9VTdrYJZbrgpZ0rNWWXobKuGQZT1nNDKEsa3lB9_4h8'
headers['X-Authorization']=Authorization
url = 'https://test-public-rest.qkex.com'
account='12345678@qq.com'
password='aa123456'
verifyCode='111111'

#登录
def login(account,password,verifyCode):
    email(account)
    params = {
        'account':account,
        'password':password,
        'verifyCode':verifyCode

    }
    path='/user/login'
    res =requests.post(url=url+path,json=params,headers=headers).json()
    return res

#登录时获取邮箱验证码
def email(email):
    params={
        "type": 3,
        "email": email,
        "countdownType": "signinEmail"}
    path='/user/send-code/email'
    res = requests.post(url=url+path,json=params,headers=headers).json()
    return res

#下单
def orders(**kwargs):
    # params = {
    #     'systemOrderType':systemOrderType,
    #     'side':side,
    #     'price':price,
    #     'volume':volume,
    #     'source':source,
    #     'quoteVolume':0
    # }
    symbol = kwargs['symbol']
    params = {}
    if kwargs != None:
        for tmp in kwargs:
            params[tmp] = kwargs[tmp]
    path = f'/exchange/{symbol}/orders'
    res = requests.post(url=url+path,json=params,headers=headers).json()
    return res

#查现货余额
def exchange_assets():
    path = '/exchange/assets'
    res = requests.get(url=url+path,headers=headers).json()
    return res

#单个撤单'http://13.215.135.141/exchange/BTC_USDT/orders/167356484372496'
def cancelorder(symbol=None,orderid=None):
    path = f'/exchange/{symbol}/orders/{orderid}'
    res = requests.delete(url=url + path, headers=headers).json()
    return res



#获取深度信息
def orderBook(symbol=None):
    path =f'/exchange/public/{symbol}/orderBook'
    res = requests.get(url=url+path,headers=headers).json()
    return res


#查看当前委托
def openOrders(page=None,pageSize=None,pairCode=None):
    params = {
        'page':page,
        'pageSize':pageSize,
        'pairCode':pairCode
    }
    path = '/exchange/orders'
    res = requests.get(url=url + path, json=params, headers=headers).json()
    return res

#查看历史委托
def hisOrders(page=None,pageSize=None,symbol=None):
    params = {
        'page': page,
        'pageSize': pageSize

    }
    path = f'/exchange/{symbol}/fulfillment'
    res = requests.get(url=url + path, json=params, headers=headers).json()
    return res

#账户划转
def wallet_transfer(_from=None,to=None,symbol=None,currency=None,pairCode=None):
    params = {"from": _from, "to": to, "symbol": symbol, "currency":currency, "pairCode": pairCode,
     "amount": "1"}
    path = '/wallet/transfer'
    res = requests.get(url=url + path, json=params, headers=headers).json()
    return res

#c2c下单
def otc_pending(orderId,amount,price,googleVerifyCode=None,tradePassword=None):
    newheaders = copy.deepcopy(headers)
    newheaders['Content-Type'] = 'application/x-www-form-urlencoded'
    path = '/otc/pendings'
    params = {
        'orderId':orderId,
        'amount':amount,
        'price':price,
        'googleVerifyCode':googleVerifyCode,
        'tradePassword':tradePassword
    }
    res = requests.post(url=url+path,data=params,headers=newheaders).json()
    return res

#用户c2c下单
def consumer_otc_pending(Authorization1,orderId,amount):
    # newheaders = copy.deepcopy(headers)
    headers['X-Authorization']=Authorization1
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    path = '/otc/pendings'
    params = {
        'orderId':orderId,
        'amount':amount,
        'cacheParams': "[object Object]",

    }
    res = requests.post(url=url+path,data=params,headers=headers).json()
    return res

#获取c2c广告信息
def otc_PublicOrders(amount=None,payType=None,symbol=None,legalSymbol=None,side=None,page=None,pageSize=None):
    #'http://13.215.135.141/otc/public/orders?amount=&payType=&symbol=USDT&legalSymbol=USD&side=sell&page=1&pageSize=1000'
    path = '/otc/public/orders'
    params = {
        'amount':amount,
        'payType':payType,
        'symbol':symbol,
        'legalSymbol':legalSymbol,
        'side':side,
        'page':page,
        'pageSize':pageSize
    }
    res = requests.get(url=url+path,params=params,headers=headers).json()
    return res

#我已付款/otc/pendings/940/paid
def otc_pendings_paid(orderid=None,payment=None):
    # headers['X-Authorization']=Authorization1
    headers['Content-Type']="application/x-www-form-urlencoded"
    path = f'/otc/pendings/{orderid}/paid'
    parms = {'payment': payment}
    res = requests.put(url=url+path,headers=headers,data=parms).json()
    return res
#我已付款/otc/pendings/940/paid
def consumer_otc_pendings_paid(Authorization1,orderid=None,payment=None):
    # newheaders = copy.deepcopy(headers)
    headers['Content-Type']="application/x-www-form-urlencoded"
    headers['X-Authorization']=Authorization1
    path = f'/otc/pendings/{orderid}/paid'
    parms = {'payment': payment}
    # request_data = MultipartEncoder(parms)
    # parms=json.dumps(parms)
    print(type(parms))
    print(url+path,headers,parms)
    res = requests.put(url=url+path,headers=headers,data=parms).json()
    return res
#用户-我的订单列表
def consumer_my_order(Authorization1,status,page,pageSize):

    # newheaders = copy.deepcopy(headers)
    # newheaders['X-Authorization']=Authorization1
    headers['X-Authorization']=Authorization1
    path = f'/otc/pendings'
    parms = {"status":status,"page":page,"pageSize":pageSize}
    res = requests.get(url=url + path, headers=headers, params=parms).json()
    return res

#确认收款并放币/otc/pendings/940/complete
def otc_pendings_complete(orderid=None,googleVerifyCode=None,tradePassword=None):
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['X-Authorization'] = Authorization
    path = f'/otc/pendings/{orderid}/complete'
    parms={
        'pendingId': orderid,
        'tradePassword': tradePassword,
        'googleVerifyCode': googleVerifyCode
    }
    res = requests.put(url=url+path,headers=headers,params=parms).json()
    return res

#http://13.215.135.141/user/detail 查询用户信息
def user():
    path = '/user/detail'
    res =requests.get(url=url+path,headers=headers).json()


#发布广告/otc/orders
def otc_orders(amount=None,side=None,quote=None,base=None,price=None,payType=None):
    path = '/otc/orders'
    params ={"side":side,
           "base":base,
           "quote":quote,
           "type":"limit",
           "floatingRate":0,
           "price":price,
           "amount":amount,
           "minAmount":"200.00000000",
           "maxAmount":"30000.00000000",
           "notes": "瑞士是",
           "payType":payType
           }
    res = requests.post(url=url+path,headers=headers,json=params).json()
    #print(res.json())
    return  res
#查询我的广告/otc/orders?status=1
def otc_orders_ads_select():
    path = '/otc/orders?status=1'
    res = requests.get(url=url+path,headers=headers).json()
    return res

def otc_orders_adsid(id):#根据广告id查询广告订单
    path = f'/otc/orders/{id}'
    res = requests.get(url=url+path,headers=headers).json()
    return res

#http://13.215.135.141/otc/pendings/1179/cancel 取消otc订单
def otc_cancel(id):
    path =f'/otc/pendings/{id}/cancel'
    res = requests.delete(url=url+path,headers=headers).json()
    print(url+path)
    return res

#根据币种获取otc资产
def otc_assets_symbol():
    path = '/otc/assets'
    res = requests.get(url=url+path,headers=headers).json()
    return res
#获取币种价格
def otc_tickers():
    path = '/foundation/indexes/tickers'
    res = requests.get(url=url+path,headers=headers).json()
    return res
#获取汇率
def otc_rate():
    path = '/foundation/indexes/exchange-rate'
    res = requests.get(url=url + path, headers=headers).json()
    return res

#/exchange/public/currencies
def exchange_currencies():
    path = '/exchange/public/currencies'
    res = requests.get(url=url + path, headers=headers).json()
    return res
#/exchange/exchange_set/{symbol}币种兑换配置
def exchange_exchange_set(symbol):
    path = f'/exchange/exchange_set/{symbol}'
    res = requests.get(url=url+path ,headers=headers).json()
    return res
def exchange_convert(baseSymbol,quoteSymbol,amount,googleVerifyCode):
    path = '/exchange/exchange'
    parpms={
    'baseSymbol': baseSymbol,
    'quoteSymbol': quoteSymbol,
    'googleVerifyCode':googleVerifyCode,
    'amount': amount
    }
    res =requests.post(url=url+path,json=parpms,headers=headers).json()
    return res

def otc_reject():
    #https://test-public-rest.qkex.com/otc/pendings/1964/reject
    pass

if __name__ == '__main__':
    #cachedParams = {'symbol':'BTC', }
    # print(login(account='y005@cc.com',password='q123456',verifyCode='111111'))
    # print(orders(symbol='BTC_USDT',systemOrderType='limit',side='buy',volume=0.01,price=1003,source='web'))
    #print(exchange_exchange_set('QQ'))
    #print(exchange_convert(baseSymbol='ABC',quoteSymbol='USDT',amount=2090))
    #print(otc_PublicOrde)rs(amount=None,payType=None,symbol='BTC',legalSymbol='USD',side='buy',page=1,pageSize=1000))
    # print(otc_orders(amount="0.10000000",side="sell",base="BTC",quote="USD",price="30000.00000000",payType=[3]))
    print(consumer_otc_pendings_paid(orderid="1910",payment="403"))
