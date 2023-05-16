import os
import sys
import BasicData as BD
object_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(object_path)
from common.util import d
from common.mysqlClient import mysql
import dataCheck
# from temp.Nts_Check_formula_owen import marginEquity
# t=mysql(3)
t = mysql(7)
tidb=mysql(server=6,product=1)
#最大下单数量 计算 - Author : Brian
def MaxOrderNumber(positionSide=None,side=None,available_margin=None,orderPrice=None,leverage=None,takerFeeRate=None,posionBuy=None,closeBuy=None,posionSell=None,closeSell=None,bid1=None):
    if positionSide.upper() in ['BOTH']:
        if str(side)=='1':
            _MaxOrderNumber=available_margin/orderPrice/(1/leverage+takerFeeRate)+(posionSell-closeSell)
        if str(side)=='2':
            _MaxOrderNumber=available_margin/max(bid1,orderPrice)/(1/leverage+takerFeeRate)+(posionSell-closeSell)
    if positionSide.upper() in ['LONG','SHORT']:
        if positionSide.upper=='LONG':
            _MaxOrderNumber=available_margin/orderPrice/(1/leverage+takerFeeRate)
        if str(side)=='2':
            _MaxOrderNumber=available_margin/max(bid1,orderPrice)/(1/leverage+takerFeeRate)

#冻结保证金 计算 - Author : Brian
def FrozenMargin(side=None,orderPrice=None,orderQty=None,takerFeeRate=None,leverage=None,coinValue=None,bid1=0):
    # print(bid1,side,orderPrice,orderQty,leverage,coinValue,takerFeeRate)
    if str(side)=='1' or side=='buy':
        _FrozenMargin=d(orderPrice)*d(orderQty)/d(leverage)*d(coinValue)+d(orderPrice)*d(orderQty)*d(coinValue)*d(takerFeeRate)
    if str(side)=='2' or side=='sell':
        _FrozenMargin=d(max(d(bid1),d(orderPrice)))*d(orderQty)/d(leverage)*d(coinValue)+d(max(d(bid1),d(orderPrice)))*d(orderQty)*d(coinValue)*d(takerFeeRate)
    return _FrozenMargin

#未实现盈亏 计算 - Author : Brian
def UnRealisePnl(side,markPrice,avgEntryPrice,positionAmt,ctVal):
    if str(side)  in ['long']:
        _UnRealisePnl=(d(markPrice)-d(avgEntryPrice) ) * d(positionAmt) * d(ctVal)
    if str(side)   in ['short']:

        _UnRealisePnl =(d(avgEntryPrice) - d(markPrice)) * d(positionAmt) * d(ctVal)

    # print('未实现盈亏',_UnRealisePnl)
        # _UnRealisePnl=truncate(_UnRealisePnl,22)
    return _UnRealisePnl

#持仓保证金 计算 - Author : Brian
def PositionMargin(markPrice,positionAmt,ctVal,leverage) :
    _PositionMargin=d(markPrice)*d(positionAmt)*d(ctVal)/d(leverage)
    return _PositionMargin

#权益 计算 - Author : Brian  余额+未实现盈亏
def Equity(amount,unRealisePnl) :
    _Equity=d(amount)+d(unRealisePnl)
    return _Equity

#可用 计算 - Author : Brian   可用 = 账户权益 - 委托保证金 - 全仓持仓保证金 - 逐仓权益 - 划转冻结
def AvailMargin(Equity, unFronzen, positonMargin, isolatedEquity, transferFrozen):
    _availMaring=d(Equity)-d(positonMargin)-d(unFronzen)-d(isolatedEquity)-d(transferFrozen)
    return _availMaring

#最大可划转 计算 - Author : Brian   max( min (可用，余额)，0)
def TransferAmount(availMaring=None,amount=None,MarginType=None,EquityIsolated=None,WarnMarginRate=None,Side=None,FundingRate=None,TakerFeeRate=None,PositionQty=None,MarkPrice=None,Ctval=None,log_level=None):
    # print('测试计算值 可用',availMaring,'余额',amount,min(availMaring,amount))
    if not MarginType: #全仓= max { min ( 可用 ，账户余额 ) , 0 }
        _transferAmount=max(min(d(availMaring),d(amount)),0)
    else: # 逐仓最大转出= max { 0 , 逐仓权益 - ( 预警保证金率 + max( p * 资金费率，0 ) + taker费率 ) * 持仓数量 * 标记价格 ) }
        p=1 if Side=='buy' else -1
        RateSum=d(WarnMarginRate)+max(d(p*FundingRate),0)+d(TakerFeeRate)
        if log_level and log_level>=2: print('逐仓权益:',EquityIsolated,'各类费率*标记价*数量',RateSum*d(PositionQty)*d(MarkPrice)*d(Ctval))
        _transferAmount=max(0,d(EquityIsolated)-(d(WarnMarginRate)+max(d(p*FundingRate),0)+d(TakerFeeRate))*d(PositionQty)*d(Ctval)*d(MarkPrice))
    return _transferAmount
