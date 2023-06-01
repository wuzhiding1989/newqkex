symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'sell';marginType = 'cross';positionSide = 'short'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount=40;pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
from BU.futures.api import webapi as wb
from common import util as ut
import random,time
def order_ad(use,side,positionSide):
    '''一键平仓、撤单
    当前资金、订单、持仓查询
    历史资金、订单、持仓查询'''
    user = wb.webapi(use, 'test')
    tradingAccount=user.web_tradingAccount()#资金查询
    if tradingAccount['code'] != '0':
        print(f"web_tradingAccount() failed with error code {tradingAccount['code']}: {tradingAccount['msg']}")

    else:
        print('资产接口',tradingAccount)
        # if 'currency' not in tradingAccount['data'][0] or 'marginEquity' not in tradingAccount['data'][0]:
        #     print("Error: tradingAccount response does not contain 'currency' or 'marginEquity' field")
    tra=user.web_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount)
    if tra['code'] != 0:
        print(f"web_transfer() failed with error code {tra['code']}: {tra['msg']}")
    else:
        print('划转接口',tra)
    available=user.web_wallet_transfer(fromAccountType=fromAccountType,toAccountType=toAccountType,currency=currency,amount=amount,pairCode=pairCode,symbol=currency)#划转
    if available['code'] != 0:
        print(f"web_wallet_transfer() failed with error code {available['code']}: {available['msg']}")

    else:
        print('旧版本划转接口',available)
    se=user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=positionSide, orderType=orderType, reduceOnly=reduceOnly,
                  marginType=marginType, price='21842.21', priceType=priceType, orderQty=3, postOnly=postOnly, timeInForce=timeInForce)#下单
    if se['code'] != '0':
        print(f"web_order() failed with error code {se['code']}: {se['msg']}")

    else:
        print('下单接口',se)
    op=user.web_position(tradeType=tradeType)
    if op['code'] != '0':
        print(f"web_position() failed with error code {op['code']}: {op['msg']}")

    else:
        print('持仓接口',op)
    w=user.web_openOrders(tradeType=tradeType) #当前委托
    if w['code'] != '0':
        print(f"web_openOrders() failed with error code {w['code']}: {w['msg']}")

    else:
        print('当前委托接口',w)
        # if 'list' in w['data'] and len(w['data']['list']) > 0:
        #     id=w['data']['list'][0]['orderId']
        #     if id is not None:
        #         cl=user.web_orders_cancel(tradeType=tradeType,orderId=id,symbol=symbol)#撤单
        #         if cl['code'] != '0':
        #             print(f"web_orders_cancel() failed with error code {cl['code']}: {cl['msg']}")
        #             return
        #         else:
        #             print('撤单接口',cl)
    ws=user.web_orders_history(tradeType=tradeType)
    if ws['code'] != '0':
        print(f"web_orders_history() failed with error code {ws['code']}: {ws['msg']}")

    else:
        print('历史委托接口', ws)
    clo=user.web_position_closed(tradeType=tradeType)
    if clo['code'] != '0':
        print(f"web_position_closed() failed with error code {clo['code']}: {clo['msg']}")

    else:
        print('历史仓位接口', clo)
    fle=user.web_orders_fills(tradeType=tradeType)
    if fle['code'] != '0':
        print(f"web_orders_fills() failed with error code {fle['code']}: {fle['msg']}")

    else:
        print('历史成交接口', fle)
    zij=user.web_account_income(tradeType=tradeType)
    if zij['code'] != '0':
        print(f"web_account_income() failed with error code {zij['code']}: {zij['msg']}")

    else:
        print('历史资金接口', zij)

    Close=user.web_orders_oneClickClose(tradeType=tradeType,symbol=symbol)
    if Close['code'] != '0':
        print(f"web_orders_oneClickClose() failed with error code {Close['code']}: {Close['msg']}")

    # cll=user.web_oneClickClose(tradeType=tradeType,symbol=symbol)
    # if cll['code'] != '0':
    #     print(f"web_oneClickClose() failed with error code {cll['code']}: {cll['msg']}")
    # else:
    #     print('一键平仓',cll)
    print('查询档位深度接口',user.web_market_depth(tradeType=tradeType,gear=gear,symbol=symbol,limit=limit))
    print('查询行情简化信息接口',user.web_market_ticker_mini(tradeType=tradeType,symbol=symbol,limit=limit))
    print('查询行情接口',user.web_market_ticker_24hr(tradeType=tradeType, symbol=symbol, limit=limit))
    print('历史成交接口',user.web_market_trade(tradeType=tradeType, symbol=symbol, limit=limit))
    print('k线接口',user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit,period=period))
    lev=user.web_leverage(tradeType=tradeType,symbol=symbol,leverage=20,marginType=marginType)
    print('调整杠杆接口',lev)
    #stop=user.se

