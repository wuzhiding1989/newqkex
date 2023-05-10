import copy
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhNzdmYzA1Yi1mN2U2LTRhZjgtYTBhMS01N2UyYjZkMjAwNmIxOTU2OTY1OTAzIiwidWlkIjoiT3dBa05jdFk5R1Jpcy9GekJaY2RkQT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJkRmxJM3RwSFdJdHpsNk9rTDRBSlBRPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4MzY5ODc0MiwiZXhwIjoxNjgzNzg1MTQyLCJpc3MiOiJ3Y3MifQ.FMdGkko4zQPKqJ7KAOGrWe16XbZukV7I8hyNcx2vrV4'
Authorization1='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjMWQ0YmU4OC1kMTA4LTRjYmYtYjE4Ny00MzdmOWFmZGNjMzE4MDc2NDg0NzkiLCJ1aWQiOiJsN1ZkOHlLTCswQWxXcUU5TWJXcmpBPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6ImRGbEkzdHBIV0l0emw2T2tMNEFKUFE9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjgzMzQ0NzQ1LCJleHAiOjE2ODM0MzExNDUsImlzcyI6IndjcyJ9.WxpT2f6vHMazjm7EYsdcN4k20lIwl8KnsqoZ39GC4Go'
headers['X-Authorization']=Authorization
url = 'http://13.215.135.141'
account='10081@qq.com'
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
    path = f'/otc/pendings/{orderid}/paid'
    parms = {'payment': payment}
    res = requests.put(url=url+path,headers=headers,data=parms).json()
    return res

#确认收款并放币/otc/pendings/940/complete
def otc_pendings_complete(orderid=None,googleVerifyCode=None,tradePassword=None):
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
def otc_orders(amount=None,side=None,quote=None,base=None,price=None):
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
           "notes":"瑞士是一个位于欧洲中部的联邦制国家，其历史可以追溯到公元前1世纪。以下是有关瑞士的一些基本信息：\n\n历史：早在公元前1世纪的罗马帝国时期，瑞士境内就已有人居住。1291年，三个山区小州——乌里、施维茨和下瓦尔登组成了原始的瑞士联邦。之后，瑞士陆续加入了其他州和城市，并在1848年颁布宪法。现今的瑞士政治体制为联邦制，由26个州组成。\n\n国土面积：瑞士国土面积约41,285平方千米，位于阿尔卑斯山脉中心地带。\n\n人口：截至2021年，瑞士人口约为8,673,000人。瑞士拥有四种官方语言，分别是德语、法语、意大利语和罗曼什语。\n\nGDP：根据国际货币基金组织（IMF）发布的数据，2019年瑞士的GDP总量为7090亿美元，是全球最富有的国家之一。该国以服务业和制造业为主要经济支柱，其中银行和金融业是瑞士最重要的产业之一。\n\n总体而言，瑞士历史悠久、文化多元，经济发达，同时保持着良好的社会秩序和治安环境。它是一个非常受欢迎的旅游目的地，吸引着数百万游客前来观光、滑雪、品尝当地美食等。",
           "payType":[5]
           }
    res = requests.post(url=url+path,headers=headers,json=params).json()
    #print(res.json())
    return  res
#查询我的广告/otc/orders?status=1
def otc_orders_ads_select():
    path = '/otc/orders?status=1'
    res = requests.get(url=url+path,headers=headers).json()
    return res

def otc_orders_adsid(id):
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

if __name__ == '__main__':
    #cachedParams = {'symbol':'BTC', }
    #print(exchange_assets())
    # print(orders(symbol='BTC_USDT',systemOrderType='limit',side='buy',volume=0.01,price=1003,source='web'))
    print(exchange_exchange_set('QQ'))
    #print(exchange_convert(baseSymbol='ABC',quoteSymbol='USDT',amount=2090))
    #print(otc_PublicOrde)rs(amount=None,payType=None,symbol='BTC',legalSymbol='USD',side='buy',page=1,pageSize=1000))