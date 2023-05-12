from common.googleCode import read_google_authenticator_code as goolgle
import requests
import copy
from BU.spot.api import webapi
import time,datetime,random
from decimal import *
import math
from common.mysql_san import mysql_select
from ws4py.client.threadedclient import WebSocketClient
from BU.spot.openapi import api


#获取买一卖一价 和数量
def price(symbol):
    orderbook = {'bid':[1000,1],'ask':[1001,2] }
    res = webapi.orderBook(symbol=symbol)
    if res['code'] !=0:
        print("获取买卖盘接口异常，异常原因：",res['msg'])
    orderbook['bid'][0] = res['data']['bids'][0][0]
    orderbook['bid'][1] = res['data']['bids'][0][1]
    orderbook['ask'][0] = res['data']['asks'][0][0]
    orderbook['ask'][1] = res['data']['asks'][0][1]
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
#获取OTC最新价格
def otc_tickers_rate(symbol,quote):
    res = webapi.otc_tickers()
    if symbol=='USDT' and quote =='USD':
        usdt_cc=1
        return usdt_cc
    elif symbol!='USDT' and quote =='USD':
        for tmp in res['data']:
            if tmp['symbol'] == symbol:
                ccc = tmp['last']
                return ccc
    elif symbol=='USDT' and quote !='USD':
        res2 = webapi.otc_rate()
        rate = res2['data'][f'USD_{quote}']
        if quote !='USD':
            return d(rate,2)
    else:
        res2 = webapi.otc_rate()
        rate = res2['data'][f'USD_{quote}']
        for tmp in res['data']:
            if tmp['symbol'] == symbol:
                ccc=tmp['last']
                ass= d(ccc) * d(rate)
                return d(ass,2)

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

#根据币种获取otc资产(可用和冻结）
def otc_assets_symbol(symbol):
    res =webapi.otc_assets_symbol()
    for tmp in res['data']:
        if tmp['symbol'] ==symbol:
            availableBalance = tmp['availableBalance']
            frozenBalance = tmp['frozenBalance']
            assets=str(d(availableBalance)),str(d(frozenBalance))
            return assets
def exchange_fee(pairCode=None):#获取现货手续费
    res=webapi.exchange_currencies()
    fee = {'makerFeesRate': 1000, 'tickerFeesRate': 1001 }
    for tmp in res['data']:
        if tmp['pairCode']==pairCode:
            fee['makerFeesRate']=tmp['makerFeesRate']
            fee['tickerFeesRate'] = tmp['tickerFeesRate']
            return fee
def exchange_assets_symbol(symbol):#打印现货单个资产的可用和不可用
    assets={'available':'','hold':''}
    res =webapi.exchange_assets()
    if res['code']==0:
        for tmp in res['data']:
            if tmp['symbol'] ==symbol:
                assets['available'] = tmp['available']
                assets['hold'] = tmp['hold']
                return assets
    else:
        print('请求失败，返回结果为',res)
        return
def openapi_order_History(pairCode,id=None):#open历史委托查询订单数据
    res = api.fulfillment(pairCode=pairCode,isHistory=True,systemOrderType=0)
    fle = {'dealAmount': '0', 'averagePrice': '0','amount': '0',
           'dealQuoteAmount': '0', 'side': '0', 'status': 1, 'openAmount': '0','entrustPrice': '0'}
    #print(res)
    for tmp in res:
        if tmp['id']==id:
            fle['averagePrice']=tmp['averagePrice']
            fle['dealAmount']=tmp['dealAmount']
            fle['amount'] = tmp['amount']
            fle['dealQuoteAmount'] = tmp['dealQuoteAmount']
            fle['side'] = tmp['side']
            fle['status'] = tmp['status']
            fle['openAmount'] = tmp['openAmount']
            fle['entrustPrice'] = tmp['entrustPrice']
            return fle
def openapi_order(pairCode,id=None):#open当前委托查询订单数据
    res = api.orders(pairCode=pairCode)
    fle = {'dealAmount': '0', 'averagePrice': '0','amount': '0',
           'dealQuoteAmount': '0', 'side': '0', 'status': 1, 'openAmount': '0','entrustPrice': '0'}
    print(res)
    for tmp in res:
        if tmp['id']==id:
            fle['averagePrice']=tmp['averagePrice']
            fle['dealAmount']=tmp['dealAmount']
            fle['amount'] = tmp['amount']
            fle['dealQuoteAmount'] = tmp['dealQuoteAmount']
            fle['side'] = tmp['side']
            fle['status'] = tmp['status']
            fle['openAmount'] = tmp['openAmount']
            fle['entrustPrice'] = tmp['entrustPrice']
            return fle
def openapi_order1(pairCode):#打印当前币对所有的当前委托订单
    res = api.orders(pairCode=pairCode)
    print(res)
    ids = [d['id'] for d in res if d['pairCode'] == pairCode]
    print(ids)
    return ids
def StampToTime(timeStamp,type=None):
    if not type:
        dateArray = datetime.datetime.fromtimestamp(int(str(timeStamp)[0:]))  # 获取创建时间戳,并转换
        time = dateArray.strftime("%Y-%m-%d %H:%M:%S")  # 时间再次转换
        return  time
    if type=='MicroSecond':
        dateArray = datetime.datetime.fromtimestamp(int(str(timeStamp)[0:-3]))  # 获取创建时间戳,并转换
        time = dateArray.strftime("%Y-%m-%d %H:%M:%S")  # 时间再次转换
        return  time


#登录获取headers带token，失败后继续重试，重试6次后退出---兼容邮件登录和谷歌登录，不用输谷歌key，输入账号和密码就可登录
def login_email(email,password):
    newheaders=copy.deepcopy(webapi.headers)
    sql = f"SELECT c.google_auth_flag,a.google_code FROM user_center.user_info a ,user_center.user_settings c WHERE a.id=c.user_id AND a.email='{email}'"
    cw = mysql_select(sql)
    google_auth_flag = cw[0][0];bind_google_code = cw[0][1]#获取账号的是否绑定谷歌和谷歌验证码
    for i in range(6):
        try:
            if google_auth_flag == 1:
                locode = goolgle(secret_key=bind_google_code)
                res = webapi.login(account=email,password=password,verifyCode=locode)
                token = res['data']['accessToken']
                newheaders['X-Authorization'] = token
                return newheaders
                break #终止循环
            else:
                res=webapi.login(account=email,password=password,verifyCode='111111')
                token = res['data']['accessToken']
                newheaders['X-Authorization'] = token
                return newheaders
                break
        except Exception as e:
            print('获取token失败,报错为',res['msg'],'2秒后自动重试')
            time.sleep(2)
    else:
        print('重试6次后，登录失败，请检查服务或配置信息')
        return

if __name__ == '__main__':
    # sa='q123456'
    print(login_email('y001@cc.com','q123456'))
    #print(otc_tickers_rate(symbol='BTC',quote='INR'))
    #p=exchange_assets_symbol('BTC')
    #q=openapi_order_History(pairCode='ADA_USDT',id=171960320359488)


