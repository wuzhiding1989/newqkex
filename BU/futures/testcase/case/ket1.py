from BU.futures.api import webapi as wb
import random,time, threading
from  common import util as ut
from  BU.futures.testcase.case import ket3
symbol =ket3.symbol;tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long';name='eth_usdt'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum ='1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(ket3.us,'test')

def get_open_orders():
    w = user.web_openOrders(tradeType=tradeType,symbol=symbol,pageNum=1,pageSize=100)  # 当前委托
    id_list = [d['orderId'] for d in w['data']['list']]
    print('当前订单总数为：',w['data']['totalSize'])
    #print(id_list)
    return id_list

def buy_open_orders2(nex):
    w = user.web_openOrders(tradeType=tradeType,symbol=symbol,pageNum=1,pageSize=100,side='buy')  # 当前委托
    pri = ket3.getSpotList(symbol, ne=3)
    pri1=pri-nex
    print('买盘超过盘口价格将会被撤销掉，价格为',pri1)
    iid_list = [d['orderId'] for d in w['data']['list'] if float(d['price'] )> pri1]
    #print('当前订单总数为：',w['data']['totalSize'])
    #print(id_list)
    return iid_list
def sell_open_orders2(nex):
    w = user.web_openOrders(tradeType=tradeType,symbol=symbol,pageNum=1,pageSize=100,side='sell')  # 当前委托
    pri = ket3.getSpotList(symbol, ne=3)
    pri1=pri+nex
    print('卖盘超过盘口价格将会被撤销掉，价格为',pri1)
    iid_list = [d['orderId'] for d in w['data']['list'] if float(d['price'] )< pri1]
    #print('当前订单总数为：',w['data']['totalSize'])
    #print(id_list)
    return iid_list


def orders_cancel(nex):
    try:
        a = buy_open_orders2(nex=nex)
        b = sell_open_orders2(nex=nex)
        print('撤销订单为',a,'--',b)

        if a:
            for order_id in a:
                a=user.web_orders_cancel(tradeType=tradeType, orderId=order_id, symbol=symbol)
                print(a)

        if b:
            for order_id in b:
                aa=user.web_orders_cancel(tradeType=tradeType, orderId=order_id, symbol=symbol)
                print(aa)

    except Exception as e:
        print('Error:', e)
def clorder():
    try:
        id=get_open_orders()
        leng=len(id)
        ax=random.randint(4,5)
        x=max(int(leng)/ax,1)
        print(ax,x)
        result=random.sample(id,int(x))
        print('当前撤单的数量为',int(x),result)
        for a in result:
            a=user.web_orders_cancel(tradeType=tradeType, orderId=a, symbol=symbol)  # 撤单
            print(a)
    except Exception as e:
        print('Error:', e)
if __name__ == '__main__':
    #print(orders_cancel(nex=0.01))
    # print(orderid1())
    for i in range(10000):
        print(clorder())
        #print(orders_cancel(nex=0.013))
        time.sleep(10)
