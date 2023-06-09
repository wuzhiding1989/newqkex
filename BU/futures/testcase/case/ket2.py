from BU.futures.api import webapi as wb
import random,time
symbol = 'ETHUSDT';tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(5,'test')

def sidess2():
    d = round(random.uniform(1, 5))
    a=user.tickpre()
    pri=a['data'][1][3]
    swq=random.randint(0,1)
    if swq == 0 :
        se1 = user.web_order(tradeType=tradeType, symbol=symbol, side='buy', positionSide='long',
                                    orderType=orderType,
                                    reduceOnly=reduceOnly,
                                    marginType=marginType, price=pri, priceType=priceType, orderQty=d, postOnly=postOnly,
                                    timeInForce=timeInForce)  # 下单
        se2 = user.web_order(tradeType=tradeType, symbol=symbol, side='sell', positionSide='short',
                                    orderType=orderType,
                                    reduceOnly=reduceOnly,
                                    marginType=marginType, price=pri, priceType=priceType, orderQty=d, postOnly=postOnly,
                                    timeInForce=timeInForce)  # 下单
        print(se2)
    else:
        se1 = user.web_order(tradeType=tradeType, symbol=symbol, side='sell', positionSide='short',
                             orderType=orderType,
                             reduceOnly=reduceOnly,
                             marginType=marginType, price=pri, priceType=priceType, orderQty=d, postOnly=postOnly,
                             timeInForce=timeInForce)  # 下单
        se2 = user.web_order(tradeType=tradeType, symbol=symbol, side='buy', positionSide='long',
                             orderType=orderType,
                             reduceOnly=reduceOnly,
                             marginType=marginType, price=pri, priceType=priceType, orderQty=d, postOnly=postOnly,
                             timeInForce=timeInForce)  # 下单
        print(se2)
if __name__ == '__main__':
    for i in range(500):
        print(sidess2())
        time.sleep(10)