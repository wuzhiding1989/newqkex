from BU.NTS.dataCheck.dataCheck import close_wear_no_pos
from BU.NTS.BasicData import BasicData
# from temp.Nts_Check_formula_owen import close_wear_Price
from BU.NTS.WebOrder import n_order
from common.asserts import responseCodeAssert as _assert
from common.util import request_http as req, truncate, printc, printl, d, requests, priceSpread, t as _t, \
    countCaseNumber, ModeCount
from BU.NTS.dataCheck.dataCheck import close_wear_Price
from BU.NTS.dataCheck.dataCheck import *
tradeType='linearPerpetual'
symbol='BTCUSDT'
orderType='limit'
marginType='cross'
module='最大下单数量限制'
currency='USDT'

def orderLongCheckLess(NTS,log_level=None):
    CommonName = '买入开多数量小于最大下单数量限制边界值测试'
    side = 'buy';positionSide = 'long'
    markPriceMap = makerprice(NTS)
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPrice = truncate((round(d(markPriceMap[symbol]) / 2,pricesize)),pricesize)
    maxOlumeLimit = check_olume_limit(NTS, symbol=symbol, side=side, positionSide=positionSide, price=markPrice)
    maxOlumeLimit = maxOlumeLimit - 1
    res = NTS.order(price=markPrice, orderQty=maxOlumeLimit, tradeType=tradeType, symbol=symbol, orderType=orderType,marginType=marginType, side=side, positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName,log_level);ModeCount(orderAssertResult,module+CommonName)
    if  orderAssertResult:
        orderId = res['data']['orderId']
        NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=orderId)
    return orderAssertResult



def orderLongCheckEqual(NTS,log_level=None):
    CommonName='买入开多数量等于最大下单数量限制边界值测试';
    side = 'buy';positionSide='long'
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate((round(d(markPriceMap[symbol]) / 2,pricesize)),pricesize)
    # res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    # ctVal = res['ctVal']
    # takerRate = res['takerRate']
    # leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    # balances = NTS.balances(currency=currency)['data'][0]['marginAvailable']
    # amount = cal.MaxOpenQty(avail=balances, side=side, orderPrice=markPrice, leverage=leverage, takerRate=takerRate,
    #                         ctVal=ctVal, bid1=0)

    maxOlumeLimit=check_olume_limit(NTS,symbol=symbol,side=side,positionSide=positionSide,price=markPrice)
    res = NTS.order(price=markPrice,orderQty=maxOlumeLimit,tradeType=tradeType,symbol=symbol,orderType=orderType,marginType=marginType,side=side,positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName, log_level);ModeCount(orderAssertResult,module+CommonName)
    if orderAssertResult:
        orderId=res['data']['orderId']
        NTS.orderCancel(tradeType=tradeType,symbol=symbol,orderId=orderId)
    return orderAssertResult



def orderLongCheckMore(NTS,log_level=None):
    CommonName = '买入开多数量大于最大下单数量限制边界值测试'
    side = 'buy';positionSide = 'long'
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate((round(d(markPriceMap[symbol]) / 2,pricesize)),pricesize)
    #
    # res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    # ctVal = res['ctVal']
    # takerRate = res['takerRate']
    # leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    # balances = NTS.balances(currency=currency)['data'][0]['marginAvailable']
    # amount = cal.MaxOpenQty(avail=balances, side=side, orderPrice=markPrice, leverage=leverage, takerRate=takerRate,
    #                         ctVal=ctVal, bid1=0)

    maxOlumeLimit = check_olume_limit(NTS, symbol=symbol, side=side, positionSide=positionSide, price=markPrice)
    maxOlumeLimit = maxOlumeLimit + 1
    res = NTS.order(price=markPrice, orderQty=maxOlumeLimit, tradeType=tradeType, symbol=symbol, orderType=orderType,marginType=marginType, side=side, positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1037', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName,log_level);ModeCount(orderAssertResult,module+CommonName)
    return orderAssertResult




def orderShortCheckEqual(NTS,log_level=None):
    bids = [['18000', '1000'], ['16000', '10']]
    bid1=bids[0][0]
    CommonName='卖出开空数量等于最大下单数量限制边界值测试';
    side = 'sell';positionSide = 'short'
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate(round(float(markPriceMap[symbol]) * 1.5, pricesize),pricesize)
    maxOlumeLimit = check_olume_limit(NTS, symbol=symbol, side=side, positionSide=positionSide, price=markPrice)

    res = NTS.order(price=markPrice, orderQty=maxOlumeLimit, tradeType=tradeType, symbol=symbol, orderType=orderType,marginType=marginType, side=side, positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName,log_level);ModeCount(orderAssertResult,module+CommonName)
    if orderAssertResult:
        orderId = res['data']['orderId']
        NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=orderId)
    return orderAssertResult

