from BU.futures.api import webapi as wb
import random,time, threading
from  common import util as ut
symbol = 'ETHUSDT';tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(5,'test')

def orderid1():
    orderid = []
    w = user.web_openOrders(tradeType=tradeType,symbol=symbol,pageNum=1,pageSize=100)  # 当前委托
    id_list = [d['orderId'] for d in w['data']['list']]
    orderid.extend(id_list)
    return orderid
def clorder():
    id=orderid1()
    leng=len(id);
    x=float(leng)/3
    result=random.sample(id,int(x))
    print(result)
    for a in result:
        cl = user.web_orders_cancel(tradeType=tradeType, orderId=a, symbol=symbol)  # 撤单
if __name__ == '__main__':
    # print(kte())
    # print(orderid1())
    for i in range(1000):
        print(clorder())
        time.sleep(3)
