import BU.NTS.Calculator as cal
from UnitTest.com import LogName
from BU.NTS.WebOrder import n_order
import param.dict as param_dict
from param.dict import linear_tradeType
from UnitTest.AOP import AOP
from common import mysqlClient
from common.other import httpCheck as e
from common.util import printc, d, printl
from common.util import LogOuts

t = mysqlClient.mysql(7)


# A强平价格 = 【sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）-
# A标记价格*A净持仓数量 - sum各交易对（标记价格 * 持仓数量 / 杠杆 ）-可用】 /
# 【 - A净持仓数量 - A持仓数量 * （维持保证金率A + max（ - 资金费率,0）+taker手续费率A ） -（ a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a）】
# 资金费用 = -P * 持仓数量 * 结算标记价格 * 资金费率
# 其他交易对计算：
# B交易对持仓保证金 = B标记价格*B持仓数量/B杠杆
# B交易对维持保证金 = B标记价格*B持仓数量*B维持保证金率
# B交易对预付资金费率 = B标记价格*B持仓数量*max（p'*B资金费率，0）
# B交易对强平手续费 = B标记价格*B持仓数量*taker手续费率
# p为每个持仓的持仓方向系数
# 净A交易对多持仓数量（小于0A多仓强平价格“- -”）= A多仓持仓数量 - A空仓持仓数量
# 净A交易对空持仓数量（小于0A空仓强平价格“- -”）= A空仓持仓数量 - A多仓持仓数量
# a持仓数量 = A反向持仓
# 净A多持仓小于0时，A多仓强平价格“- -”
#


# 全仓--双向持仓-强平价
def cross_liquidation_price(NTS, log_level=None):
    marginType = 'cross'
    caseTitle = '全仓双向--强平价'
    instrument = NTS.instrument
    funding = -0.0018830852
    otherSymbol = []
    trade_type = 81  # 正向永续业务线
    margin_type = 2  # 全仓=2，逐仓=1
    # 查询账户资产
    balance = NTS.Balance(currency='USDT')
    if not e(balance)[0]:
        printc(caseTitle + '账户余额查询失败,退出', balance['code'] + balance['message'])
        return False
    LogOuts(NTS, caseTitle, LogName)
    marginAvailable = balance['data'][0]['marginAvailable']
    # 获取当前币种持仓
    res = NTS.position(tradeType=linear_tradeType)
    # 如果查持仓接口失败，则退出
    if not e(res)[0]:
        printc(caseTitle + '持仓查询失败,退出', res['code'] + res['message'])
        return False
    LogOuts(NTS, caseTitle, LogName)
    res = res['data']
    if len(res) > 0:
        for i in range(0, len(res)):
            if res[i]['marginType'] == marginType:
                if res[i]['symbol'] not in otherSymbol:
                    otherSymbol.append(res[i]['symbol'])
    else:
        printc(caseTitle + f'该uid:{NTS.user_id}没有持仓，退出' + res['data'])
        return False
    #sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
    otherPosUsdt = sumSymbolValue(res,instrument)
    # 查询正向永续全仓风险限额
    t_risk_limit = cal.t_risk_limit(trade_type, margin_type)
    # 合并数据
    othersymbolpos = mergeData(res, otherSymbol, instrument, t_risk_limit, marginType, NTS)

    if len(otherSymbol) < 2:
        otherMaintMargin = 0  # sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
        WarningMargin = warningMargin(otherSymbol[0], othersymbolpos, funding)
        positionValue = WarningMargin[1]  # p*A标记价格*A净持仓数量
        currWarningMargin = WarningMargin[2]  # A净持仓数量 - A持仓数量 * （维持保证金率A + max（ 资金费率,0）+taker手续费率A ）
        faceWarningMargin = WarningMargin[3]  # a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a）
        liquidation_price = (d(otherMaintMargin) + d(positionValue) - d(marginAvailable) - d(otherPosUsdt)) / (
                d(currWarningMargin) - d(faceWarningMargin))
        print(otherSymbol[0] + f'强平价格=' + str(liquidation_price), '公式明细如下')
        print(f'sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）={otherMaintMargin}')
        print(f'sum各交易对（标记价格 * 持仓数量 / 杠杆 ）={otherPosUsdt}')
        print(f'可用={marginAvailable}')
        print(f'p*A标记价格*A净持仓数量={positionValue}')
        print(f'A净持仓数量 - A持仓数量 * （维持保证金率A + max（ 资金费率,0）+taker手续费率A ）={currWarningMargin}')
        print(f'a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a）={faceWarningMargin}')

        return liquidation_price
    else:
        liquidationPrice = {}
        for symbol in otherSymbol:
            # sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
            # sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
            otherMargin = OtherMaintMargin(symbol, otherSymbol, othersymbolpos)
            otherMaintMargin = otherMargin[0]  # sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
            WarningMargin = warningMargin(symbol, othersymbolpos, funding)
            positionValue = WarningMargin[1]  # p*A标记价格*A净持仓数量
            currWarningMargin = WarningMargin[2]  # A净持仓数量 - A持仓数量 * （维持保证金率A + max（ 资金费率,0）+taker手续费率A ）
            faceWarningMargin = WarningMargin[3]  # a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a）
            liquidation_price = (d(otherMaintMargin) + d(positionValue) - d(marginAvailable) - d(otherPosUsdt)) / (
                    d(currWarningMargin) - d(faceWarningMargin))
            print(symbol + f'强平价格=' + str(liquidation_price), '公式明细如下')
            print(f'sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）={otherMaintMargin}')
            print(f'sum各交易对（标记价格 * 持仓数量 / 杠杆 ）={otherPosUsdt}')
            print(f'可用={marginAvailable}')
            print(f'p*A标记价格*A净持仓数量={positionValue}')
            print(f'A净持仓数量 - A持仓数量 * （维持保证金率A + max（ 资金费率,0）+taker手续费率A ）={currWarningMargin}')
            print(f'a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a）={faceWarningMargin}')
            liquidationPrice[otherSymbol[i]] = liquidation_price

        return liquidationPrice