def orderShortCheckLess(NTS,log_level=None):
    bids = [['18000', '1000'], ['16000', '10']]
    bid1 = bids[0][0]
    CommonName='卖出开空数量小于最大下单数量限制边界值测试';
    side = 'sell';positionSide = 'short'
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate(round(float(markPriceMap[symbol]) * 1.5, pricesize),pricesize)
    #
    # res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    # ctVal = res['ctVal']
    # takerRate = res['takerRate']
    # leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    # balances = NTS.balances(currency=currency)['data'][0]['marginAvailable']
    # amount = cal.MaxOpenQty(avail=balances, side=side, orderPrice=markPrice, leverage=leverage, takerRate=takerRate,
    #                         ctVal=ctVal, bid1=bid1)
    maxOlumeLimit = check_olume_limit(NTS, symbol=symbol, side=side, positionSide=positionSide, price=markPrice)
    maxOlumeLimit = maxOlumeLimit - 1
    res = NTS.order(price=markPrice, orderQty=maxOlumeLimit, tradeType=tradeType, symbol=symbol, orderType=orderType,marginType=marginType, side=side, positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName,log_level);ModeCount(orderAssertResult,module+CommonName)
    if orderAssertResult:
        orderId = res['data']['orderId']
        NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=orderId)
    return orderAssertResult


def orderShortCheckkMore(NTS,log_level=None):
    bids = [['18000', '1000'], ['16000', '10']]
    bid1 = bids[0][0]
    CommonName='卖出开空数量大于最大下单数量限制边界值测试';
    side = 'sell';positionSide = 'short'
    pricesize=BD().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate(round(float(markPriceMap[symbol]) * 1.2, pricesize),pricesize)

    # res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    # ctVal = res['ctVal']
    # takerRate = res['takerRate']
    # leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    # balances = NTS.balances(currency=currency)['data'][0]['marginAvailable']
    # amount = cal.MaxOpenQty(avail=balances, side=side, orderPrice=markPrice, leverage=leverage, takerRate=takerRate,
    #                         ctVal=ctVal, bid1=bid1)
    maxOlumeLimit = check_olume_limit(NTS, symbol=symbol, side=side, positionSide=positionSide, price=markPrice)
    maxOlumeLimit = maxOlumeLimit + 1
    res = NTS.order(price=markPrice, orderQty=maxOlumeLimit, tradeType=tradeType, symbol=symbol, orderType=orderType,marginType=marginType, side=side, positionSide=positionSide)
    orderAssertResult = _assert(res, (0, '1037', 'maxOlumeLimit=' + str(maxOlumeLimit) + ' '), '', CommonName,log_level);ModeCount(orderAssertResult,module+CommonName)
    return orderAssertResult

def orderLimitCheckAll(NTS,log_level=None):
    orderLongCheckLess(NTS,log_level=log_level)
    orderLongCheckEqual(NTS,log_level=log_level)
    orderLongCheckMore(NTS, log_level=log_level)
    orderShortCheckEqual(NTS, log_level=log_level)
    orderShortCheckLess(NTS, log_level=log_level)
    orderShortCheckkMore(NTS, log_level=log_level)

if __name__ == '__main__':
    NTS=NtsApiOrder(6,user_id='10070')
    print(orderShortCheckEqual(NTS))
    pass


