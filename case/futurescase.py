symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce='GTC'
fromAccountType='funding';toAccountType='futures';currency='USDT';amount=20
from BU.futures.api import webapi as wb



def order_ad():
    tradingAccount=wb.web_tradingAccount()
    print(tradingAccount)
    available=wb.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)
    print(available)
    se=wb.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='20000', priceType=priceType, orderQty=1, postOnly=postOnly, timeInForce=timeInForce)
    print(se)

if __name__ == '__main__':
    print(order_ad())