#最大可开计算（前端） - Author： Brian
def MaxOpenQty(side,avail,orderPrice,leverage,takerRate,ctVal,bid1=None):
    if side=='buy':
        _MaxOpenQty=max(d(avail),0)/(d(orderPrice)*(1/d(leverage)+d(takerRate))) / d(ctVal)
    if side=='sell':
        _MaxOpenQty=max(d(avail),0)/(max(d(orderPrice),d(bid1))*(1/d(leverage)+d(takerRate)))  / d(ctVal)
    return int(_MaxOpenQty)

#未实现盈亏 = 用户所有持仓的盈亏
#多仓未实现盈亏 =（ 标记价格 - 开仓均价 ）* 持仓数量
#空仓未实现盈亏 =（ 开仓均价 - 标记价格 ）* 持仓数量
def unrealisedPnl(longamount,shortamount,openLongPrice,maketPrice,openShortPrice,ctVal):
    longunrealisedPnl = (maketPrice - openLongPrice) * longamount * d(ctVal)
    shortunrealisedPnl= (openShortPrice - maketPrice) * shortamount * d(ctVal)

    return longunrealisedPnl+shortunrealisedPnl

def CaulatorAvgPrice(CurrentAvgPrice,CurrentPositionAmt,OrderPrice,OrderQty):
    CurrentPosition_=d(CurrentAvgPrice)*d(CurrentPositionAmt)
    Order_=d(OrderQty)*d(OrderPrice)
    CaulatorAvgPrice=(CurrentPosition_+Order_) / (d(CurrentPositionAmt)+d(OrderQty))
    return CaulatorAvgPrice
#已实现盈亏 = 平仓盈亏 - 手续费
def Profit(closePnl,fee):
    pnl = closePnl - fee

    return pnl
#仓位收益率
def marginRatio(unrealisedPnl,PositionMargin):

    maintMarginRatio= unrealisedPnl / PositionMargin

    return maintMarginRatio

#   多仓平仓盈亏 = ( 平仓均价 - 持仓均价 ) * 平仓数量
#   空仓平仓盈亏 = ( 持仓均价 - 平仓均价 ) * 平仓数量
def realisedPnl(webnts,symbol,side,ctVal):

    if side == "buy":
        hisOrder_r = webnts.hisOrders(webnts,symbol=symbol,side=side,positionSide="long")
        posi_avg_price = hisOrder_r["data"]["list"][0]["avgPrice"]
        hisOrder_r = webnts.hisOrders(webnts,symbol=symbol, side="sell",positionSide="long")
        colse_avg_price = hisOrder_r["data"]["list"][0]["avgPrice"]
        amount = hisOrder_r["data"]["list"][0]["filledQty"]
        commission = hisOrder_r["data"]["list"][0]["commission"]
        realProfit = hisOrder_r["data"]["list"][0]["realProfit"]
        long_realisedPnl = (d(colse_avg_price) - d(posi_avg_price)) * d(amount) * d(ctVal)- d(commission)
        if d(long_realisedPnl) - d(realProfit) > 0.000000000000000001:
            print('<已实现盈亏 验证成功.>')
        else:
            print(f"预期:{d(long_realisedPnl)},实际:{d(realProfit)}")

    if side == "sell":
        hisOrder_r = webnts.hisOrders(webnts,symbol=symbol,side=side, positionSide="short")
        posi_avg_price = hisOrder_r["data"]["list"][0]["avgPrice"]
        hisOrder_r = webnts.hisOrders(webnts,symbol=symbol,side="buy", positionSide="short")
        colse_avg_price = hisOrder_r["data"]["list"][0]["avgPrice"]
        amount = hisOrder_r["data"]["list"][0]["filledQty"]
        commission = hisOrder_r["data"]["list"][0]["commission"]
        realProfit = hisOrder_r["data"]["list"][0]["realProfit"]
        short_realisedPnl = (d(posi_avg_price) - d(colse_avg_price)) * d(amount) * d(ctVal) - d(commission)
        if d(short_realisedPnl) - d(realProfit) > 0.000000000000000001:
            print('<已实现盈亏 验证成功.>')
        else:
            print(f"预期:{d(short_realisedPnl)},实际:{d(realProfit)}")


