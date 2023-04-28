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
def otc_tickers_rate(symbol,quote):#未完成，待续
    res = webapi.otc_tickers()
    res2 = webapi.otc_rate()
    rate = res2['data'][f'USD_{quote}']
    print(rate)
    res1 = res['data']
    if symbol!='USDT':
        for tmp in res1:
            if tmp['symbol'] == symbol:
                ccc=tmp['last']
                return ccc
    else:
        usdt_cc=1
        return usdt_cc
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

def openapi_order_History(pairCode,id=None):
    res = api.fulfillment(pairCode=pairCode,isHistory=True,systemOrderType=0)
    print(res)
    fle = {'dealQuoteAmount': '0', 'averagePrice': '9'}
    for tmp in res:
        if tmp['id']==id:
            fle['averagePrice']=tmp['averagePrice']
            fle['dealQuoteAmount']=tmp['dealQuoteAmount']
            return fle



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
    #print(login_email('yonghu001@testcc.com','q123456'))
    #print(exchange_fee(pairCode='ABF_USDT'))
    p=openapi_order_History(pairCode='ABF_USDT',id=171784369092672)
    print(p)
    print(d('23456'))