def order1(use):
    user = wb.webapi(use, 'test')
    buyaccprice = random.randint(26261, 26270);sellprice = random.randint(26271, 26280);acc=random.randint(2,7)
    #buy1=user.web_order(tradeType=tradeType, symbol=symbol, side='buy', positionSide='short', orderType=orderType, reduceOnly=reduceOnly,
                  # marginType=marginType, price=buyaccprice, priceType=priceType, orderQty=acc, postOnly=postOnly, timeInForce=timeInForce)#下单
    sell1=user.web_order(tradeType=tradeType, symbol=symbol, side='sell', positionSide='short', orderType=orderType, reduceOnly=reduceOnly,marginType=marginType, price=sellprice, priceType=priceType, orderQty=acc, postOnly=postOnly, timeInForce=timeInForce)#下单
    # print(1234,sell1['code'])
def order(use):
    user = wb.webapi(use, 'test')
    side1=['buy','sell']
    positionSide1=['long']
    price1=['20042.23','25000.34','21000.33']
    acc=random.randint(4,4);buyaccprice=random.randint(26261,26270);sellprice=random.randint(26271,26280)
    side=random.choice(side1);positionSide=random.choice(positionSide1);price=random.choice(price1)
    ak=user.web_market_depth(tradeType=tradeType,gear=gear,symbol=symbol,limit=limit)
    cc=ak['data']['bids'];cc2=ak['data']['asks']
    aa=[float(x[0]) for x in cc]
    aa1=[float(x[0]) for x in cc2]
    print('买盘盘口',cc2)
    print('卖盘盘口',cc)
    print(max(aa),min(aa1))
    aa123 = int(max(aa) - random.uniform(0.12, 0.92) * 10);aa124 = int(min(aa1) + random.uniform(0.12, 0.92) * 10)
    print(aa123,aa124)
    print('历史成交接口', user.web_market_trade(tradeType=tradeType, symbol=symbol, limit=limit))
    #print('k线接口1m',user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit,period='1m'))

    # print('k线接口5m', user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit, period='5m'))
    # print('k线接口15m', user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit, period='15m'))
    # print('k线接口30m', user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit, period='30m'))
    # ac1=(max(ak['data']['bids'], key=lambda x: float(x[1])))[0];ac2=ak['data']['asks'][-1][0]
    # # ac3=(min(cc, key=lambda x: float(x[-1])))
    # print(ac1,ac2)
    if random.randint(0,1)==0:
        se1=user.web_order(tradeType=tradeType, symbol=symbol, side='sell', positionSide='short', orderType=orderType, reduceOnly=reduceOnly,
                      marginType=marginType, price=aa123, priceType=priceType, orderQty=acc, postOnly=postOnly, timeInForce=timeInForce)#下单
        print(1,se1)
        se2=user.web_order(tradeType=tradeType, symbol=symbol, side='buy', positionSide='long', orderType=orderType, reduceOnly=reduceOnly,
                      marginType=marginType, price=aa124, priceType=priceType, orderQty=acc, postOnly=postOnly, timeInForce=timeInForce)#下单
        print(se2)
    else:
        se2 = user.web_order(tradeType=tradeType, symbol=symbol, side='buy', positionSide='long', orderType=orderType,
                             reduceOnly=reduceOnly,
                             marginType=marginType, price=aa124, priceType=priceType, orderQty=acc, postOnly=postOnly,
                             timeInForce=timeInForce)  # 下单
        print(2,se2)
        time.sleep(3)

        se1 = user.web_order(tradeType=tradeType, symbol=symbol, side='sell', positionSide='short', orderType=orderType,
                             reduceOnly=reduceOnly,
                             marginType=marginType, price=aa123, priceType=priceType, orderQty=acc, postOnly=postOnly,
                             timeInForce=timeInForce)  # 下单
        print(se1)
    #time.sleep(30)

def leverage_api():
    user = wb.webapi(5, 'test')
    post_leverage=user.web_leverage(tradeType=tradeType,symbol=symbol,leverage=34,marginType=marginType)
    print('调整杠杆接口',post_leverage)
    select_leverage = user.web_leverage_info(tradeType=tradeType,symbol=symbol,marginType=marginType)
    print('查询调整后的杠杆接口', select_leverage)
if __name__ == '__main__':
    user = wb.webapi(3, 'test')
    #print(order_ad(use=2,side='buy',positionSide='long'))
    #print(order1('5'))
    # a=26000+random.uniform(2.12,5.55)
    # aa = int(21000 + random.uniform(0.12, 0.92) * 10)
    # print(a,aa)
    for i in range(1):
        print(order(2))

        #print(order1(3))
    # lev=user.web_order(tradeType='linearPerpetual', symbol='BTCUSDT', side='sell', positionSide='long', orderType='stop-limit', reduceOnly=reduceOnly,
    #               marginType='cross', price=27887.3, priceType=priceType, orderQty=3, postOnly=postOnly, timeInForce=timeInForce)#下单
    # print(lev)
    # print(user.web_leverage_info(tradeType=tradeType,symbol=symbol,marginType=marginType))
    #print('历史成交接口',user.web_market_trade(tradeType=tradeType, symbol=symbol, limit=limit))


