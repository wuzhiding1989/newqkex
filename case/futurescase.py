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
    print(11,tradingAccount['code'])
    #print(user.web_tradingAccount()
    if tradingAccount['code'] !='0':
        print('获取c2c订单列表失败，原因：',tradingAccount['msg'])
        return False
    if tradingAccount['code'] != '0':
        raise Exception(f"web_tradingAccount() failed with error code {tradingAccount['code']}: {tradingAccount['msg']}")
    else:
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
    Close=user.web_orders_oneClickClose(tradeType=tradeType,symbol=symbol)
    print('一键撤单',Close)
    # user=wb.webapi(2,'test')

def order_ad1():
    '''一键平仓、撤单
    当前资金、订单、持仓查询
    历史资金、订单、持仓查询'''
    user = wb.webapi(2, 'test')
    tradingAccount=user.web_tradingAccount()#资金查询
    if tradingAccount['code'] != '0':
        print(f"web_tradingAccount() failed with error code {tradingAccount['code']}: {tradingAccount['msg']}")
        return
    else:
        print('资产接口',tradingAccount)
        if 'currency' not in tradingAccount['data'][0] or 'marginEquity' not in tradingAccount['data'][0]:
            print("Error: tradingAccount response does not contain 'currency' or 'marginEquity' field")
            return
    available=user.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)#划转
    if available['code'] != '0':
        print(f"web_transfer() failed with error code {available['code']}: {available['msg']}")
        return
    else:
        print('划转接口',available)
    se=user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='20000', priceType=priceType, orderQty=1, postOnly=postOnly, timeInForce=timeInForce)#下单
    if se['code'] != '0':
        print(f"web_order() failed with error code {se['code']}: {se['msg']}")
        return
    else:
        print('下单接口',se)
    op=user.web_position(tradeType=tradeType)
    if op['code'] != '0':
        print(f"web_position() failed with error code {op['code']}: {op['msg']}")
        return
    else:
        print('持仓接口',op)
    w=user.web_openOrders(tradeType=tradeType) #当前委托
    if w['code'] != '0':
        print(f"web_openOrders() failed with error code {w['code']}: {w['msg']}")
        return
    else:
        print('当前委托接口',w)
    ws=user.web_orders_history(tradeType=tradeType)
    if ws['code'] != '0':
        print(f"web_orders_history() failed with error code {ws['code']}: {ws['msg']}")
        return
    else:
        print('历史委托接口', ws)
    clo=user.web_position_closed(tradeType=tradeType)
    if clo['code'] != '0':
        print(f"web_position_closed() failed with error code {clo['code']}: {clo['msg']}")
        return
    else:
        print('历史仓位接口', clo)
    fle=user.web_orders_fills(tradeType=tradeType)
    if fle['code'] != '0':
        print(f"web_orders_fills() failed with error code {fle['code']}: {fle['msg']}")
        return
    else:
        print('历史成交接口', fle)
    zij=user.web_account_income(tradeType=tradeType)
    if zij['code'] != '0':
        print(f"web_account_income() failed with error code {zij['code']}: {zij['msg']}")
        return
    else:
        print('历史资金接口', zij)
    id=w['data']['list'][0]['orderId']
    cl=user.web_orders_cancel(tradeType=tradeType,orderId=id,symbol=symbol)#撤单
    if cl['code'] != '0':
        print(f"web_orders_cancel() failed with error code {cl['code']}: {cl['msg']}")
        return
    else:
        print('撤单接口',cl)
    Close=user.web_orders_oneClickClose(tradeType=tradeType,symbol=symbol)
    if Close['code'] != '0':
        print(f"web_orders_oneClickClose() failed with error code {Close['code']}: {Close['msg']}")


if __name__ == '__main__':
    print(order_ad1())