#风险限额
def riskLimit(NTS,tradeType, symbol):
    pos=[]
    r = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = r['ctVal']
    # 查持仓
    position = NTS.position(tradeType=tradeType, symbol=symbol)['data']
    # 查当前委托
    openposition = NTS.OpenOrders(tradeType=tradeType, symbol=symbol, pageNum=1, pageSize=100)['data']
    markPrice=NTS.webposition(symbol)
    #多仓价值
    longUsdt = 0
    #空仓价值
    shortUsdt = 0
    #当前委托多仓价值
    openLongUsdt = 0
    #当前委托空仓价值
    openShortUsdt = 0
    # longPositionValue = 0
    # shortPositionValue = 0

    if len(position) > 0:
        for i in range(0, len(position)):
            if position[i]['positionSide'] == 'long':
                longUsdt = d(markPrice) * d(position[i]['positionAmt']) * d(ctVal)
            else:
                shortUsdt = d(markPrice) * d(position[i]['positionAmt']) * d(ctVal)
    if openposition['totalSize'] > 0:
        openpos = openposition['list']
        for i in range(0, len(openpos)):
            if openpos[i]['positionSide'] == 'long':
                openLongUsdt += d(openpos[i]['price']) * d(openpos[i]['leavesQty']) * d(ctVal)
            else:
                openShortUsdt = d(openpos[i]['price']) * d(openpos[i]['leavesQty']) * d(ctVal)
    longPositionValue = longUsdt + openLongUsdt
    shortPositionValue = shortUsdt + openShortUsdt
    pos.append(longPositionValue)
    pos.append(shortPositionValue)

    return pos



# 获取当前币种最大杠杆
def maxLeverage(NTS,tradeType, symbol):
    # 获取风险限额对应最大杠杆list
    res = riskLimit(NTS, tradeType=tradeType, symbol=symbol)
    # 获取当前账户仓位价值
    posUsdt = max(d(res[0]) , d(res[1]))
    # 获取当前账户支持最大的杠杆
    leveragelist = leverage(symbol)
    for i in range(0, len(leveragelist)):
        if d(posUsdt) <= d(leveragelist[i][0]):
            maxLeverage = float(leveragelist[i][1])  # 最大杠杆
            return maxLeverage


# 获取支持切换最低杠杆
def minLeverage(NTS,tradeType, symbol):
    Response = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = Response['ctVal']
    # 获 持仓取保证金 + 可用保证金
    currency=symbol[-4:]
    Margin = NTS.Balance(currency=currency)['data'][0]
    PositionMargin = Margin['marginPosition']
    marginAvailable = Margin['marginAvailable']
    amount = 0
    r = NTS.position(tradeType=tradeType, symbol=symbol)
    markPriceMap = dataCheck.makerprice(NTS)
    markPrice = markPriceMap[symbol]
    if r['code'] == '1':
        res = r['data']
        if len(res) > 0:
            for i in range(0, len(res)):
                amount += float(res[i]['positionAmt'])

            minleverage = d(markPrice) * d(amount) * d(ctVal) / (d(PositionMargin) + d(marginAvailable))
            return minleverage
        else:
            return 1


# 查询支持最大杠杆
def leverage(symbol):
    symbol='"'+symbol+'"'
    leverageSql ='select value_limit,max_leverage from qa_mulan_trade.t_risk_limit where margin_type=2 and symbol=%s order by value_limit asc'% symbol
    maxLeverage = t.mysql(leverageSql, True)
    maxLeverage = list(maxLeverage)

    return maxLeverage
#查询最大下单张数限制
def t_order_volume_limit(symbol):
    symbol = '"' + symbol + '"'
    orderVolumeLimitSql='select symbol,order_max_volume from qa_mulan_trade.t_order_volume_limit where trade_type=81 and symbol=%s'%symbol
    maxorderVolume = t.mysql(orderVolumeLimitSql, True)
    maxorderVolume = int(maxorderVolume[0][1])
    return maxorderVolume
