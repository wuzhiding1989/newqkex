from BU.NTS.dataCheck.dataCheck import close_wear_no_pos, t_risk_limit_leverage,makerprice
from BU.NTS.BasicData import BasicData as BD
from temp.Nts_Check_formula_owen import close_wear_Price
from common.util import request_http as req, truncate, printc, printl, d, requests, priceSpread, t as _t, \
    countCaseNumber, ModeCount
from common.asserts import responseCodeAssert as _assert
from BU.NTS.Calculator import riskLimit, minLeverage, maxLeverage,leverage
from common.util import d
from BU.NTS.WebOrder import n_order
from BU.NTS.ApiOrder import NtsApiOrder
import math
import random
from common.asserts import responseCodeAssert as _assert
from BU.NTS.dataCheck import dataCheck

tradeType = 'linearPerpetual';
marginType = 'cross'
currency = 'USDT'
symbol='BTCUSDT'
module='切换杠杆限制'
orderType='limit'
# 切换杠杆测试用例
def changeLeverageCase(NTS, log_level=None):
    CommonName='切换杠杆正常场景';
    caseResult = True
    maxleverage = maxLeverage(NTS, tradeType, symbol)
    minleverage = minLeverage(NTS, tradeType, symbol)
    maxlever = math.floor(maxleverage)
    minlever = math.ceil(minleverage)
    currleverage = random.randint(minlever, maxlever)
    res = NTS.changeleverage(tradeType=tradeType, symbol=symbol, marginType=marginType, leverage=currleverage,log_level=log_level)
    orderAssertResult = _assert(res, (0, '1', 'leverage=' + str(currleverage) + ' '), '', '切换杠杆正常场景', log_level);ModeCount(orderAssertResult,module+CommonName)
    return orderAssertResult

# 切换低于最低杠杆测试用例
def changeMinLeverageCase(NTS, log_level=None):
    CommonName = '切换低于最低支持杠杆异常场景';
    minleverage = minLeverage(NTS, tradeType, symbol)
    if minleverage >0 and minleverage<1:
        minleverage = round(minleverage,1)
    else:
        minleverage = math.floor(minleverage) - 1
        if minleverage==0:
            minleverage=0.1
    minleverage=str(minleverage)
    res = NTS.changeleverage(tradeType=tradeType, symbol=symbol, marginType=marginType, leverage=minleverage,log_level=log_level)
    orderAssertResult = _assert(res, (0, '1040', 'leverage=' + str(minleverage) + ' '), '', '切换低于最低支持杠杆异常场景', log_level);ModeCount(orderAssertResult,module+CommonName)


    return orderAssertResult

# 切换高于最高杠杆测试用例
def changeMaxLeverageCase(NTS, log_level=None):
    CommonName = '切换高于最高支持杠杆异常场景';
    maxleverage = maxLeverage(NTS, tradeType, symbol)
    maxlever = math.ceil(maxleverage) + 1
    res = NTS.changeleverage(tradeType=tradeType, symbol=symbol, marginType=marginType, leverage=maxlever,log_level=log_level)
    orderAssertResult = _assert(res, (0, '1013', 'leverage=' + str(maxlever) + ' '), '', '切换高于最高支持杠杆异常场景', log_level);ModeCount(orderAssertResult,module+CommonName)

    return orderAssertResult


#下单价值超过杠杆对应的风险限额
def orderLongRiskLimitMore(NTS,log_level=None):
    CommonName='买入开多价值超过当前杠杆对应的风险限额'
    side='buy';positionSide='long'
    leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    tRiskLiit=t_risk_limit_leverage(symbol=symbol)
    pricesize = BD().pricesize(NTS, tradeType=tradeType, symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate(round(float(markPriceMap[symbol])/2, pricesize), pricesize)
    res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = res['ctVal']
    for i in range(0,len(tRiskLiit)):
        if d(leverage)<=tRiskLiit[i][1]:
            risklimit=tRiskLiit[i][0]
            break
    amout=float(risklimit)/float(markPrice)//float(ctVal)
    orderQty=int(amout+2)
    res=NTS.order(tradeType=tradeType,symbol=symbol,price=markPrice,side=side,positionSide=positionSide,marginType=marginType,orderQty=orderQty,orderType=orderType)

    orderAssertResult = _assert(res, (0, '1017', 'risklimit=' + str(risklimit) + ' '), '', '买入开多价值超过当前杠杆对应的风险限额', log_level);
    ModeCount(orderAssertResult, module + CommonName)

    return orderAssertResult


def ordershortRiskLimitMore(NTS,log_level=None):
    CommonName='卖出开空价值超过当前杠杆对应的风险限额'
    side='sell';positionSide='short'
    leverage = NTS.leverage_info(tradeType=tradeType, symbol=symbol, marginType=marginType)['data'][0]['leverage']
    tRiskLiit=t_risk_limit_leverage(symbol=symbol)
    pricesize = BD().pricesize(NTS, tradeType=tradeType, symbol=symbol)
    markPriceMap = makerprice(NTS)
    markPrice = truncate(round(float(markPriceMap[symbol])*1.5, pricesize), pricesize)
    res = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = res['ctVal']
    for i in range(0,len(tRiskLiit)):
        if d(leverage)<=tRiskLiit[i][1]:
            risklimit=tRiskLiit[i][0]
            break
    amout=float(risklimit)/float(markPrice)//float(ctVal)
    orderQty=int(amout+2)
    res=NTS.order(tradeType=tradeType,symbol=symbol,price=markPrice,side=side,positionSide=positionSide,marginType=marginType,orderQty=orderQty,orderType=orderType)

    orderAssertResult = _assert(res, (0, '1017', 'risklimit=' + str(risklimit) + ' '), '', '卖出开空价值超过当前杠杆对应的风险限额', log_level);
    ModeCount(orderAssertResult, module + CommonName)

    return orderAssertResult









def changeLeverageCaseAll(NTS,log_level=None):
    changeLeverageCase(NTS,log_level=log_level)
    changeMinLeverageCase(NTS, log_level=log_level)
    changeMaxLeverageCase(NTS, log_level=log_level)
    orderLongRiskLimitMore(NTS, log_level=log_level)
    ordershortRiskLimitMore(NTS, log_level=log_level)







if __name__ == '__main__':
    # NTS = NtsApiOrder(6, user_id='10070')
    NTS = n_order(6, user_id='10070')
    # print(changeLeverageCaseAll(NTS))
    print(orderLongRiskLimitMore(NTS))
