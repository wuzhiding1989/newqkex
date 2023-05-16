from BU.NTS.dataCheck.dataCheck import close_wear_no_pos
from BU.NTS.BasicData import BasicData
# from temp.Nts_Check_formula_owen import close_wear_Price
from BU.NTS.WebOrder import n_order
from common.asserts import responseCodeAssert as _assert
from common.util import request_http as req, truncate, printc, printl, d, requests, priceSpread, t as _t, \
    countCaseNumber, ModeCount
from BU.NTS.dataCheck.dataCheck import close_wear_Price


tradeType='linearPerpetual'
symbol='BTCUSDT'
module='平仓不穿仓'
#卖出平多，爆仓穿仓，不能下单
def closeLongCheck_01(NTS,log_level=None):
    CommonName='卖出平多，爆仓穿仓，不能下单'
    priceSize=BasicData().pricesize(NTS,tradeType=tradeType,symbol=symbol)
    position=NTS.position(tradeType=tradeType,symbol=symbol)['data']
    if len(position)!=0:
        for i in range(0,len(position)):
            if position[i]['positionSide']=='long':
                Amount=position[i]['availPos']
                positionSide=position[i]['positionSide']
                marginType=position[i]['marginType']
                res = close_wear_Price(NTS,symbol,Amount,positionSide)
                closePrice = truncate(float(round(res[0],priceSize)),priceSize)
                if priceSize==0:
                    closePrice=int(closePrice)
                else:
                    closePrice=float(closePrice)
                if closePrice <= 0:
                    print('期望：卖出平多爆仓穿仓,实际：该多仓仓位，无法爆仓，爆仓价格='+str(closePrice))

                else:
                    Response=NTS.order(log_level=1, tradeType=tradeType, symbol=symbol, marginType=marginType, price=closePrice, orderQty=Amount, side='sell', positionSide=positionSide, orderType='limit')
                    orderAssertResult=_assert(Response, (0, '1052', 'positionSide=' + positionSide + ' '), '', '限价平仓', log_level);ModeCount(orderAssertResult,module+CommonName)
                    return orderAssertResult
    else:
        printc('本次没有仓位可平',p_type='yellow')
        return False

#卖出平多，不爆仓不穿仓，可以下单
def closeLongCheck_02(NTS,log_level=None):
    CommonName = '卖出平多，不爆仓不穿仓，可以下单'
    priceSize = BasicData().pricesize(NTS, tradeType=tradeType, symbol=symbol)
    position = NTS.position(tradeType=tradeType, symbol=symbol)['data']
    if len(position) != 0:
        for i in range(0, len(position)):
            if position[i]['positionSide'] == 'long':
                Amount = position[i]['positionAmt']
                positionSide = position[i]['positionSide']
                marginType = position[i]['marginType']
                res = close_wear_Price(NTS, symbol, Amount, positionSide)
                closePrice = float(round(res[0], priceSize))
                fee=float(round(res[1], priceSize)) * 2
                newClosePrice = truncate(closePrice + fee,priceSize)
                if priceSize==0:
                    newClosePrice=int(newClosePrice)
                else:
                    newClosePrice=float(newClosePrice)
                if newClosePrice <= 0:
                    print('期望：卖出平多爆仓穿仓,实际：该多仓仓位，无法爆仓，爆仓价格='+str(closePrice))

                else:
                    Response = NTS.order(log_level=log_level, tradeType=tradeType, symbol=symbol, marginType=marginType, price=newClosePrice, orderQty=Amount, side='sell', positionSide=positionSide, orderType='limit')
                    orderAssertResult = _assert(Response, (0, '1', 'positionSide=' + positionSide + ' '), '', '限价平仓', log_level);ModeCount(orderAssertResult,module+CommonName)
                    orderId=Response['data']['orderId']
                    orderCancel=NTS.orderCancel(tradeType=tradeType, symbol=symbol,orderId=orderId,log_level=log_level)
                    orderAssertResult = _assert(orderCancel, (0, '1', 'positionSide=' + positionSide + ' '), '', '撤销平多仓订单', log_level)

                    return orderAssertResult
    else:
        print('本次没有仓位可平')
        return True



