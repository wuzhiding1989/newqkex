from BU.futures.api import webapi as wb
import random,time, threading,requests
from  common import util as ut
from BU.futures.testcase import wsstestfutures as ws
symbol = 'ETHUSDT';tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(5,'test')
def sidess():
    sides = ['buy','sell']
    tmp = random.choice(sides)
    d = round(random.uniform(1, 10))
    pri = tipicer()
    if tmp == 'buy':
        positionSide = 'long'
        pri1=pri-3
        pri2=pri-20
        price = round(random.uniform(pri1,pri2), 2)
        se = user.web_order(tradeType=tradeType, symbol=symbol, side=tmp, positionSide=positionSide,
                            orderType=orderType,
                            reduceOnly=reduceOnly,
                            marginType=marginType, price=price, priceType=priceType, orderQty=d, postOnly=postOnly,
                            timeInForce=timeInForce)  # 下单
    else:
        positionSide = 'short'
        pri1=pri+3
        pri2=pri+20
        price = round(random.uniform(pri1, pri2), 2)
        se = user.web_order(tradeType=tradeType, symbol=symbol, side=tmp, positionSide=positionSide,
                            orderType=orderType,
                            reduceOnly=reduceOnly,
                            marginType=marginType, price=price, priceType=priceType, orderQty=d, postOnly=postOnly,
                            timeInForce=timeInForce)  # 下单
    if tmp == 'buy':
        positionSide = 'long'
        pri1=pri-3
        pri2=pri-20
        price = round(random.uniform(pri1,pri2), 2)
        se = user.web_order(tradeType=tradeType, symbol=symbol, side=tmp, positionSide=positionSide,
                            orderType=orderType,
                            reduceOnly=reduceOnly,
                            marginType=marginType, price=price, priceType=priceType, orderQty=d, postOnly=postOnly,
                            timeInForce=timeInForce)  # 下单
    else:
        positionSide = 'short'
        pri1=pri+3
        pri2=pri+20
        price = round(random.uniform(pri1, pri2), 2)
        se = user.web_order(tradeType=tradeType, symbol=symbol, side=tmp, positionSide=positionSide,
                            orderType=orderType,
                            reduceOnly=reduceOnly,
                            marginType=marginType, price=price, priceType=priceType, orderQty=d, postOnly=postOnly,
                            timeInForce=timeInForce)  # 下单
def orderid1():
    orderid = []
    w = user.web_openOrders(tradeType=tradeType,symbol=symbol,pageNum=1,pageSize=100)  # 当前委托
    id_list = [d['orderId'] for d in w['data']['list']]
    orderid.extend(id_list)
    return orderid
def clorder():
    id=orderid1()
    leng=len(id)
    x=float(leng)/2
    result=random.sample(id,int(x))
    print(result)
    for a in result:
        cl = user.web_orders_cancel(tradeType=tradeType, orderId=a, symbol=symbol)  # 撤单
        print(cl)
def tipicer():
    a=user.tickpre()
    cc=a['data'][1][3]
    return cc

if __name__ == '__main__':
    for i in range(2000):
        print(sidess())
        time.sleep(1)
