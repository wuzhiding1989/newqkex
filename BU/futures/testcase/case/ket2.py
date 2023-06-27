from BU.futures.api import webapi as wb
import random,time
from BU.futures.testcase.case import ket3
symbol =ket3.symbol;tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long';name='eth_usdt'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(ket3.us,'test')

def place_order(side, position_side, **kwargs):
    try:
        order = user.web_order(orderType=orderType, reduceOnly=reduceOnly,tradeType=tradeType,priceType=priceType,postOnly=postOnly, timeInForce=timeInForce,symbol=symbol,marginType=marginType, side=side, positionSide=position_side, **kwargs)
        print(order)
    except Exception as e:
        print('Error getting availPos:', e)
def sidess2():#成交控制
    try:
        d = round(random.uniform(1, 20))
        pri = float(ket3.getSpotList(symbol))
        swq = random.randint(0, 1)
        if swq == 1:
            place_order('buy', 'long', price=pri, orderQty=d)
            place_order('sell', 'short', price=pri, orderQty=d)
            place_order('buy', 'long', price=pri, orderQty=d)
            place_order('sell', 'short', price=pri, orderQty=d)
        else:
            place_order('sell', 'short', price=pri, orderQty=d)
            place_order('buy', 'long', price=pri, orderQty=d)
    except Exception as e:
        print('Error getting availPos:', e)

if __name__ == '__main__':
    for i in range(2000):
        print(sidess2())
        time.sleep(1)