#查询风险限额
def t_risk_limit(trade_type,margin_type,symbol=None):
    if symbol == None:
        tRiskLimitSql='select symbol,value_limit,maintenance_margin_rate,grade from qa_mulan_trade.t_risk_limit where trade_type=%s and margin_type=%s order by value_limit' %(trade_type,margin_type)
        tRiskLimit = t.mysql(tRiskLimitSql, True)
        tRiskLimit = list(list(tRiskLimit))
        return tRiskLimit
    else:
        symbol = '"' + symbol + '"'
        tRiskLimitSql = 'select value_limit,maintenance_margin_rate,grade from qa_mulan_trade.t_risk_limit where trade_type=%s and margin_type=%s and symbol=%s order by grade' % (
        trade_type, margin_type,symbol)
        tRiskLimit = t.mysql(tRiskLimitSql, True)
        tRiskLimit = list(list(tRiskLimit))
        return tRiskLimit


#账户风险率，账户风险率 = sum全仓各交易对维持保证金 / （可用 + 全仓持仓保证金）
def riskRito():
    return
#下单仓位价值对应风险限额/标记价格 - 持仓数量 - 同向挂单冻结数量
def risk_limit_orderQty(riskLimit,positionSide,orderPrice,positionAmt,openAmt,ctVal,bid1=None):
    if positionSide=='long':
        riskLimitOrderQty = (d(riskLimit) - d(positionAmt) -d(openAmt)) / d(orderPrice) // d(ctVal)
    else:
        maxprice= max(str(orderPrice),bid1)
        riskLimitOrderQty = (d(riskLimit) - d(positionAmt) -d(openAmt)) / d(maxprice) //d(ctVal)

    return int(riskLimitOrderQty)




#维持保证金,维持保证金 = 标记价格 * 持仓数量 * 维持保证金率
def maintenance_margin(markPrice,posAmount,maintenanceMarginRate):
    maintenanceMargin = markPrice * posAmount * maintenanceMarginRate

    return maintenanceMargin





def avgPrice(uid,orderId):
    uid=int(uid)
    #select sum(filled_qty*filled_price)/sum(filled_qty) from t_trade where uid=%s and  order_id=%s
    # avgPriceSql='select * from qa_mulan_btc1.t_trade where uid=10070 '
    # avgPriceSql='select (filled_qty*filled_price)/sum(filled_qty) from qa_mulan_btc1.t_trade where uid=%s and  order_id=%s'%uid %orderId
    avgPriceSql='select sum(filled_qty*filled_price)/sum(filled_qty) from qa_mulan_btc1.t_trade where uid=%s and order_id=%s'%(uid,orderId)
    avgPrice = tidb.mysql(avgPriceSql, True)
    avgPrice=list(avgPrice)[0][0]
    return avgPrice


#查询最优N档配置
def t_symbol_optimum_level(symbol):
    symbol = '"' + symbol + '"'
    optimum_levelSql='select optimum_level from qa_mulan_trade.t_symbol_config where trade_type=81 and symbol=%s'%symbol
    return int(t.mysql(optimum_levelSql, True)[0][0])

#查询OrderRange幅度
def t_symbol_optimum_rate(symbol):
    symbol = '"' + symbol + '"'
    optimum_rateSql='select optimum_rate from qa_mulan_trade.t_symbol_config where trade_type=81 and symbol=%s'%symbol
    return int(t.mysql(optimum_rateSql, True)[0][0])


if __name__ == '__main__':
    class c:
        def __init__(self):pass
        def cc(self):
            print(1)
    a=c()
    print(type(a))

    #单元测试
    # print(FrozenMargin(1,19000.00,20,0.004,50,0.001))
    # print(avgEntryPrice(1))
    # a=UnRealisePnl('short',20000,18583.994411764705882352,204,0.01) #对底层算法进行单元测试 可以 和 java的计算方法进行对比验证
    # print(d('20696.000000000000000001')-d('7562.000000000000000000'))
    # # # *d(2.04)
    from BU.NTS.WebOrder import n_order
    #
    NTS = n_order(6, user_id=10070)
    # print(realisedPnl(NTS,"ETHUSDT","buy",0.01))
    # a=UnRealisePnl('long',1795.016,'1342.388888888888888888',1,0.01) #对底层算法进行单元测试 可以 和 java的计算方法进行对比验证
    # print('盈亏：',a)
    # # *d(2.04)
    # LV=d('0.005')*d('1.2')+0+d('0.0004')
    # RightExplore=d(1800)*d(0.01)*d(LV)+d(19500)*d(0.01)*d(LV)
    # Left=d('104.259004003506572498')+d(1800)*d(0.01)
    # print('开仓强平校验：',Left,RightExplore)
    # print(avgPrice(NTS.user_id,orderId=1030892011453972480))