symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'positionSide'
postOnly = 'false';reduceOnly = 'false';orderType = 'limit';priceType = 'optimalN';pageNum = '1';pageSize = '10';timeInForce='GTC'
from BU.futures.api import webapi as wb



def order_ad():
    se=wb.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='20000', priceType=priceType, orderQty=3, postOnly=postOnly, timeInForce=timeInForce)
    print(se)

if __name__ == '__main__':
    print(order_ad())