# 逐仓--双向持仓-强平价
def isolated_liquidation_price(NTS, log_level=None):
    marginType = 'isolated'
    caseTitle = '全仓双向--空仓强平价'
    instrument = NTS.instrument
    funding = -0.0018830852
    otherSymbollist = []
    trade_type = 81  # 正向永续业务线
    margin_type = 1  # 全仓=2，逐仓=1
    # 获取当前币种持仓
    res = NTS.position(tradeType=linear_tradeType)
    # 如果查持仓接口失败，则退出
    if not e(res)[0]:
        printc(caseTitle + '持仓查询失败,退出', res['code'] + res['message'])
        return False
    res = res['data']
    if len(res) > 0:
        for i in range(0, len(res)):
            if res[i]['marginType'] == marginType:
                if res[i]['symbol'] not in otherSymbollist:
                    otherSymbollist.append(res[i]['symbol'])
    else:
        printc(caseTitle + f'该uid:{NTS.user_id}没有持仓，退出' + res['data'])
        return False
    # 查询正向永续全仓风险限额
    t_risk_limit = cal.t_risk_limit(trade_type, margin_type)
    # 合并数据
    othersymbolpos = mergeData(res, otherSymbollist, instrument, t_risk_limit, marginType, NTS)
    liquidationPrice = {}
    for symbol in otherSymbollist:
        if 'long' in othersymbolpos[symbol]:
            posamount = d(othersymbolpos[symbol]['long']) * d(othersymbolpos[symbol]['ctVal'])
            posMargin = d(othersymbolpos[symbol]['long_posMargin'])
            avgEntryPrice = d(othersymbolpos[symbol]['long_avgEntryPrice'])
            maintenanceMarginRate = d(othersymbolpos[symbol]['isolated_long_maintenance_margin_rate'])
            funding = d(othersymbolpos[symbol]['funding'])
            takerRate = d(othersymbolpos[symbol]['TakerRate'])
            # 强平价格 = （仓位保证金 / 持仓数量 - 持仓均价）/ ( 维持保证金率 + max ( 资金费率 , 0 ) + taker手续费率 - 1 )  --多仓
            longliquidationPrice = (posMargin / posamount - avgEntryPrice) / (
                        maintenanceMarginRate + max(funding, 0) + takerRate - 1)
            liquidationPrice[symbol]['long_liquidationPrice'] = longliquidationPrice
        if 'short' in othersymbolpos[symbol]:
            posamount = d(othersymbolpos[symbol]['short']) * d(othersymbolpos[symbol]['ctVal'])
            posMargin = d(othersymbolpos[symbol]['short_posMargin'])
            avgEntryPrice = d(othersymbolpos[symbol]['short_avgEntryPrice'])
            maintenanceMarginRate = d(othersymbolpos[symbol]['isolated_short_maintenance_margin_rate'])
            funding = d(othersymbolpos[symbol]['funding'])
            takerRate = d(othersymbolpos[symbol]['TakerRate'])
            # 强平价格 = （仓位保证金 / 持仓数量 - 持仓均价）/ ( 1*维持保证金率 + max ( 资金费率 , 0 ) + taker手续费率 + 1 )  --空仓
            shortliquidationPrice = (posMargin / posamount - avgEntryPrice) / (
                        -1 * maintenanceMarginRate + max(funding, 0) + takerRate + 1)
            liquidationPrice[symbol]['short_liquidationPrice'] = shortliquidationPrice

    return liquidationPrice


