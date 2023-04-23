import copy
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzMjkzZDhiMi00MzA3LTQ4YjktODQ3ZS05MmVhOWFhZWJmMzE0MDcxMzQzNzUiLCJ1aWQiOiJ5YlRXQzNSU1VKbVhndkdJLzNWbFlnPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6IkE0akhmalBoeWxKbVJWa2VubTdmRWc9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjc5NTY4NTQ0LCJleHAiOjE2Nzk2NTQ5NDQsImlzcyI6IndjcyJ9.005ekNPToC9T-7tD0QksQt0sUx-ADexnOD47Ryd45mQ'
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

#单个撤单
'http://13.215.135.141/exchange/BTC_USDT/orders/167356484372496'
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
def pending(orderId,amount,price,googleVerifyCode=None,tradePassword=None):

    newheaders = copy.deepcopy(headers)
    newheaders['Content-Type'] = 'application/x-www-form-urlencoded'
    path = '/otc/pendings'
    params = {
        'orderId':orderId ,
        'amount':amount ,
        'price':price,
        'googleVerifyCode':googleVerifyCode,
        'tradePassword':tradePassword
    }
    res = requests.post(url=url+path,data=params,headers=newheaders).json()
    return res
#获取c2c广告信息
def otcPublicOrders(amount=None,payType=None,symbol=None,legalSymbol=None,side=None,page=None,pageSize=None):
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


if __name__ == '__main__':
    cachedParams = {'symbol':'BTC', }
    # print(login(account,password,verifyCode))
    # print(orders(symbol='BTC_USDT',systemOrderType='limit',side='buy',volume=0.01,price=1003,source='web'))
    # print(pending())
    print(otcPublicOrders(amount=None,payType=None,symbol='BTC',legalSymbol='USD',side='buy',page=1,pageSize=1000))
