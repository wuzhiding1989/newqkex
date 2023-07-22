import copy
import json

import requests
from werkzeug.sansio.multipart import MultipartEncoder

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
headers1 = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
stoken="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4M2EzMTQzMy05Zjg4LTQ2NjEtYmM3NC04NzdiNDg2MjRlNjkxODEwMTUwODk0IiwidWlkIjoiT3dBa05jdFk5R1Jpcy9GekJaY2RkQT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJRbXM0VVlDZmVNNHNVdkh3L1UvWHRnPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4OTU4NDUxNywiZXhwIjoxNjg5NjcwOTE3LCJpc3MiOiJ3Y3MifQ.qHmZUt2x20BaDN_1IJLT2U6u5GFgecNAnPo_KdFZDh8"
ytoken='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzZTRkMDM3Mi00NmE1LTQyYjAtODA4ZC1hMTQyOTAzZjA4YmIxODAxNTkyMTU5IiwidWlkIjoiaDBsVXZiR0t2SkdkdGVscGYxQWRZUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJRbXM0VVlDZmVNNHNVdkh3L1UvWHRnPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4OTU4NDcxMCwiZXhwIjoxNjg5NjcxMTEwLCJpc3MiOiJ3Y3MifQ.ea0UoJRePl6BZVb4qfbTlWOHoOm2PyHYXIeFRiC_hGI'
headers['X-Authorization']=stoken
headers1['X-Authorization']=ytoken
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
def otc_pending(orderId,amount=None,googleVerifyCode=None,tradePassword=None):
    newheaders = copy.deepcopy(headers1)
    newheaders['Content-Type'] = 'application/x-www-form-urlencoded'
    path = '/otc/pendings'
    params = {
        'orderId':orderId,
        'amount':amount,
        'googleVerifyCode':googleVerifyCode,
        'tradePassword':tradePassword,
        'cachedParams': "[object Object]"
    }
    print(params)
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
    # print(type(parms))
    # print(url+path,headers,parms)
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
    headers['X-Authorization'] = stoken
    path = f'/otc/pendings/{orderid}/complete'
    parms={
        'pendingId': orderid,
        'tradePassword': tradePassword,
        'googleVerifyCode': googleVerifyCode
    }
    res = requests.put(url=url+path,headers=headers,params=parms).json()
    return res
#确认收款并放币/otc/pendings/940/complete
def otc_pendings_complete01(orderid=None,googleVerifyCode=None,tradePassword=None,headers=None):
    # headers['Content-Type'] = "multipart/form-data; boundary=----WebKitFormBoundaryDPGBW7MuZLcAyCfJ"
    # headers['X-Authorization'] = Authorization
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

def otc_orders_computeMax():
    path = f'/otc/orders/computeMax?symbol=BTC&legalSymbol=USD&side=sell'
    res = requests.get(url=url+path,headers=headers).json()
    return res
def otc_orders_adsid(id):#根据广告id查询广告订单
    path = f'/otc/orders/{id}'
    res = requests.get(url=url+path,headers=headers).json()
    return res
def otc_bill(page=None,pageSize=None,symbol=None,type=None):#查询otc流水
    path = '/otc/bill'
    parms = {'page': page,'pageSize': pageSize,'symbol': symbol,'type':type}
    res = requests.get(url=url+path,headers=headers,params=parms).json()
    return res

def user_kyc():
    path = '/user/kyc/info/save'
    parms={"firstName":"test1235","lastName":"123431","cardType":"id_card",
           "cardNumber":"32456754324","birthDay":1688524084873,"countryCode":"660",
           "frontImg":"20230705/1688524193228.","backImg":"20230705/1688524195448.",
           "handsImg":"20230705/1688524202756."}
    res = requests.post(url=url+path,json=parms,headers=headers).json()
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
    print(otc_orders_computeMax())
    #print(exchange_convert(baseSymbol='ABC',quoteSymbol='USDT',amount=2090))
    #print(otc_PublicOrde)rs(amount=None,payType=None,symbol='BTC',legalSymbol='USD',side='buy',page=1,pageSize=1000))
    # print(otc_orders(amount="0.10000000",side="sell",base="BTC",quote="USD",price="30000.00000000",payType=[3]))
    # a=otc_bill(page=1,pageSize=1000,symbol='USDT')
    # print(len(a['data']['bills']))
    # print(a)
    # for tmp in a['data']['bills']:
    #     print(tmp)