# 全仓--双向持仓-预估强平价
def cross_forecast_liquidation_price(NTS, symbol, price, amount, log_level=None):
    p = 1
    marginType = 'cross'
    forecast_liquidation_price = {}
    aop = AOP(NTS, symbol, '2')
    OpenOrders = aop.OpenOrders[symbol][marginType]
    otherSymbol = []
    markprice = param_dict.makrPriceMap[symbol]
    caseTitle = f'{marginType}双向--预估强平价'
    instrument = NTS.instrument
    ctVal = instrument[symbol]['ctVal']
    takerRate = instrument[symbol]['takerRate']
    funding = -0.0018830852
    trade_type = 81  # 正向永续业务线
    margin_type = 1  # 全仓=2，逐仓=1
    openCoin = d(amount) * d(ctVal)  # 开仓数量
    longOpenValue = 0  # 下单币对开仓多仓价值
    shortOpenValue = 0  # 下单币对开仓空仓价值
    longOpenCoin = 0  # 下单币对开仓多仓币数量
    shortOpenCoin = 0  # 下单币对开仓空仓币数量
    longPosiValue = 0  # 下单币对持仓多仓价值
    shortPosiValue = 0  # 下单币对持仓空仓价值
    otherMaintMargin = 0  # sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
    otherPosUsdt = 0  # sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
    if 'buy' in OpenOrders:
        longOpenValue = OpenOrders['buy']['value']  # 当前委托 多仓仓位价值
        longOpenCoin = OpenOrders['buy']['coin']  # 当前委托 多仓币量
    if 'sell' in OpenOrders:
        shortOpenValue = OpenOrders['sell']['value']  # 当前委托 空仓仓位价值
        shortOpenCoin = OpenOrders['sell']['coin']  # 当前委托 空仓币量
    # 查询账户资产
    balance = NTS.Balance(currency='USDT')
    if not e(balance)[0]:
        printc(caseTitle + '账户余额查询失败,退出', balance['code'] + balance['message'])
        return False
    marginAvailable = balance['data'][0]['marginAvailable']
    # 获取当前币种持仓
    res = NTS.position(tradeType=linear_tradeType)
    # 查询正向永续全仓风险限额
    t_risk_limit = cal.t_risk_limit(trade_type, margin_type)
    # 如果查持仓接口失败，则退出
    if not e(res)[0]:
        printc(caseTitle + '持仓查询失败,退出', res['code'] + res['message'])
        return False
    LogOuts(NTS, caseTitle, LogName)
    res = res['data']
    if len(res) > 0:
        for i in range(0, len(res)):
            if res[i]['marginType'] == marginType:
                if res[i]['symbol'] not in otherSymbol:
                    otherSymbol.append(res[i]['symbol'])
        # 合并数据
        othersymbolpos = mergeData(res, otherSymbol, instrument, t_risk_limit, marginType, NTS=None)
        sumSymbolUsdt = sumSymbolValue(res,instrument)
        if len(otherSymbol) == 1:
            if symbol == otherSymbol[0]:
                symbolpos = othersymbolpos[symbol]
                longamount = 0
                shortamount = 0
                openPnl = (d(markprice) - d(price)) * openCoin  # ( A标记价格 - 委托价格) * 开仓数量

                if 'long' in symbolpos:
                    longamount = symbolpos['long']
                    posLongValue = symbolpos['posLongValue']
                if 'short' in symbolpos:
                    shortamount = symbolpos['long']
                    posShortValue = symbolpos['posShortValue']
                longNetPosiCoin = d(amount + longamount - shortamount) * d(ctVal)  # 多仓，A’净持仓数量
                shortNetPosiCoin = d(amount + shortamount - longamount) * d(ctVal)  # 空仓，A’净持仓数量
                longNetPosiValue = d(markprice) * longNetPosiCoin  # 多仓，A标记价格 * A’净持仓数量
                shortNetPosiValue = d(markprice) * shortNetPosiCoin  # 空仓，A标记价格 * A’净持仓数量
                totalLongPosiCoin = d(longOpenCoin) + d(longamount) * d(ctVal)  # 多仓，A持仓数量 = 开仓数量 + 同向持仓数量
                totalShortPosiCoin = d(shortOpenCoin) + d(longamount) * d(ctVal)  # 空仓，A持仓数量 = 开仓数量 + 同向持仓数量
                # （A’净持仓数量 -【 A持仓数量 * （维持保证金率A + max（ 资金费率,0）+ taker手续费率A ）+ a持仓数量 * （维持保证金率a + max（资金费率,0）+ taker手续费率a）】）







    else:

        # if 'posLongValue' not in  othersymbolpos[symbol]: # 该下单币种没有持仓

        return

    # 逐仓--双向持仓--预估强平价

