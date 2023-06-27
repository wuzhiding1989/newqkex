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

def clorder():
    try:
        id=get_open_orders()
        leng=len(id)
        ax=random.randint(4,5)
        x=int(leng)/ax
        result=random.sample(id,int(x))
        print('当前撤单的数量为',int(x),result)
        for a in result:
            user.web_orders_cancel(tradeType=tradeType, orderId=a, symbol=symbol)  # 撤单
    except Exception as e:
        print('Error getting availPos:', e)
if __name__ == '__main__':
    #print(get_open_orders())
    # print(orderid1())
    for i in range(1000):
        print(clorder())
        time.sleep(1)
