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
    tradingAccount=user.web_tradingAccount()#资金查询
    #print(user.web_tradingAccount())
    print('资产接口',tradingAccount)
    available=user.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)#划转
    print('划转接口',available)
    se=user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='20000', priceType=priceType, orderQty=1, postOnly=postOnly, timeInForce=timeInForce)#下单
    op=user.web_position(tradeType=tradeType)
    print('持仓接口',op)
    print('下单接口',se)
    w=user.web_openOrders(tradeType=tradeType) #当前委托
    ws=user.web_orders_history(tradeType=tradeType)
    clo=user.web_position_closed(tradeType=tradeType)
    fle=user.web_orders_fills(tradeType=tradeType)
    zij=user.web_account_income(tradeType=tradeType)
    print('历史成交接口', fle)
    print('历史资金接口', zij)
    print('历史委托接口', ws)
    print('历史仓位接口', clo)
    id=w['data']['list'][0]['orderId']
    print('当前委托接口',w)
    print(id)
    cl=user.web_orders_cancel(tradeType=tradeType,orderId=id,symbol=symbol)#撤单
    print('撤单接口',cl)
    # user=wb.webapi(2,'test')


if __name__ == '__main__':
    print(order_ad())