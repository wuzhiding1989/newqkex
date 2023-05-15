symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce='GTC'
fromAccountType='funding';toAccountType='futures';currency='USDT';amount=20
from BU.futures.api import webapi as wb
from common import util as ut



def order_ad():
    '''一键平仓、撤单
    当前资金、订单、持仓查询
    历史资金、订单、持仓查询'''
    # tradingAccount=wb.web_tradingAccount()
    # print(tradingAccount)
    # available=wb.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)
    # print(available)
    # se=wb.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
    #               marginType=marginType, price='20000', priceType=priceType, orderQty=1, postOnly=postOnly, timeInForce=timeInForce)
    # print(se)
    # w=wb.web_openOrders(tradeType=tradeType) #当前委托
    # id=w['data']['list'][0]['orderId']
    # print(w)
    # print(id)
    # cl=wb.web_orders_cancel(tradeType=tradeType,orderId=id,symbol=symbol)#撤单
    # print(cl)
    print(wb.web_position(tradeType, symbol, marginType))
    ac=ut.login_email('y005@cc.com','q123456')
    print(ac)

if __name__ == '__main__':
    print(order_ad())