# 逐仓--双向持仓-预估强平价
def isolated_forecast_liquidation_price(NTS, symbol, price, amount, log_level=None):
    marginType = 'isolated'
    forecast_liquidation_price = {}
    aop = AOP(NTS, symbol, '2')
    OpenOrders = aop.OpenOrders[symbol][marginType]
    # markprice = param_dict.makrPriceMap[symbol]
    caseTitle = '逐仓双向--预估强平价'
    instrument = NTS.instrument
    ctVal = instrument[symbol]['ctVal']
    takerRate = instrument[symbol]['takerRate']
    funding = -0.0018830852
    trade_type = 81  # 正向永续业务线
    margin_type = 1  # 全仓=2，逐仓=1
    openCoin = d(amount) * d(ctVal)  # 开仓数量
    longOpenValue = 0
    shortOpenValue = 0
    longPosiValue = 0
    shortPosiValue = 0
    longPositionMargin = 0
    shortPositionMargin = 0
    if 'buy' in OpenOrders:
        longOpenValue = OpenOrders['buy']['value']
    if 'sell' in OpenOrders:
        shortOpenValue = OpenOrders['sell']['value']
    # 查询当前杠杆
    levr = NTS.leverageInfo(tradeType=linear_tradeType, symbol=symbol, marginType=marginType)
    if not e(levr)[0]:
        printc(caseTitle + '持仓查询失败,退出', levr['code'] + levr['message'])
        return False
    leverage = levr['data'][0]['leverage']
    # 查询正向永续全仓风险限额
    t_risk_limit = cal.t_risk_limit(trade_type, margin_type, symbol)
    # 获取市场 bid1 价格
    bid1 = 0  # todo 暂时默认给0
    # 查询当前币种持仓
    res = NTS.position(tradeType=linear_tradeType, symbol=symbol, log_level=log_level)
    # 如果查持仓接口失败，则退出
    if not e(res)[0]:
        printc(caseTitle + '持仓查询失败,退出', res['code'] + res['message'])
        return False
    LogOuts(NTS, caseTitle, LogName)
    res = res['data']
    if len(res) > 0:
        for tmp in res:
            if 'long' == tmp['positionSide']:
                longPosiValue = d(tmp['positionAmt']) * d(tmp['avgEntryPrice']) * d(ctVal)
                longPositionMargin = d(tmp['positionMargin'])
                posiCoin = d(tmp['positionAmt']) * d(tmp['avgEntryPrice'])
            if 'short' == tmp['positionSide']:
                shortPosiValue = d(tmp['positionAmt']) * d(tmp['avgEntryPrice']) * d(ctVal)
                shortPositionMargin = d(tmp['positionMargin'])
                posiCoin = d(tmp['positionAmt']) * d(tmp['avgEntryPrice'])

    if longPosiValue == 0:  # 没有多仓持仓
        longRiskLimit = d(price) * openCoin + longOpenValue  # 多仓风险限额
        long_maintenance_margin_rate = isolated_maintenance_margin_rate(longRiskLimit, t_risk_limit)  # 获取多仓价值维持保证金率
        longPpenMargin = (d(price) * openCoin / d(leverage)) + (d(price) * openCoin * d(takerRate))  # 委托保证金
        #  p * （持仓均价 * 持仓数量 + max（委托价格，bid1）* 开仓数量 ）
        longTotalValue = 1 * (longPosiValue + d(price) * openCoin)
        # 【 ( 维持保证金率 + max(p*资金费率,0) + taker手续费率 ) *（持仓数量 + 开仓数量）- p *（ 开仓数量 + 持仓数量) 】
        longWarningMargin = (d(long_maintenance_margin_rate) + d(max(1 * funding, 0)) + d(
            takerRate)) * openCoin - 1 * openCoin
        long_forecast_liquidation_price = (longPpenMargin - longTotalValue) / longWarningMargin  # 多仓预估强平价
        forecast_liquidation_price[symbol]['多仓预估强平价'] = long_forecast_liquidation_price

    else:  # 有多仓持仓
        longRiskLimit = d(price) * openCoin + longOpenValue + longPosiValue  # 多仓风险限额
        long_maintenance_margin_rate = isolated_maintenance_margin_rate(longRiskLimit, t_risk_limit)  # 获取多仓价值维持保证金率
        longPpenMargin = (d(price) * openCoin / d(leverage)) + (d(price) * openCoin * d(takerRate))  # 委托保证金
        #  p * （持仓均价 * 持仓数量 + max（委托价格，bid1）* 开仓数量 ）
        longTotalValue = 1 * (longPosiValue + d(price) * openCoin)
        # 【 ( 维持保证金率 + max(p*资金费率,0) + taker手续费率 ) *（持仓数量 + 开仓数量）- p *（ 开仓数量 + 持仓数量) 】
        longWarningMargin = (d(long_maintenance_margin_rate) + d(max(1 * funding, 0)) + d(takerRate)) * d(
            posiCoin + openCoin) - 1 * d(posiCoin + openCoin)
        long_forecast_liquidation_price = (
                                                      longPositionMargin + longPpenMargin - longTotalValue) / longWarningMargin  # 多仓预估强平价
        forecast_liquidation_price[symbol]['多仓预估强平价'] = long_forecast_liquidation_price

    if shortPosiValue == 0:  # 没有空仓持仓
        shortRiskLimit = d(price) * d(amount) * d(ctVal) + shortOpenValue  # 空仓风险限额
        short_maintenance_margin_rate = isolated_maintenance_margin_rate(shortRiskLimit, t_risk_limit)  # 获取空仓价值维持保证金率
        shortPpenMargin = (d(max(bid1, price)) * openCoin / d(leverage)) + (
                    d(max(bid1, price)) * openCoin * d(takerRate))  # 委托保证金
        #  p * （持仓均价 * 持仓数量 + max（委托价格，bid1）* 开仓数量 ）
        shortTotalValue = -1 * (shortPosiValue + max(price, bid1) * openCoin)
        # 【 ( 维持保证金率 + max(p*资金费率,0) + taker手续费率 ) *（持仓数量 + 开仓数量）- p *（ 开仓数量 + 持仓数量) 】
        shortWarningMargin = (d(short_maintenance_margin_rate) + d(max(-1 * funding, 0)) + d(takerRate)) * d(
            posiCoin + openCoin) - -1 * d(posiCoin + openCoin)
        short_forecast_liquidation_price = (shortPpenMargin - shortTotalValue) / shortWarningMargin  # 空仓预估强平价
        forecast_liquidation_price[symbol]['空仓预估强平价'] = short_forecast_liquidation_price

    else:  # 有空仓持仓
        shortRiskLimit = d(price) * d(amount) * d(ctVal) + shortOpenValue  # 空仓风险限额
        short_maintenance_margin_rate = isolated_maintenance_margin_rate(shortRiskLimit, t_risk_limit)  # 获取空仓价值维持保证金率
        shortPpenMargin = (d(max(bid1, price)) * openCoin / d(leverage)) + (
                    d(max(bid1, price)) * openCoin * d(takerRate))  # 委托保证金
        #  p * （持仓均价 * 持仓数量 + max（委托价格，bid1）* 开仓数量 ）
        shortTotalValue = -1 * (shortPosiValue + max(price, bid1) * openCoin)
        # 【 ( 维持保证金率 + max(p*资金费率,0) + taker手续费率 ) *（持仓数量 + 开仓数量）- p *（ 开仓数量 + 持仓数量) 】
        shortWarningMargin = (d(short_maintenance_margin_rate) + d(max(-1 * funding, 0)) + d(takerRate)) * d(
            posiCoin + openCoin) - -1 * d(posiCoin + openCoin)
        short_forecast_liquidation_price = (
                                                       shortPositionMargin + shortPpenMargin - shortTotalValue) / shortWarningMargin  # 空仓预估强平价
        forecast_liquidation_price[symbol]['空仓预估强平价'] = short_forecast_liquidation_price

    return forecast_liquidation_price