#买入平空，爆仓穿仓，不能下单
def closeShortCheck_03(NTS,log_level=None):
    CommonName = '买入平空，爆仓穿仓，不能下单'
    priceSize = BasicData().pricesize(NTS, tradeType=tradeType, symbol=symbol)
    position = NTS.position(tradeType=tradeType, symbol=symbol)['data']
    if len(position) != 0:
        for i in range(0, len(position)):
            if position[i]['positionSide'] == 'short':
                Amount = position[i]['availPos']
                positionSide = position[i]['positionSide']
                marginType = position[i]['marginType']
                res = close_wear_Price(NTS, symbol, Amount, positionSide)
                closePrice = truncate(float(round(res[0], priceSize)),priceSize)
                if priceSize==0:
                    closePrice=int(closePrice)
                else:
                    closePrice=float(closePrice)

                if closePrice >= 200000:
                    print('期望：买入平空爆仓穿仓,实际：该空仓仓位，无法爆仓，爆仓价格=' + str(closePrice))

                else:
                    Response = NTS.order(log_level=1, tradeType=tradeType, symbol=symbol, marginType=marginType, price=closePrice, orderQty=Amount, side='buy', positionSide=positionSide, orderType='limit')
                    orderAssertResult = _assert(Response, (0, '1052', 'positionSide=' + positionSide + ' '), '', '限价平仓',log_level);ModeCount(orderAssertResult,module+CommonName)
                    return orderAssertResult
    else:
        print('本次没有仓位可平')
        return True

#买入平空，不爆仓不穿仓，可以下单
def closeShortCheck_04(NTS,log_level=None):
    CommonName = '买入平空，不爆仓不穿仓，可以下单'
    priceSize = BasicData().pricesize(NTS, tradeType=tradeType, symbol=symbol)
    position = NTS.position(tradeType=tradeType, symbol=symbol)['data']
    if len(position) != 0:
        for i in range(0, len(position)):
            if position[i]['positionSide'] == 'short':
                Amount = position[i]['availPos']
                positionSide = position[i]['positionSide']
                marginType = position[i]['marginType']
                res = close_wear_Price(NTS, symbol, Amount, positionSide)
                closePrice = float(round(res[0], priceSize))
                fee = float(round(res[1], priceSize)) * 2
                newClosePrice =truncate((closePrice - fee ) * (0.99),priceSize)
                if priceSize==0:
                    newClosePrice=int(newClosePrice)
                else:
                    newClosePrice=float(newClosePrice)

                if newClosePrice >= 200000:
                    print('期望：买入平空爆仓穿仓,实际：该空仓仓位，无法爆仓，爆仓价格=' + str(closePrice))

                else:
                    Response = NTS.order(log_level=log_level, tradeType=tradeType, symbol=symbol, marginType=marginType, price=newClosePrice, orderQty=Amount, side='buy', positionSide=positionSide, orderType='limit')
                    orderAssertResult = _assert(Response, (0, '1', 'positionSide=' + positionSide + ' '), '', '限价平仓',log_level);ModeCount(orderAssertResult,module+CommonName)
                    orderId = Response['data']['orderId']
                    orderCancel = NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=orderId,log_level=log_level)
                    orderAssertResult = _assert(orderCancel, (0, '1', 'positionSide=' + positionSide + ' '), '','撤销平空仓订单', log_level)
                    return orderAssertResult
    else:
        print('本次没有仓位可平')
        return True


def closePositionCaseAll(NTS,log_level=None):
    closeLongCheck_01(NTS,log_level=None)
    closeLongCheck_02(NTS,log_level=None)
    closeShortCheck_03(NTS,log_level=None)
    closeShortCheck_04(NTS,log_level=None)





if __name__ == '__main__':
    NTS = n_order(6, user_id='10070')
    # NTS=n_order(6,user_id='97201938')
    print(closeLongCheck_02(NTS))