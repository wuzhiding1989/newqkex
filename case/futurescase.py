symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce='GTC'
fromAccountType='funding';toAccountType='futures';currency='USDT';amount=20
from BU.futures.api import webapi as wb
from common import util as ut



def order_ad():
    '''一键平仓、撤单
    当前资金、订单、持仓查询
    历史资金、订单、持仓查询'''
    user = wb.webapi(2, 'test')
    #tradingAccount=user.web_tradingAccount()#划转域名需要检查
    print(user.web_position(tradeType, symbol, marginType))
    #print(user.web_tradingAccount())
    #print(tradingAccount)
    available=user.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)
    print(available)
    se=user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='20000', priceType=priceType, orderQty=1, postOnly=postOnly, timeInForce=timeInForce)
    print(se)
    w=user.web_openOrders(tradeType=tradeType) #当前委托
    id=w['data']['list'][0]['orderId']
    print(w)
    print(id)
    cl=user.web_orders_cancel(tradeType=tradeType,orderId=id,symbol=symbol)#撤单
    print(cl)
    # user=wb.webapi(2,'test')


if __name__ == '__main__':
    print(order_ad())