# list[0]=sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
# list[1]=sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
def OtherMaintMargin(symbol, otherSymbol, othersymbolpos):
    # sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
    # sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）
    otherList = []
    otherMaintMargin = 0
    otherPosUsdt = 0
    for i in range(0, len(otherSymbol)):
        if symbol != otherSymbol[i]:
            if 'long' not in othersymbolpos[otherSymbol[i]]:
                otherlongAmount = 0
            else:
                otherlongAmount = othersymbolpos[otherSymbol[i]]['long']

            if 'short' not in othersymbolpos[otherSymbol[i]]:
                othershortAmount = 0
            else:
                othershortAmount = othersymbolpos[otherSymbol[i]]['short']
            otherMarkPrice = othersymbolpos[otherSymbol[i]]['markprice']
            otherMaintenanceMarginRate = othersymbolpos[otherSymbol[i]]['maintenance_margin_rate']
            otherCtVal = othersymbolpos[otherSymbol[i]]['ctVal']
            otherFunding = othersymbolpos[otherSymbol[i]]['funding']
            TakerRate = othersymbolpos[otherSymbol[i]]['TakerRate']
            leverage = othersymbolpos[otherSymbol[i]]['leverage']
            otherMargin = d(otherMarkPrice) * d(otherlongAmount + othershortAmount) * \
                          d(otherMaintenanceMarginRate)  # 维持保证金
            otherfunding = d(otherMarkPrice) * d(otherlongAmount - othershortAmount) * d(otherCtVal) * d(
                otherFunding)  # 预付资金费
            otherfee = d(otherMarkPrice) * d(otherlongAmount + othershortAmount) * d(otherCtVal) * d(TakerRate)  # 强平手续费
            otherPosUsdt += d(otherMarkPrice) * d(otherlongAmount + othershortAmount) * d(otherCtVal) / d(
                leverage)  # sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
            otherMaintMargin += (otherMargin + otherfunding + otherfee)
            print(otherSymbol[
                      i] + f':\n 多仓仓位={otherlongAmount}，空仓仓位={othershortAmount},\n 当前杠杆对应的维持保证金率={otherMaintenanceMarginRate},标记价格={otherMarkPrice}'
                           f'\n 资金费率={otherFunding}, taker费率={TakerRate}，当前杠杆={leverage}'
                           f'\n 维持保证金={otherMargin}, 预付资金费={otherfunding},强平手续费={otherfee}'
                           f'\n (标记价格 * 持仓数量 / 杠杆 ）={d(otherMarkPrice) * d(otherlongAmount + othershortAmount) * d(otherCtVal) / d(leverage)}\n')
    otherList.append(otherMaintMargin)
    otherList.append(otherPosUsdt)
    print('sum其他交易对（维持保证金 + 预付资金费 + 强平手续费）=' + str(otherMaintMargin))
    print('sum各交易对（标记价格 * 持仓数量 / 杠杆 ）=' + str(otherPosUsdt))
    return otherList


# 合并基础数据
def mergeData(res, otherSymbol, instrument, t_risk_limit, marginType, NTS=None):
    funding = -0.0018830852
    othersymbolpos = {}
    for i in range(0, len(otherSymbol)):
        pos = {}
        for tmp in res:
            if tmp['symbol'] == otherSymbol[i] and tmp['marginType'] == marginType:
                if tmp['positionSide'] == 'long':
                    pos['long'] = int(tmp['positionAmt'])  # 多仓持仓数量
                    pos['long_posMargin'] = tmp['posMargin']  # 持仓保证金
                    pos['long_avgEntryPrice'] = tmp['avgEntryPrice']  # 持仓均价
                    pos['posLongValue'] = d(tmp['positionAmt']) * d(tmp['markPrice']) * d(
                        instrument[tmp['symbol'][:-4]][1])  # 多仓仓位价值
                if tmp['positionSide'] == 'short':
                    pos['short'] = int(tmp['positionAmt'])  # 空仓持仓数量
                    pos['short_posMargin'] = tmp['posMargin']  # 持仓保证金
                    pos['short_vgEntryPrice'] = tmp['avgEntryPrice']  # 持仓均价
                    pos['posShortValue'] = int(tmp['positionAmt']) * d(tmp['markPrice']) * d(
                        instrument[tmp['symbol'][:-4]][1])  # 空仓仓位价值
                pos['markprice'] = tmp['markPrice']  # 标记价格
                pos['leverage'] = tmp['leverage']  # 仓位杠杆
                pos['TakerRate'] = instrument[tmp['symbol'][:-4]][2]  # taker手续费率
                pos['MakerRate'] = instrument[tmp['symbol'][:-4]][3]  # maker手续费率
                pos['ctVal'] = instrument[tmp['symbol'][:-4]][1]  # 面值
                pos['funding'] = funding  # 资金费率
        othersymbolpos[otherSymbol[i]] = pos
    # 添加挂单价值
    if NTS != None:
        othersymbolpos = opensValue(NTS, othersymbolpos, marginType)
    # 添加仓位价值对应风险限额
    othersymbolpos = posRiskLimit(otherSymbol, othersymbolpos, t_risk_limit, marginType)

    return othersymbolpos


