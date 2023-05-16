from BU.NTS.ApiOrder import NtsApiOrder
import copy
import BU.NTS.dataCheck.dataCheck as dataCheck
import case.other.UserDataCheck as UserDataCheck
import BU.NTS.Calculator as cal
from BU.NTS.WebOrder import n_order
from param.dict import cumQty, avgPrice, lastPrice, leavesQty, base, linear_tradeType, side, positionSide, price
import BU.NTS.comm.params as PAR
import common.util as ut
import common.other as other
from common.other import httpCheck as e
from common.util import truncate, printc, printl, d, Count, decimalLength
from BU.NTS.dataCheck.dataCheck import newPrice

tradeType = 'linearPerpetual'
marginType = 'cross'


# taker平仓变maker
def closePositionTakerTomaker(NTS, symbol, Side, log_level=None, takerFlag=None):
    ThisCaseNumber = 9;
    if Side == 'buy': Position = 'short';Position_Name = '空仓';faceSide = 'sell';facePositionSide = 'short';PriceX=1
    if Side == 'sell': Position = 'long';Position_Name = '多仓';faceSide = 'buy';facePositionSide = 'long';PriceX=-1
    if takerFlag:
        tradeName = 'taker';newTradeName='taker变maker'
    else:
        tradeName = 'maker'
    caseTitle = '<全仓双向 平仓全部成交，taker变maker>';
    S = 0;
    caseMark = 1;
    symbol_ = symbol + 'USDT';
    printl(log_level, '  场景：' + caseTitle+f'平{Position_Name}{tradeName}')
    ins = NTS.instrument[symbol];
    TakerRate = ins[2]
    MakerRate = ins[3]
    ctVal = ins[1]
    TickSize = ins[0]
    postionList = {}
    NTS_FACE = n_order(6, user_id=97201972)
    for_number = 3
    r1 = NTS.position(log_level=0, tradeType=linear_tradeType, symbol=symbol_)
    if not e(r1)[0]:
        printc(caseTitle + f'{Position_Name}持仓查询失败,退出', r1['code'] + r1['message']);
        Count(caseTitle, ThisCaseNumber, 0, ThisCaseNumber, 0);
        return False;
    S = S + 1;
    printl(log_level, str(S) + f'{Position_Name}初始持仓 查询成功.' );
    Count(caseTitle, 1, 1, 0, 0);
    for tmp in r1['data']:
        postionList[tmp['positionSide']] = [tmp['positionAmt'], tmp['availPos'], tmp['avgEntryPrice']]
    if Position in str(postionList):
        if float(postionList[Position][1]) >= 9:
            caseMark = 1
        else:
            printc(caseTitle + f'{Position_Name}持仓<9,退出');
            Count(caseTitle, ThisCaseNumber - 1, 0, 1, ThisCaseNumber - 2);
            caseMark = 0;
            return False;
    else:
        printc(caseTitle + f'{Position_Name}持仓数据为空，退出');
        Count(caseTitle, ThisCaseNumber - 1, 0, 1, ThisCaseNumber - 2);
        caseMark = 0;
        return False;
    S = S + 1;
    printl(log_level, str(S) + f'{Position_Name}持仓 持仓量>=9 验证成功.' );
    Count(caseTitle, 1, 1, 0, 0);
    if caseMark:
        OrderPrice = newPrice(NTS, symbol, _type=3)
        OrderPriceList=[];OrderIdList=[];makerOrder_res_List=[]
        for i in range(for_number):
            OrderPriceList.append(truncate(float(OrderPrice) + float(TickSize) * (i) * PriceX, decimalLength(TickSize)))

        # 复制固定参数
        caseParam = copy.deepcopy(PAR.linear_cross_param);
        orderQty = 2
        totalorderQty=for_number*2
        #要下单的参数
        paramList = [[side, Side], [positionSide, Position], [price, str(OrderPrice)], ['symbol', symbol_],['orderQty', str(orderQty)]]
        for p in paramList:
            # 如果p[1]的值不为空，就添加到固定参数里，得到要下单到全部参数
            if p[1]:
                caseParam[p[0]] = p[1]
        # 如果是taker单，对手方先挂单，然后自己再去吃单
        if takerFlag:

            for i in range(len(OrderPriceList)):
                caseParamFace = copy.deepcopy(caseParam)
                caseParamFace['price'] = OrderPriceList[i]
                caseParamFace[side] = faceSide;
                caseParamFace[positionSide] = facePositionSide;
                # 对手方先挂单单
                makerOrder_r = NTS_FACE.order(log_level=log_level, caseParam=caseParamFace)
                if not e(makerOrder_r)[0]:
                    printc(caseTitle + f'{Position_Name}平仓  对手方挂单 失败', makerOrder_r)
                    Count(caseTitle, ThisCaseNumber - 2, 0, 1, ThisCaseNumber - 3)
                    return False
                S = S + 1
                printl(log_level, str(S) + f'{Position_Name}平仓  对手方挂单 成功.' )
                Count(caseTitle, 1, 1, 0, 0)
            caseParam['price'] = OrderPriceList[i];caseParam[side]=Side;caseParam[positionSide]=Position;caseParam['orderQty']=9
            # 自己去吃单
            print('taker下单价格='+str(caseParam['price']))
            takerOrder_r = NTS.order(log_level=log_level, caseParam=caseParam, orderQty=9)
            if not e(takerOrder_r)[0]:
                printc(caseTitle + f'{Position_Name}平仓{tradeName}下单失败 ,退出 ', takerOrder_r['message'])
                ut.otherCase['全部平仓'] = {"pass": 0, "fail": 1, "block": 10}
                return False
            else:
                OrderIdList.append(takerOrder_r['data']['orderId']);
                makerOrder_res_List.append(takerOrder_r);S = S + 1;
                S = S + 1
                printl(log_level, str(S) + f'{Position_Name}平仓 下单{tradeName}成功.' ,' ' + str(takerOrder_r['data']['orderId']) + '  ' + str(OrderPrice))
                Count(caseTitle, 1, 1, 0, 0)

        openFlag = True
        priceAll = 0;
        Commission_ = 0;
        profit_ = 0;
        TradeData = []
        for i in OrderPriceList:
            priceAll = priceAll + float(i)
            Commission = d(TakerRate) * d(i) * d(orderQty) * d(ctVal)
            Commission_ = Commission_ + Commission
            profit = cal.UnRealisePnl(Position, str(i), postionList[Position][2], orderQty, ctVal)
            profit_ = profit_ + profit
            TradeData.append([i, profit - Commission, Commission, profit])
        RealProfit = profit_ - Commission_
        # Profit = profit_
        # print(Commission_,profit_,profit_-Commission_)
        # 计算成交均价
        AvgPrice = float(priceAll / OrderPriceList.__len__())
        if takerFlag:
            # newAvgPrice=cal.avgPrice(uid=NTS.user_id,orderId=OrderIdList[0])
            res=NTS.OpenOrders(tradeType=tradeType, orderId=OrderIdList[0])['data']['list'][0]
            Commission = d(TakerRate) * d(res['avgPrice']) * d(res['cumQty']) * d(ctVal)  # taker 试算手续费
            OrderStatus = 'partially_filled'  # taker  当前委托 订单状态为部分成交
            paramListAssert = [['orderStatus',OrderStatus],['commission',Commission],[cumQty, str(totalorderQty)],[lastPrice, d(caseParam['price'])],[avgPrice, d(AvgPrice)],[leavesQty, str(3)],['orderQty', str(9)]]  #taker时，成交6张，剩余3张
            if NTS.source=='web':
                paramListAssert = [['orderStatus', OrderStatus], ['commission', Commission], [cumQty, str(totalorderQty)],[lastPrice, d(caseParam['price'])],[base, symbol] ,[avgPrice, d(AvgPrice)], [leavesQty, str(3)],['orderQty', str(9)]]  # taker时，成交6张，剩余3张

        # 当前委托验证
        openOrderResult = dataCheck.OrderRelateCheck(NTS, takerOrder_r, caseTitle + ' 当前委托', 0,
                                                     param=[caseParam, paramListAssert], _type='OpenOrder',
                                                     openFlag=openFlag)
        if openOrderResult:
            S = S + 1
            printl(log_level, str(S) + f'{Position_Name}平仓 {tradeName}下单后 当前委托数据验证成功.' );
            Count(caseTitle, 1, 1, 0, 0);
        # 验持仓
        r1 = NTS.position(log_level=0, tradeType=linear_tradeType, symbol=symbol_)
        if not e(r1)[0]:
            printc(caseTitle + '持仓查询失败,退出')
            ut.otherCase['全部平仓'] = {"pass": 0, "fail": 1, "block": 10}
            return False
        for i in r1['data']:
            if i['positionSide'] == Position:
                if not takerFlag:  # maker订单时，持仓数量不变，可用数量变小
                    if i['positionAmt'] == postionList[Position][0] and float(i['availPos']) == float(postionList[Position][1]) - float(totalorderQty):
                        S = S + 1
                        printl(log_level, str(S) + f'{Position_Name}平仓 {tradeName}下单后 持仓数据验证成功.' )
                        Count(caseTitle, 1, 1, 0, 0)
                    else:
                        printc(str(S) + f'{Position_Name}平仓 {tradeName}下单后 持仓数据验证失败. 预期 ',[postionList[Position][0], float(postionList[Position][1]) - float(totalorderQty)], ' 实际 ',i['positionAmt'], i['availPos'])
                        Count(caseTitle, 1, 0, 1, 0)
                else:  # taker 订单时，持仓数量和可用数量 同时变小
                    if float(i['positionAmt']) == float(postionList[Position][0]) - float(totalorderQty) and float(i['availPos']) == float(postionList[Position][1]) - float(caseParam['orderQty']):
                        S = S + 1
                        printl(log_level, str(S) + f'{Position_Name}平仓 {tradeName}下单后 持仓数据验证成功.' )
                        Count(caseTitle, 1, 1, 0, 0)
                    else:
                        printc(str(S) + f'{Position_Name}平仓 {tradeName}下单后 持仓数据验证失败. 预期 ',[float(postionList[Position][0]) - float(totalorderQty), float(postionList[Position][1]) - float(totalorderQty)], ' 实际 ',i['positionAmt'], i['availPos'])
                        Count(caseTitle, 1, 0, 1, 0)
        # 历史委托数据 计算
        Leverage_r = NTS.leverage_info(tradeType=PAR.linear_cross_param['tradeType'], symbol=symbol_, marginType='cross')
        Leverage = Leverage_r['data'][0]['leverage']
        if takerFlag:
            Rate=TakerRate
            number = 0
        for i in range(len(TradeData)):
            index =len(TradeData) - i - 1
            number = number + 1
            OrderPrice=TradeData[index][0]
        # 历史成交数据 计算
            Commission = d(Rate) * d(TradeData[index][0]) * d(orderQty) * d(ctVal)  # taker 试算手续费
            paramList_Trade = [[side, Side], [positionSide, Position],['symbol', symbol_],['clOrdId',''], ['filledQty', d(orderQty)],['filledPrice',d(OrderPrice)],['tradeId',str],['realProfit',TradeData[index][1]],['commission',Commission]]
            caseParam_Trade=other.OrderRelateInstall(_type='HisTrade',ParamList=paramList_Trade,OrderPrice=OrderPrice)
            openOrderResult = dataCheck.OrderRelateCheck(NTS, takerOrder_r, caseTitle + ' 历史成交', 0,caseParam['tradeType'], symbol=symbol_, param=caseParam_Trade,_type='HisTrade',Number=number,AllNumber=for_number)


            if openOrderResult:
                S=S+1;printl(log_level,str(S)+f'{Position_Name}平仓成交后 查询成交订单数据 验证成功')
                Count(caseTitle,1,1,0,0);
            else:
                printc(caseTitle + f'{Position_Name}平仓成交后 查询历史成交数据 验证失败')
                Count(caseTitle, 1, 0, 1, 0);

        #剩下的平仓单变成maker，被对手方taker掉
        caseParam['orderQty'] = int(postionList[Position][0]) - int(totalorderQty)
        caseParam['side'] = faceSide
        caseParam['positionSide'] = facePositionSide
        caseParamFace=copy.deepcopy(caseParam)
        face_takerOrder_r=NTS_FACE.order(log_level=log_level, caseParam=caseParamFace)
        if not e(face_takerOrder_r)[0]:
            printc(caseTitle + f'{Position_Name}平仓  对手方吃单 失败', face_takerOrder_r)
            Count(caseTitle, ThisCaseNumber - 2, 0, 1, ThisCaseNumber - 3)
            return False
        S = S + 1
        printl(log_level, str(S) + f'{Position_Name}平仓  对手方吃单 成功.' )
        Count(caseTitle, 1, 1, 0, 0)

        #验证当前委托
        openOrder=NTS.OpenOrders(tradeType=tradeType, symbol=symbol_, log_level=log_level)
        if not e(openOrder)[0]:
            printc(caseTitle + '当前委托查询失败,退出')
            ut.otherCase['taker变maker全部平仓'] = {"pass": 0, "fail": 1, "block": 1}
        if len(openOrder['data']['list'])>0 and openOrder['data']['list'][0]['side']==faceSide and openOrder['data']['list'][0]['positionSide']==facePositionSide:
            printl(log_level, caseTitle + f'{Position_Name}平仓 {tradeName}被吃单后 当前委托数据验证失败.');
            Count(caseTitle, 1, 0, 1, 0);
        else:
            S = S + 1
            printl(log_level, str(S) + f'{Position_Name}平仓 {tradeName}被吃单后 当前委托数据验证成功.' );
            Count(caseTitle, 1, 1, 0, 0);

        #验证持仓
        pos=NTS.position(tradeType=tradeType,symbol=symbol_,log_level=log_level)
        if not e(pos)[0]:
            printc(caseTitle + '持仓查询失败,退出')
            ut.otherCase['taker变maker全部平仓'] = {"pass": 0, "fail": 1, "block": 1}
            return False
        if len(pos['data']) > 0 and pos['data'][0]['positionSide'] == facePositionSide:
            printl(log_level, caseTitle + f'{Position_Name}平仓 {tradeName}被吃单后 持仓数据验证失败.');
            Count(caseTitle, 1, 0, 1, 0);
        else:
            S = S + 1
            printl(log_level, str(S) + f'{Position_Name}平仓 {tradeName}被吃单后 持仓数据验证成功.' );
            Count(caseTitle, 1, 1, 0, 0);

        #验证历史委托
        #试算手续费
        fee = d(caseParam['price']) * d(caseParam['orderQty']) * d(ctVal) * d(MakerRate)
        totalfee=Commission_ + fee
        newAvgPrice=(d(AvgPrice)*d(totalorderQty)+d(caseParam['price'])*d(caseParam['orderQty']))/ (d(9))
        profit = cal.UnRealisePnl(side=Position,markPrice=caseParam['price'], avgEntryPrice=postionList[Position][2], positionAmt=orderQty, ctVal=ctVal)
        newRealProfit=d(RealProfit)+(d(profit)-d(fee))
        caseParamAssert=copy.deepcopy(PAR.linear_cross_param)
        caseParamAssert[side]=Side;caseParamAssert[positionSide]=Position;caseParamAssert['symbol']=symbol_;caseParamAssert['filledQty']=d(caseParam['orderQty']);caseParamAssert['orderQty']=d(d(totalorderQty)+d(caseParam['orderQty']));
        caseParamAssert['cumQty'] = d(d(totalorderQty)+d(caseParam['orderQty']));caseParamAssert['commission'] = d(totalfee);caseParamAssert['lastPrice'] = d(caseParam['price']);caseParamAssert['price'] = caseParam['price'];
        caseParamAssert['avgPrice'] =newAvgPrice;caseParamAssert['realProfit'] =newRealProfit;
        openOrderResult = dataCheck.OrderRelateCheck(NTS, takerOrder_r, caseTitle + ' 历史订单', 0, param=caseParamAssert, _type='HisOrder',openFlag=True)
        if openOrderResult:
            S=S+1
            printl(log_level,str(S)+f' 下{newTradeName}{Position_Name}平仓单后 查询历史订单无数据 验证成功')
            Count(caseTitle,1,1,0,0)
        else:
            printc(  f'下{newTradeName}{Position_Name}平仓单后 查询历史订单无数据 验证失败')
            Count(caseTitle,1,0,1,0)

        #验证历史成交
        new_paramList_Trade = [[side, Side], [positionSide, Position], ['symbol', symbol_], ['clOrdId', ''],
                           ['filledQty', d(caseParam['orderQty'])], ['filledPrice', str(d(caseParam['price']))], ['tradeId', str],
                           ['realProfit', profit], ['commission', fee],['taker',False]]
        new_caseParam_Trade = other.OrderRelateInstall(_type='HisTrade', ParamList=new_paramList_Trade,
                                                   OrderPrice=caseParam['price'])

        openOrderResult = dataCheck.OrderRelateCheck(NTS, takerOrder_r, caseTitle + ' 历史成交', 0, caseParam['tradeType'],
                                                     symbol=symbol_, param=new_caseParam_Trade, _type='HisTrade')
        if openOrderResult:
            S = S + 1;
            printl(log_level, str(S) + f'{Position_Name}平仓成交后 查询成交订单数据 验证成功' )
            Count(caseTitle, 1, 1, 0, 0);
        else:
            printc(str(S) + f'{Position_Name}平仓成交后 查询历史成交数据 验证失败')
            Count(caseTitle, 1, 0, 1, 0);


        # 流水数据 计算
        # print(realProfit_1, Commission)
        hisAccounts_assert=dataCheck.OrderRelateCheck(NTS,True,Accounts=[newRealProfit,totalfee],_type='HisAccount',symbol=symbol_)
        if hisAccounts_assert:
            S=S+1
            printl(log_level,str(S) + f'{Position_Name}平仓成交后 流水验证成功 ');Count(caseTitle,1,1,0,0);
        else :
            printc(str(S)+f'{Position_Name}平仓成交后 查询流水 验证失败');Count(caseTitle, 1, 0, 1, 0);

        #进行仓位、资金数据公式验证
        DataCheckResult=UserDataCheck.UsderDataCheckCase(NTS, log_level,option='23',title=caseTitle+f'{Position_Name}+{tradeName}')
        Count(caseTitle, 2, DataCheckResult, 2-DataCheckResult, 0);


if __name__ == '__main__':
    NTS = NtsApiOrder(6, user_id='10070')
    print(closePositionTakerTomaker(NTS, symbol='BTC', Side='buy', log_level=2, takerFlag=True))