# 预警保证金
def warningMargin(symbol, othersymbolpos, funding):
    title = 'a持仓数量 * （维持保证金率a+max（ - 资金费率,0）+taker手续费率a'
    maintenanceMarginRate = othersymbolpos[symbol]['maintenance_margin_rate']
    TakerRate = othersymbolpos[symbol]['TakerRate']
    markPrice = othersymbolpos[symbol]['markprice']
    ctVal = othersymbolpos[symbol]['ctVal']
    WarningMargin = []
    longAmount = 0  # 多仓仓位
    longWarningMargin = 0  # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
    shortAmount = 0  # 空仓仓位
    shortWarningMargin = 0  # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
    if 'long' in othersymbolpos[symbol]:
        p = 1
        longAmount = othersymbolpos[symbol]['long']
        # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
        longWarningMargin = d(longAmount) * d(ctVal) * (
                d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
    if 'short' in othersymbolpos[symbol]:
        p = -1
        shortAmount = othersymbolpos[symbol]['short']
        # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
        shortWarningMargin = d(longAmount) * d(ctVal) * (
                d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))

    if longAmount > shortAmount:
        p = 1
        positionValue = d(p) * d(markPrice) * d(longAmount - shortAmount) * d(ctVal)  # A标记价格*A净持仓数量
        # p*A净持仓数量 - A持仓数量 * （维持保证金率A + max（ - 资金费率,0）+taker手续费率A ）
        currWarningMargin = d(p) * d(longAmount - shortAmount) - d(longAmount + shortAmount) * (
                d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
        WarningMargin.append('long')
        WarningMargin.append(positionValue)
        WarningMargin.append(currWarningMargin)
        WarningMargin.append(shortWarningMargin)
        print(title + f'\n 当前币种{symbol}的多仓仓位={longAmount},空仓仓位={shortAmount}，\n 反向预警保证金={shortWarningMargin}')
        return WarningMargin
    if shortAmount > longAmount:
        p = -1
        positionValue = d(p) * d(markPrice) * d(shortAmount - longAmount) * d(ctVal)  # A标记价格*A净持仓数量
        # p*A净持仓数量 - A持仓数量 * （维持保证金率A + max（ - 资金费率,0）+taker手续费率A ）
        currWarningMargin = d(p) * d(longAmount - shortAmount) - d(longAmount + shortAmount) * (
                d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
        WarningMargin.append('short')
        WarningMargin.append(positionValue)
        WarningMargin.append(currWarningMargin)
        WarningMargin.append(longWarningMargin)
        print(title + f'\n 当前币种{symbol}的多仓仓位={longAmount},空仓仓位={shortAmount}，\n 反向预警保证金={longWarningMargin}')

        return WarningMargin


# 获取开仓挂单价值
def opensValue(NTS, othersymbolpos, marginType, log_level=None):
    res = NTS.OpenOrders(tradeType=linear_tradeType, pageSize=100, pageNum=1)
    oporder = res['data']['list']
    if e(res)[0]:
        totalPage = res['data']['totalPage']
        if totalPage == 0:
            printl(log_level=log_level, title='UID:' + NTS.user_id + ',' + '合约没有当前委托')
            return othersymbolpos
        else:
            for op in oporder:
                if op['marginType'] == marginType:
                    # 判断时候在持仓交易对里，判断是否为开仓的订单
                    if op['symbol'] in othersymbolpos and op['side'] == 'buy' and op['positionSide'] == 'long':
                        if 'openlongvalue' not in othersymbolpos[op['symbol']].keys():
                            othersymbolpos[op['symbol']]['openlongvalue'] = d(op['leavesQty']) * d(op['price']) * d(
                                othersymbolpos[op['symbol']]['ctVal'])
                        else:
                            othersymbolpos[op['symbol']]['openlongvalue'] += d(op['leavesQty']) * d(op['price']) * d(
                                othersymbolpos[op['symbol']]['ctVal'])
                    if op['symbol'] in othersymbolpos and op['side'] == 'sell' and op['positionSide'] == 'short':
                        if 'openshortvalue' not in othersymbolpos[op['symbol']].keys():
                            othersymbolpos[op['symbol']]['openshortvalue'] = d(op['leavesQty']) * d(op['price']) * d(
                                othersymbolpos[op['symbol']]['ctVal'])
                        else:
                            othersymbolpos[op['symbol']]['openshortvalue'] += d(op['leavesQty']) * d(op['price']) * d(
                                othersymbolpos[op['symbol']]['ctVal'])
            if totalPage > 1:
                for i in range(2, totalPage + 1):
                    res = NTS.OpenOrders(tradeType=linear_tradeType, pageSize=100, pageNum=i)
                    res = res['data']['list']
                    for tmp in res:
                        if tmp['marginType'] == marginType:
                            # 判断时候在持仓交易对里，判断是否为开仓的订单
                            if tmp['symbol'] in othersymbolpos and tmp['side'] == 'buy' and tmp[
                                'positionSide'] == 'long':
                                if 'openlongvalue' not in othersymbolpos[oporder[i]['symbol']].keys():
                                    othersymbolpos[tmp['symbol']]['openlongvalue'] = tmp['leavesQty'] * tmp['price'] * \
                                                                                     othersymbolpos[tmp['symbol']][
                                                                                         'ctVal']
                                else:
                                    othersymbolpos[tmp['symbol']]['openlongvalue'] += tmp['leavesQty'] * tmp['price'] * \
                                                                                      othersymbolpos[tmp['symbol']][
                                                                                          'ctVal']
                            if tmp['symbol'] in othersymbolpos and tmp[i]['side'] == 'sell' and tmp[
                                'positionSide'] == 'short':
                                if 'openshortvalue' not in othersymbolpos[tmp['symbol']].keys():
                                    othersymbolpos[tmp['symbol']]['openshortvalue'] = tmp['leavesQty'] * tmp['price'] * \
                                                                                      othersymbolpos[tmp['symbol']][
                                                                                          'ctVal']
                                else:
                                    othersymbolpos[tmp['symbol']]['openshortvalue'] += tmp['leavesQty'] * tmp['price'] * \
                                                                                       othersymbolpos[tmp['symbol']][
                                                                                           'ctVal']
    return othersymbolpos


# 获取仓位价值对应的风险限额
def posRiskLimit(otherSymbol, symbolpos, t_risk_limit, marginType):
    for i in range(0, len(otherSymbol)):
        posLongValue = 0
        posShortValue = 0
        openlongvalue = 0
        openshortvalue = 0
        if 'posLongValue' in symbolpos[otherSymbol[i]]:
            posLongValue = symbolpos[otherSymbol[i]]['posLongValue']
        if 'posShortValue' in symbolpos[otherSymbol[i]]:
            posShortValue = symbolpos[otherSymbol[i]]['posShortValue']
        if 'openlongvalue' in symbolpos[otherSymbol[i]]:
            openlongvalue = symbolpos[otherSymbol[i]]['openlongvalue']
        if 'openshortvalue' in symbolpos[otherSymbol[i]]:
            openshortvalue = symbolpos[otherSymbol[i]]['openshortvalue']
        if marginType == 'cross':
            Value = max(d(posLongValue) + d(openlongvalue), d(posShortValue) + d(openshortvalue))
            for tmp in t_risk_limit:
                if otherSymbol[i] == tmp[0] and float(Value) <= tmp[1]:
                    symbolpos[otherSymbol[i]]['maintenance_margin_rate'] = float(tmp[2])
                    break
        else:
            longValue = d(posLongValue) + d(openlongvalue)
            shortValue = d(posShortValue) + d(openshortvalue)
            for tmp in t_risk_limit:
                if posLongValue > 0:
                    if otherSymbol[i] == tmp[0] and float(longValue) <= tmp[1]:
                        symbolpos[otherSymbol[i]]['isolated_long_maintenance_margin_rate'] = float(tmp[2])
                        break
                if posShortValue > 0:
                    if otherSymbol[i] == tmp[0] and float(shortValue) <= tmp[1]:
                        symbolpos[otherSymbol[i]]['isolated_short_maintenance_margin_rate'] = float(tmp[2])
                        break
    return symbolpos


# 查询持仓有哪些币种
def postionSymbol(res, marginType):
    caseTitle = '获取当前币种持仓,'
    otherSymbol = []

    # 如果查持仓接口失败，则退出
    if not e(res)[0]:
        printc(caseTitle + '持仓查询失败,退出', res['code'] + res['message'])
        return False
    res = res['data']
    if len(res) > 0:
        for i in range(0, len(res)):
            if res[i]['marginType'] == marginType:
                if res[i]['symbol'] not in otherSymbol:
                    otherSymbol.append(res[i]['symbol'])
        return otherSymbol
    else:
        printc(caseTitle + f'该uid:{NTS.user_id}没有持仓，退出' + res['data'])
        return False


# 强制减仓费用
def mandatoryReducePositionsFee(marginType, liquidationList):
    # 如果是逐仓，需要在平仓保证金中收取，强制减仓费=min（平仓保证金，减仓数量*成交价格*爆仓费率）
    # 平仓保证金=平仓数量*开仓价格/杠杆 + （平仓价格-开仓价格）*平仓数量 + I手续费I
    # 全仓，各个交易对按成交顺序收取，强制减仓费=min（账户剩余权益，减仓数量*成交价格*爆仓费率）
    if marginType == 'isolated':
        liquidationFee = d(liquidationList['closePositionAmt']) * d(liquidationList['avgPrice']) * d(
            liquidationList['liquidationReta'])
        fee = d(liquidationList['closePositionAmt']) * d(liquidationList['closePrice']) * d(
            liquidationList['TakerReta'])
        Profit = (d(liquidationList['closePrice']) - d(liquidationList['openPrice'])) * d(
            liquidationList['closePositionAmt'])
        closePosMaegin = d(liquidationList['closePositionAmt']) * d(liquidationList['openPrice']) / d(
            liquidationList['leverage']) + Profit + fee
        ReducePositionsFee = min(closePosMaegin, liquidationFee)
        return ReducePositionsFee
    else:
        for tmp in liquidationList:
            remainInterests = tmp['remainInterests']


# 计算减仓后动态维持保证金，#单合约单方向持仓专用，风险限额对应维持保证金率
def dynamicMarginMaintenance(t_risk_limit, interests=None, positions=None):
    t_risk_limit_interests = {}
    step = d(t_risk_limit[1][0]) - d(t_risk_limit[0][0])
    t_risk_limit_interests['step'] = step
    if positions != None:
        posValue = d(positions['avgEntryPrice']) * d(positions['positionAmt']) * d(positions['ctVal'])
        for tmp in t_risk_limit:
            if float(posValue) <= tmp[0]:
                t_risk_limit_interests['maintenance_margin_rate'] = float(tmp[1])
                t_risk_limit_interests['t_risk_limit_grade'] = float(tmp[2])
                t_risk_limit_interests['N_value_limit'] = float(tmp[0])
                break
    if interests != None:
        for tmp in t_risk_limit:
            if float(interests) <= tmp[3]:
                t_risk_limit_interests['interests_grade'] = float(tmp[2])
                t_risk_limit_interests['M_value_limit'] = float(tmp[0])
                break

    return t_risk_limit_interests


# 预估预警保证金 （给预估强平价用的）
def foreCastWarningMargin(symbol, othersymbolpos, side, amount):
    # p * A’净持仓数量 -【 A持仓数量 * （维持保证金率A + max（ p * 资金费率,0）+ taker手续费率A ）+ a持仓数量 * （维持保证金率a + max（ p * 资金费率,0）+ taker手续费率a）】）
    maintenanceMarginRate = othersymbolpos[symbol]['maintenance_margin_rate']
    TakerRate = othersymbolpos[symbol]['TakerRate']
    markPrice = othersymbolpos[symbol]['markprice']
    ctVal = othersymbolpos[symbol]['ctVal']
    funding = -0.0018830852
    warningMargin = []
    longAmount = 0
    shortAmount = 0
    reverseWarningMargin = 0  # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
    if 'long' in othersymbolpos[symbol]:
        longAmount = othersymbolpos[symbol]['long']

    if 'short' in othersymbolpos[symbol]:
        shortAmount = othersymbolpos[symbol]['short']
    if side == 'buy' and shortAmount != 0:
        p = -1
        # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
        reverseWarningMargin = d(shortAmount) * d(ctVal) * (
                    d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
    if side == 'sell' and longAmount != 0:
        p = 1
        # a持仓数量 * （维持保证金率a + max（ - 资金费率, 0）+taker手续费率a）
        reverseWarningMargin = d(longAmount) * d(ctVal) * (
                    d(maintenanceMarginRate) + max(p * funding, 0) + d(TakerRate))

    # A持仓数量 = 开仓数量 + 同向持仓数量
    # A'净持仓数量 = 本次开仓数量 + 同向持仓数量 - 反向持仓数量
    # p * A标记价格 * A’净持仓数量
    if side == 'buy':
        p = 1
        totalLongAmount = longAmount + amount  # A持仓数量 = 开仓数量 + 同向持仓数量
        netLongAmount = totalLongAmount - shortAmount  # A’净持仓数量
        WarningMargin = d(totalLongAmount) * d(ctVal) * (
                    d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
        newWarningMargin = p * netLongAmount - (reverseWarningMargin + WarningMargin)
        netPosition = p * markPrice * netLongAmount  # p * A标记价格 * A’净持仓数量
        warningMargin.append(newWarningMargin)
        warningMargin.append(netPosition)

    else:
        p = -1
        totalLongAmount = shortAmount + amount
        netLongAmount = totalLongAmount - longAmount
        WarningMargin = d(totalLongAmount) * d(ctVal) * (
                    d(maintenanceMarginRate) + d(max(p * funding, 0)) + d(TakerRate))
        newWarningMargin = p * netLongAmount - (reverseWarningMargin + WarningMargin)
        netPosition = p * markPrice * netLongAmount  # p * A标记价格 * A’净持仓数量
        warningMargin.append(newWarningMargin)
        warningMargin.append(netPosition)

    return warningMargin
#sum各交易对（标记价格 * 持仓数量 / 杠杆 ）
def sumSymbolValue(res,instrument):
    totalSymbolUsdt = 0
    for tmp in res:
        totalSymbolUsdt += d(tmp['avgEntryPrice']) * d(tmp['positionAmt']) * d(instrument[tmp['symbol'][:-4]][1]) / d(tmp['leverage'])


    return totalSymbolUsdt





# 逐仓预估强平价获取维持保证金率
def isolated_maintenance_margin_rate(RiskLimit, t_risk_limit):
    for i in t_risk_limit:
        if RiskLimit <= t_risk_limit[i][0]:
            maintenance_margin_rate = t_risk_limit[i][1]
            return maintenance_margin_rate


if __name__ == '__main__':
    NTS = n_order(5, user_id='99999')
    print(cross_liquidation_price(NTS))
