import copy, random
import time

from BU.NTS.BasicData import BasicData as BD
import common.mysqlClient as mysql
from BU.NTS.comm.userData import face_user
from BU.NTS.WebOrder import n_order
from common.asserts import compare
import param.dict as dict
# from BU.NTS.NtsApiOrder import NtsApiOrder as n_order
from common import mysqlClient
from param.dict import linear_tradeType
from common.other import httpCheck as e
from common.util import truncate, printc, printl, d, t as _t,countCaseNumber as u
import BU.NTS.BasicData as basic
import BU.NTS.Calculator as cal
import BU.NTS.comm.params as par

log_level = 0
thisCaseNumber = 0
tradeType = 'linearPerpetual';
symbol = 'BTCUSDT'
currency = 'USDT'
pageNum = 1
pageSize = 100
t = mysqlClient.mysql(7)
def OrderRelateCheck(NTS,r=None,caseTitle='',log_level=0,openFlag=True,param=None,_type=None,Accounts=None,symbol=None,openPositionFlag=None,Number=None,AllNumber=None):
    if not r : r_status=e(r)[0]
    else: r_status=r
    if _type=='OpenOrder':
        orderParam=param[0];paramListAssert=param[1]
        openOrderAssert = copy.deepcopy(par.OpenOrderAssert);caseParamAssert = copy.deepcopy(orderParam)
        if NTS.source=='API':
            del openOrderAssert['base']
            del openOrderAssert['quote']
        caseParamAssert.update(openOrderAssert)
        for p1 in paramListAssert:
            caseParamAssert[p1[0]] = p1[1]
    if _type in ['HisOrder','HisTrade']:
        caseParamAssert=param
    if _type == 'HisAccount':
        hisAccounts_r = NTS.hisAccounts(tradeType=linear_tradeType, symbol=symbol)
        realProfit_compareResult=False;fee_compareResult=False
        accounts={};openAccount={'openFee':[]}
        if openPositionFlag:
            openAccount['openFee'].append(hisAccounts_r['data']['list'][0]['income'])
            openAccount['openFee'].append(hisAccounts_r['data']['list'][0]['income'])
            a_fee = copy.deepcopy(par.HisAccountAssert)
            a_fee['incomeType'] = 'openFee';
            a_fee['income'] = Accounts[1]
            fee_compareResult0 = compare(a_fee, hisAccounts_r['data']['list'][0], title=caseTitle, New=1);
            fee_compareResult1 = compare(a_fee, hisAccounts_r['data']['list'][0], title=caseTitle, New=1);
            if fee_compareResult0 or fee_compareResult1: return True
            return False
        else:
            accounts[hisAccounts_r['data']['list'][0]['incomeType']]=hisAccounts_r['data']['list'][0]['income']
            accounts[hisAccounts_r['data']['list'][1]['incomeType']]=hisAccounts_r['data']['list'][1]['income']
            a_realProfit=copy.deepcopy(par.HisAccountAssert)
            a_fee = copy.deepcopy(par.HisAccountAssert)
            a_realProfit['incomeType']='realProfit';a_realProfit['income']=Accounts[0]
            a_fee['incomeType'] = 'closeFee';a_fee['income'] = Accounts[1]
            # print(a_realProfit,a_fee)  #调试代码
            # print(hisAccounts_r['data']['list'][0]) #调试代码
            # print(hisAccounts_r['data']['list'][1])#调试代码
            if hisAccounts_r['data']['list'][0]['incomeType']=='realProfit':
                realProfit_compareResult = compare(a_realProfit, hisAccounts_r['data']['list'][0], title=caseTitle+' realProfit ', New=1);
            else:
                fee_compareResult = compare(a_fee, hisAccounts_r['data']['list'][0], title=caseTitle+' closeFee ', New=1);

            if hisAccounts_r['data']['list'][1]['incomeType'] == 'closeFee':
                fee_compareResult = compare(a_fee, hisAccounts_r['data']['list'][1], title=caseTitle+' closeFee ', New=1);
            else:
                realProfit_compareResult = compare(a_realProfit, hisAccounts_r['data']['list'][1], title=caseTitle+' realProfit ', New=1);

            if realProfit_compareResult and fee_compareResult: return True
            else:return False

    if r_status:
        order_id = r['data']['orderId'];
        OrderRelateResult = check.isExit_Order(NTS, order_id,openFlag=openFlag,param=caseParamAssert,_type=_type,openPositionFlag=openPositionFlag,caseTitle=caseTitle,Number=Number,AllNumber=AllNumber)
        caseResult=OrderRelateResult
        # if openOrdersCheckResult:printl(log_level,caseTitle + ' 验证成功.');u(1);caseResult = 1; #, all=0,pass_=0
        # else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0);caseResult = 0;
    else:   caseResult = False
    return caseResult

def openOrdersChecks(NTS,r,Flag,caseTitle,log_level, tradeType=None, symbol=None,openFlag=True,param=None,_type=None):
    r_status=e(r)[0]
    if not r_status: u(0, block=1);
    if r_status and Flag:
        order_id = r['data']['orderId']
        openOrdersCheckResult = check.isExit_openOrders(NTS, tradeType, symbol, order_id, openFlag=openFlag, log_level=log_level, param=param, _type=_type)
        if openOrdersCheckResult:printl(log_level,caseTitle + ' 验证成功.');u(1);caseResult = 1;
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0);caseResult = 0;
    else:   caseResult = False
    return caseResult

# 资金流水数据校验
def accountIncomeChecks(NTS, r, Flag, caseTitle, log_level, tradeType, symbol, openFlag=True):
    r_status=e(r)[0]
    if not r_status: u(0, block=1);
    if r_status and Flag:
        openOrdersCheckResult = check.isExit_web_api_accountIncome(NTS, tradeType, symbol, openFlag=openFlag)
        if openOrdersCheckResult:printl(log_level,caseTitle + ' 验证成功.');u(1);caseResult = 1; #, all=0,pass_=0
        else:   printc(caseTitle+ ' 验证失败 incomeType ！= openFee');u(0);caseResult = 0;
    else:   caseResult = False
    return caseResult

def openOrdersCheck(NTS,r,r1,r2,caseTitle,log_level, tradeType, symbol,openFlag=True,param=None):
    if not r1[0]: u(0, block=1);
    if r1[0] and r2:
        order_id = r['data']['orderId'];
        openOrdersCheckResult = check.isExit_openOrders(NTS, tradeType, symbol, order_id,openFlag=openFlag,param=param)
        if openOrdersCheckResult:printl(log_level,caseTitle + ' 验证成功.');u(1);caseResult = 1; #, all=0,pass_=0
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0);caseResult = 0;
    else:   caseResult = False
    return caseResult

#冻结保证金检查
def frozenMaringCheck(NTS,symbol,tradeType=None,log_level=None,title=''):
    tradeType= dict.linear_tradeType
    instrumentList = NTS.instrumentList;ins=NTS.instrument;frozenMarginCal = 0 ;openOrdersBySymbol=0
    balances_r = NTS.Balance(currency='USDT');
    if e(balances_r)[0]:    frozenMarginResponse = balances_r['data'][0]['marginFrozen']
    else:   printc('web资金接口获取异常:',balances_r);return False
    for symbol in instrumentList:
        openOrders_r = NTS.OpenOrders(symbol=symbol, log_level=log_level, tradeType=tradeType, pageSize=100, com_=0);
        takerRate=ins[symbol[:-4]][2];oneCoinValue=ins[symbol[:-4]][1]
        if e(openOrders_r)[0]:
            if openOrders_r['data']['totalPage']>0:
                for openOrder in openOrders_r['data']['list']:
                    if isOpen(openOrder['side'],openOrder['positionSide']):
                        # print('委托数据：',openOrder['side']+openOrder['positionSide'], openOrder['price'], openOrder['leavesQty'], takerRate,openOrder['leverage'],oneCoinValue)
                        _frozenMargin = cal.FrozenMargin(openOrder['side'], openOrder['price'], openOrder['leavesQty'],takerRate,openOrder['leverage'],oneCoinValue)
                        # print('单笔冻结保证金：',_frozenMargin)
                        frozenMarginCal = frozenMarginCal + _frozenMargin
            if openOrders_r['data']['totalPage']>1:
                for i in range(openOrders_r['data']['totalPage']):
                    if i+2<=openOrders_r['data']['totalPage']:
                        openOrders_r = NTS.OpenOrders(symbol=symbol, log_level=log_level, tradeType=tradeType, pageSize=100, pageNum=i + 2);
                        for openOrder in openOrders_r['data']['list']:
                            if isOpen(openOrder['side'], openOrder['positionSide']):
                                _frozenMargin = cal.FrozenMargin(openOrder['side'], openOrder['price'],openOrder['leavesQty'], takerRate, openOrder['leverage'],oneCoinValue)
                                frozenMarginCal = frozenMarginCal + _frozenMargin
        else: openOrdersBySymbol=openOrdersBySymbol+1

    if not float(frozenMarginResponse) == float(frozenMarginCal):
        printc(title+'  预期:', frozenMarginCal, ' 实际：', frozenMarginResponse);return False
    else:
        printl(log_level, _t(), title+' 验证成功.');return True;
    # print('不存在当前委托的symbol数',openOrdersBySymbol,instrumentList.__len__())    #调试代码
    if openOrdersBySymbol==instrumentList.__len__():
            if d(frozenMarginResponse)>0: printc('当前无挂单 仍存在冻结保证金',frozenMarginResponse);return False
            # printc('当前委托无数据，冻结保证金=0 ',p_type='yellow');
            return True

#获取余额
def getNowAccount(user_id):
    db=mysql.mysql(6,1)
    dbName='qa_mulan_btc1.'
    r=db.mysql('select balance from '+dbName+'t_account_action where uid='+str(user_id)+' order by id desc limit 1');
    income=db.mysql('select sum(income) from '+dbName+'t_account_action where uid='+str(user_id));
    userAccount=r[:-1].replace('Decimal','').replace('\'','')
    incomes=income[:-1].replace('Decimal', '').replace('\'', '')
    if userAccount!=incomes: printc(str(user_id)+'流水汇总和余额不一致 分别为:',incomes,userAccount)
    return d(userAccount)

#资金接口数据计算：权益、可用、划转、持仓保证金  - author : Brian
def AccountCalculater(NTS,user_id,log_level=None,title=''):
    Amount=getNowAccount(user_id)
    position_r = NTS.position(log_level=0, tradeType='linearPerpetual')
    account_r = NTS.Balance(log_level=0, currency='Usdt')
    marginAll=d(0);unReal=d(0);MarginIsolated=d(0);unRealIsolated=d(0);MarginCross=d(0)
    if e(account_r)[0]:
        acc=account_r['data'][0]
    result=False
    if e(position_r)[0]:
        if position_r['data'].__len__() > 0:
            for i in position_r['data']:
                positionMargin = 'posMargin'
                if positionMargin not in i.keys():
                    positionMargin = 'positionMargin'
                if i['marginType']=='isolated': MarginIsolated=MarginIsolated+d(i[positionMargin]);unRealIsolated=unRealIsolated+d(i['unrealisedPnl'])
                else: MarginCross=MarginCross+d(i[positionMargin]);
                unReal = unReal + d(i['unrealisedPnl'])
            marginAll=MarginIsolated+MarginCross
        else:
            marginAll=0;unReal=0;
        #计算总持仓保证金 并 断言
        if marginAll!=d(acc['marginPosition']): printc(title+'总持仓保证金不一致: 预期 ' ,marginAll,'实际: ',acc['marginPosition']);result=False;return result;
        else: result=True;
        # 计算账户权益 并 断言
        equity=cal.Equity(Amount,unReal)
        if equity!=d(acc['marginEquity']): printc(title+'权益计算不一致: 预期 ' ,equity,'实际: ',acc['marginEquity'],Amount,unReal);result=False;#return result;
        else: result=True;
        # 计算账户权益 并 断言
        # print(unReal,equity,acc['marginFrozen'],marginAll,'逐仓权益:',MarginIsolated+unRealIsolated,)
        availMaring=cal.AvailMargin(equity, acc['marginFrozen'], MarginCross, MarginIsolated + unRealIsolated, 0)
        # print('权益、冻结、持仓保证金：',equity,acc['marginFrozen'],MarginCross)

        if availMaring<0:print('可用小于0，实际值为',availMaring);availMaring=d(0);
        if not availMaring==d(acc['marginAvailable']): printc(title+'可用计算不一致: 预期 ' ,availMaring,'实际: ',acc['marginAvailable']);result=False;return result;
        else: result = True;
        # 计算最大可划转 并 断言
        transferAmount=cal.TransferAmount(availMaring,Amount);
        if not float(transferAmount) == float(acc['maxWithdrawAmount']): printc('最大可划转计算不一致: 预期 ' ,transferAmount,'实际: ',acc['maxWithdrawAmount']);result=False;return result;
        else:result = True;
        # printl(log_level,'资金接口权益、可用、余额、划转、持仓保证金验证成功.') if result else 0
        return result

#持仓相关公式计算：author : brian
def PositionCalculater(NTS,avgFlag=None,log_level=None):
    temp=0;instrumentList = NTS.instrumentList;ins=NTS.instrument;
    tradeType='linearPerpetual';#symbol='BTCUSDT'
    postionNumber=0
    for symbol in  instrumentList:
        position_r = NTS.position(log_level=0, tradeType='linearPerpetual',symbol=symbol)
        instrument = basic.BasicData().contractCode(NTS, tradeType=tradeType, symbol=symbol)
        oneCoinValue=ins[symbol[:-4]][1]
        if e(position_r)[0]:
            if position_r['data'].__len__()>0:
                if NTS.source == 'API':
                    markPrice = NTS.webposition(symbol=symbol)
                else:
                    markPrice = position_r['data'][0]['markPrice']
                for p in position_r['data']:
                    #持仓保证金 - 按产品公式计算
                    positionMargin_cal=cal.PositionMargin(markPrice, p['positionAmt'],oneCoinValue,p['leverage'])
                    #未实现盈亏 - 按产品公式计算
                    unRealisePnl_cal = cal.UnRealisePnl(p['positionSide'], markPrice, p['avgEntryPrice'], p['positionAmt'],oneCoinValue)
                    #盈亏比例 - 按产品公式计算
                    positionMargin='posMargin'
                    if positionMargin not in p.keys():
                        positionMargin='positionMargin'
                    unRealisePnlRate_cal=float(unRealisePnl_cal / d(p[positionMargin]))
                    # print(positionMargin_cal,unRealisePnl_cal,p['unrealisedPnl'],unRealisePnlRate_cal)
                    if float(unRealisePnl_cal)-float(p['unrealisedPnl'])!=0:
                        printc('浮动盈亏计算错误：','预期: ',unRealisePnl_cal,'实际:',p['unrealisedPnl'],'参数:',[p['symbol']+'-'+p['positionSide'], markPrice, p['avgEntryPrice'], p['positionAmt'],oneCoinValue])
                        return False
                    elif NTS.source=='web' and unRealisePnlRate_cal!=float(p['earningRate']):
                        printc('浮动盈亏"率"计算错误: 预期:',unRealisePnlRate_cal,'实际:',p['earningRate'],'参数:',[unRealisePnl_cal,p[positionMargin]]);return False
                    elif float(positionMargin_cal)!=float(p[positionMargin]):
                        printc('持仓保证金计算错误: 预期:',positionMargin_cal,'实际:',p[positionMargin],'参数:',[p['symbol']+'-'+p['positionSide'],markPrice,p['positionAmt'],oneCoinValue,'levarage='+p['leverage']]);return False
                    else: temp=1
            else: postionNumber=postionNumber+1#printc('持仓无数据',p_type='green');return False
        else: printc('持仓请求异常',position_r);return False
    if postionNumber==instrumentList.__len__() : printc('持仓无数据',p_type='green');return False
    if temp == 1 and  not avgFlag:return True
    if temp==1 and avgFlag:
        price=21999;qty=10;sellPositionFlag=False;
        p1 = position_r['data'][0];
        if position_r['data'].__len__()>0:p2=position_r['data'][1]; sellPositionFlag=True
        order_r = NTS.order(symbol=symbol, log_level=0, price=price, tradeType=tradeType, side='buy', positionSide='long', orderQty=qty, source='web', beautiful=True);
        order_1 = NTS.order(symbol=symbol, log_level=0, price=price, tradeType=tradeType, side='sell', positionSide='short', orderQty=qty, source='web', beautiful=True);
        lastAvgEntryPrice=(d(p1['avgEntryPrice'])*d(p1['positionAmt'])+d(price*qty) ) / (d(p1['positionAmt'])+d(qty))
        if sellPositionFlag: lastAvgEntryPrice_sell=(d(p2['avgEntryPrice'])*d(p2['positionAmt'])+d(price*qty) ) / (d(p2['positionAmt'])+d(qty))
        if e(order_r)[0] and e(order_1)[0]:

            position_after = NTS.position(log_level=0, tradeType='linearPerpetual')
            # print(lastAvgEntryPrice,  position_after['data'][0]['avgEntryPrice'],lastAvgEntryPrice_sell,position_after['data'][1]['avgEntryPrice'])
            if float(lastAvgEntryPrice)!=float(position_after['data'][0]['avgEntryPrice']):
                printc('多仓 开仓均价计算错误: 预期:', lastAvgEntryPrice, '实际:', position_after['data'][0]['avgEntryPrice'], '参数:',[p1['symbol'] + '-' + p1['positionSide'], markPrice, p1['positionAmt']]);
                return False
            else: return True
            if sellPositionFlag:
                if float(lastAvgEntryPrice_sell)!=float(position_after['data'][1]['avgEntryPrice']):
                    printc('空仓 开仓均价计算错误: 预期:', lastAvgEntryPrice_sell, '实际:', position_after['data'][1]['avgEntryPrice'], '参数:',[p2['symbol'] + '-' + p2['positionSide'], markPrice, p2['positionAmt']]);
                    return False
                else: return True
        else: printc('<成交均价计算错误> 新下单失败: ',e(order_r),e(order_1))
        # return True


#当前委托公用验证-owen
def apiopenOrdersCheck(nts,r,r1,r2,caseTitle,log_level, tradeType, symbol):
    if not r1[0]: u(0, block=1);
    if r1[0] and r2:
        order_id = r['data']['orderId'];
        openOrdersCheckResult = check.isExit_api_openOrders(nts, tradeType, symbol, order_id)
        if openOrdersCheckResult:printl(log_level, _t(),caseTitle + ' 验证成功.');u(1, all=0,pass_=0);caseMark = 1;
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0, all=-1,pass_=-1);caseMark = 0;
    else:   caseResult = False
    return caseMark

def owenOpenOrdersCheck(nts,r,r1,r2,caseTitle,log_level, tradeType, symbol):
    if not r1[0]: u(0, block=1);
    if r1[0] and r2:
        order_id = r['data']['orderId'];
        openOrdersCheckResult = check.isExit_api_openOrders(nts, tradeType, symbol, order_id)
        if openOrdersCheckResult:printl(log_level, _t(),caseTitle + ' 验证成功.');u(1, all=0,pass_=0);caseMark = 1;
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0, all=-1,pass_=-1);caseMark = 0;
    else:   caseResult = False
    return True




#历史委托公用验证-owen
def apiHistoryOrdersCheck(nts,r,r1,r2,caseTitle,log_level, tradeType, symbol):
    if not r1[0]: u(0, block=1);
    if r1[0] and r2:
        order_id = r['data']['orderId'];
        HistoryOrdersCheckResult = check.isExit_open_api_historyOrders(nts, tradeType, symbol, order_id)
        if HistoryOrdersCheckResult:printl(log_level, _t(),caseTitle + ' 验证成功.');u(1, all=-1,pass_=-1);caseMark = 1;
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0, all=-1,pass_=-1);caseMark = 0;
    else:   caseResult = False
    return caseMark

#历史委托公用验证-owen
def HistoryOrdersCheck(nts,r,r1,r2,caseTitle,log_level, tradeType, symbol,caseParam=None):
    if not r1[0]: u(0, block=1);
    if r1[0] and r2:
        order_id = r['data']['orderId'];
        HistoryOrdersCheckResult = check.isExit_web_api_historyOrders(nts, tradeType, symbol, order_id)
        if HistoryOrdersCheckResult:printl(log_level, _t(),caseTitle + ' 验证成功.');u(1, all=-1,pass_=-1);caseMark = 1;
        else:   printc(caseTitle+ ' 验证失败 orderId=', order_id);u(0, all=-1,pass_=-1);caseMark = 0;
    else:   caseResult = False
    return caseMark

def CheckP0(NTS,orderId=None,_type='',Flag=True,caseTitle='',status=None,tradeType=None):
    if _type=='HisOrder':
        hisOrders_r = NTS.hisOrders(orderId=orderId)
        if e(hisOrders_r)[0]:
            if hisOrders_r['data']['list'].__len__()==1:
                if Flag:
                    if hisOrders_r['data']['list'][0]['orderStatus']==status:
                        return True
                    else:return False
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(caseTitle+'请求失败',hisOrders_r)
    if _type == 'OpenOrder':
        r= NTS.OpenOrders(tradeType=tradeType, orderId=orderId)
        if e(r)[0]:
            if r['data']['list'].__len__()==1:
                if Flag:    return True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(caseTitle+'请求失败',r)


#根据订单方向、持仓方向判断是否开仓  author: brian
def isOpen(side,positionSide):
    side=side.upper();positionSide=positionSide.upper();
    if (side=='BUY' and positionSide=='LONG') or (side=='SELL' and positionSide=='SHORT'): return True
    else: return False

#最大可开计算
def MaxOrderQtyCal(NTS,side,orderPrice):
    balances_r = NTS.Balance(currency='USDT');
    avail=balances_r['data'][0]['marginAvailable']
    i=NTS.instrument['BTC']
    takerRate=i[2];ctVal=i[1]
    leverage_info=NTS.leverage_info(tradeType=linear_tradeType,symbol='BTCUSDT')
    leverage=leverage_info['data'][0]['leverage']
    # print(takerRate[2],leverage)
    _MaxOpenQty=cal.MaxOpenQty(side,avail,orderPrice,leverage,takerRate,ctVal,0)
    print(side, orderPrice, _MaxOpenQty, takerRate, leverage,ctVal)
    margin=cal.FrozenMargin(side, orderPrice, _MaxOpenQty, takerRate, leverage,ctVal)
    print('按最大可开进行开仓 预估冻结金额：',margin)
    return _MaxOpenQty

#获取委托推荐价格: _type=1:买挂单价(买一买二之间)、_type=2：卖挂单价(卖一卖二之间)、_type=3:成交价(买一、卖一之间)
def newPrice(api,symbol,_type=None):
    # symbolmap = dict.symbolList[symbol]
    # tickSize = float(api.instrument[symbol][0]) if symbol in str(NTS.instrument) else float(NTS.instrument[symbol][0])
    tickSize_len=api.instrument[symbol]["PriceScale"]#BD().size(tickSize) #获取下单 价格精度的长度
    # BD().pricesize(NTS,tradeType='linearPerpetual',symbol=symbolmap[1])
    # res=NTS.muLanOrderBook(symbolmap[0])['body']

    ###OrderBook souce from ws  - add by Brian -- 目前推送不稳定，暂时注释代码
    # import common.noti_ws as Websocket
    # Ws=Websocket.WebsocketSevice(str(NTS._server)+'l','1','1')
    # SYMBOL=symbol if 'USDT' in symbol else symbol+'USDT'
    # OrderBook=Ws.depth(SYMBOL)
    # if not OrderBook[0]:printc('价格从WebSocke获取异常:',OrderBook[1]);return False;
    # else: res=OrderBook[1]
    #ws,rest都不行时，默认一个值
    # res={'time': 1665284425030, 'symbolId': 7, 'bids': [['16000', '1000'], ['15000', '10']], 'asks': [['17000', '100'], ['16000', '2']]}
    Depth = api.Depth("BTC_USDT", log_level=0)[0]
    # print(Depth)
    asks=1;bids=1; #默认买盘，卖盘都有数据
    if Depth["data"]['asks'].__len__()==0: asks = 0
    if Depth["data"]['bids'].__len__()==0: bids = 0
    # 获取买一价格
    if bids:
        bid1 = Depth["data"]['bids'][0][0]
        # 获取买二价格,如果没有买二，则买二=买一的9折
        if Depth["data"]['bids'].__len__()>=2:bid2 = Depth["data"]['bids'][1][0]
        else: bid2=float(bid1)*0.95
    elif asks:  bid1=Depth["data"]['asks'][0][0]*0.9;bid2=bid1*1.05;
    else:   printc("合约无盘口")

    # 获取卖一价格
    if asks:
        ask1 = Depth["data"]['asks'][0][0]
        # # 获取卖二价格,如果没有卖二，则买二=买一的1.1折
        if Depth["data"]['asks'].__len__() >= 2: ask2 = Depth["data"]['asks'][1][0]
        else: ask2=float(ask1)*1.05
    elif bids:  ask1=bid1*1.1;ask2=ask1*1.05;
    else:   printc("合约无盘口")
    # print("买1,买2,卖1,卖2:",bid1,bid2,ask1,ask2)  #调试使用
    if _type == 1 or _type =='buy' or _type == None:
        #获取新的买价格
        newBuyPrice = truncate(round(random.uniform(float(bid2), float(bid1)),tickSize_len),tickSize_len)
        return newBuyPrice
    if _type == 2 or _type =='sell' :
        # 获取新的卖价格
        newSellPrice = truncate(round(random.uniform(float(ask1), float(ask2)), tickSize_len),tickSize_len)
        return newSellPrice
    if _type == 3:
        # 获取买一、卖一价的中间价
        tradeprice = truncate(round(random.uniform(float(bid1), float(ask1)), tickSize_len),tickSize_len)
        return tradeprice

# 开仓不爆仓
def positionSymbol(NTS, symbol, positionSide, price, amount):
    # 面值
    r = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = r['ctVal']
    # taker费率
    takerRate = r['takerRate']
    markPrice=NTS.webposition(symbol)
    # makrPriceMap={'ETHUSDT': '1800', 'BTCUSDT': '19499'} # 标记价格
    p = 1
    if positionSide == 'short':
        p = -1
    # 获取当前账户所有仓位
    currwebpos=[]
    webpos = NTS.position(tradeType=tradeType)['data']
    for i in range(0, len(webpos)):
        # if webpos[i]['symbol'] not in makrPriceMap.keys():
        #     makrPriceMap[webpos[i]['symbol']] = webpos[i]['markPrice']  # 更新标记价格
        if webpos[i]['symbol'] == symbol:
            currwebpos.append(webpos[i])  #把当前币种的持仓放到这里list

    # 获取持仓和当前委托的仓位价值
    PosUsdtList = cal.riskLimit(NTS, tradeType=tradeType, symbol=symbol)
    print(symbol+"持仓+当前委托的仓位价值,多仓USDT="+str(PosUsdtList[0])+',空仓USDT='+str(PosUsdtList[1]))
    ##仓位价值
    if positionSide == 'long':
        value_limit = max((d(price) * d(amount) * d(ctVal) + d(PosUsdtList[0])), d(PosUsdtList[1]))
    else:
        value_limit = max(d(PosUsdtList[0]), (d(price) * d(amount) * d(ctVal) + d(PosUsdtList[1])))

    print(symbol+f"{positionSide}持仓+同向当前委托的仓位价值+开仓价值USDT="+ str(value_limit))

    # 获取风险限额 0:symbol , 1:value_limit 价值限制 ,  2:maintenance_margin_rate 维持保证金率
    risk_limit = t_risk_limit(symbol)
    for i in range(0, len(risk_limit)):
        if d(value_limit) <= d(risk_limit[i][0]):  ## 价值限制
            maintenance_margin_rate = risk_limit[i][1]  ##维持保证金率
            break
    print(symbol+'的维持保证金率='+str(maintenance_margin_rate))
    # 获取预警参数 0: symbol 1: warning_rate 预警参数
    warnRate = warning_rate(symbol)
    warningRate = warnRate[0][0]  ##预警参数
    # 预警保证金率 = 预警参数 * 维持保证金率
    EarlywarningMarginRatio = d(maintenance_margin_rate) * d(warningRate)
    print(symbol+'的预警保证金率='+str(EarlywarningMarginRatio))
    # 资金费率
    funding = -0.0018830852
    # # 标记价格
    # makrPrice = makrPriceMap[symbol]
    # 账户权益
    account = NTS.Balance(currency=currency)['data'][0]
    crossmarginEquity = account['marginEquity']  ## 接口返回的账户权益
    # 当前全仓权益 + p * ( A标记价格 - A委托价格 ) * A本次开仓数量
    currmarginEquity = d(crossmarginEquity) + d(p * (d(markPrice) - d(price)) * d(amount) * d(ctVal))


    othersymbolPos = 0  # sum其他交易对【标记价格 * 持仓数量 * (预警保证金率 + max(p*资金费率，0) + taker费率）】
    # otherLongPositionAmt = 0
    # otherShortPositionAmt = 0
    otherSymbol = []
    for i in range(0, len(webpos)):
        if webpos[i]['symbol'] != symbol:
            # newWebpos.append(webpos[i])
            if webpos[i]['symbol'] not in otherSymbol:
                otherSymbol.append(webpos[i]['symbol'])
    if len(otherSymbol) > 0:
        for i in range(0, len(otherSymbol)):
            # otherctval = BD().contractCode(NTS, tradeType=tradeType, symbol=otherSymbol[i])['ctVal']
            # 其他币种 标记价格 * 净持仓数量
            otherNetPosValue = netPosValue(NTS, tradeType=tradeType, symbol=otherSymbol[i])
            otherLimit = cal.riskLimit(NTS, tradeType=tradeType, symbol=otherSymbol[i])
            otherLimitValue = max(otherLimit[0],otherLimit[1])
            takerrate = BD().contractCode(NTS, tradeType=tradeType, symbol=otherSymbol[i])['takerRate']
            risk_limit = t_risk_limit(otherSymbol[i])
            for i in range(0, len(risk_limit)):
                if d(otherLimitValue) <= d(risk_limit[i][0]):  ## 价值限制
                    other_maintenance_margin_rate = risk_limit[i][1]  ##维持保证金率
                    break
            print(otherSymbol[i]+'的维持保证金率='+ str(other_maintenance_margin_rate))
            otherWarnRate = warning_rate(otherSymbol[i])
            otherWarningRate = otherWarnRate[0][0]     #预警参数
            print(otherSymbol[i] + '的预警保证金率=' + str(otherWarningRate))
            # 其他币种的预警保证金率， 预警保证金率 = 预警参数 * 维持保证金率
            otherEarlywarningMarginRatio = d(other_maintenance_margin_rate) * d(otherWarningRate)

            # funding=NTS.predictedFunding(tradeType=tradeType,symbol=res[i]['symbol'])['data']['predictedFundingRate']
            # 其他交易对的 标记价格 * 持仓数量
            # sum其他交易对【标记价格 * 持仓数量 * (预警保证金率 + max(p*资金费率，0) + taker费率）】

            othersymbolPos += d(otherNetPosValue) * (d(otherEarlywarningMarginRatio) + d(max(p * float(funding), 0)) + d(takerrate))
    print('资金费率='+str(funding))
    print('当前全仓权益= '+str(crossmarginEquity))
    print('p * ( A标记价格 - A委托价格 ) * A本次开仓数量;markFilledMargin=' + str(d(p * (d(markPrice) - d(price)) * d(amount) * d(ctVal))))
    print('当前全仓权益 + p * ( A标记价格 - A委托价格 ) * A本次开仓数量；currentAccountInterest=' + str(currmarginEquity))
    print("sum其他交易对【标记价格 * 持仓数量 * (预警保证金率 + max(p*资金费率，0) + taker费率）】；othersWarningMargin=" + str(othersymbolPos))
    longPositionAmt = 0
    shortPositionAmt = 0
    currentWarningMargin=0
    netPositionAmt=0
    if currwebpos.__len__()>0:
        for i in range(0,len(currwebpos)):
            if currwebpos[i]['positionSide']=='long':
                longPositionAmt= currwebpos[i]['positionAmt']
            else:
                shortPositionAmt = currwebpos[i]['positionAmt']
    if positionSide=='long':
        longPositionAmt=float(longPositionAmt) + float(amount)
    else:
        shortPositionAmt= float(shortPositionAmt) + float(amount)
    netPositionAmt = abs(float(longPositionAmt) - float(shortPositionAmt))
        # # A标记价格 * A（持仓数量 + 本次开仓数量）*(预警保证金率 + max(p * 资金费率，0) + taker费率）
    currentWarningMargin = d(markPrice) * (d(netPositionAmt) * d(ctVal)) * (d(EarlywarningMarginRatio) + d(max(p * float(funding), 0)) + d(takerRate))
    print("A标记价格 * A（持仓数量 + 本次开仓数量）*(预警保证金率 + max(p * 资金费率，0) + taker费率）;currentWarningMargin=" + str(currentWarningMargin))

    if currmarginEquity - (othersymbolPos + currentWarningMargin) > 0:
        print('因为'+str(currmarginEquity)+'>'+str(othersymbolPos)+' + '+str(currentWarningMargin))
        print('所以 本次开仓不爆仓，本次开仓后还剩余权益=' + str(currmarginEquity - (othersymbolPos + currentWarningMargin)))
        return False

    else:
        print("warningMargin= " + str((othersymbolPos + currentWarningMargin)))
        print('因为'+str(currmarginEquity)+'<'+str(othersymbolPos)+' + '+str(currentWarningMargin))
        print('所以 本次开仓爆仓,可用保证金不足,本次开仓后保证金剩余='+str(currmarginEquity - (othersymbolPos + currentWarningMargin)))
        return True


# 风险限额
def t_risk_limit(symbol):
    symbol = '"' + symbol + '"'
    risklimitsql = 'select value_limit,maintenance_margin_rate,max_leverage from qa_mulan_trade.t_risk_limit  where margin_type=2 and symbol=%s  order by value_limit ' % symbol
    risklimit = t.mysql(risklimitsql, True)
    risklimit = list(risklimit)

    return risklimit

# 最大杠杆对应风险限额
def t_risk_limit_leverage(symbol,max_leverage,MarginTypeNumber):
    symbol = '"' + symbol + '"'
    risklimitsql = 'select value_limit,max_leverage from qa_mulan_trade.t_risk_limit  where margin_type=%s and symbol=%s and max_leverage>=%s  order by max_leverage asc limit 1' % (MarginTypeNumber,symbol, max_leverage)
    risklimit = t.mysql(risklimitsql, True)
    risklimit = list(risklimit)

    return risklimit
# 预警参数
def warning_rate(symbol):
    symbol = '"' + symbol + '"'
    warningRateSql = 'select warning_rate from qa_mulan_trade.t_symbol   where currency="USDT" and symbol=%s and symbol_status=1 ' % symbol
    warningRate = t.mysql(warningRateSql, True)
    warningRate = list(warningRate)

    return warningRate

#处理标记价格
def makerprice(NTS):
    makrPriceMap= dict.makrPriceMap
    webpos = NTS.position(tradeType=tradeType)['data']
    if len(webpos)>0:
        for i in range(0, len(webpos)):
            if webpos[i].keys()=='markPrice':
                    makrPriceMap[webpos[i]['symbol']] = webpos[i]['markPrice']
    return makrPriceMap


#平仓不穿仓，当前全仓权益 + ( 委托价 - 标记价 ) * p * 净仓位数量 + (max( 买一价，委托价格 ) * 委托数量 * taker手续费率 ) > 0
def close_wear_no_pos(NTS,symbol,price,amount,positionSide):
    p = -1
    if positionSide == 'long':
        p = 1
    r = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = r['ctVal']
    takerRate = r['takerRate']

    account = NTS.Balance(currency=currency)['data'][0]
    crossmarginEquity = account['marginEquity']  ## 接口返回的账户权益
    #查当前持仓
    res=NTS.position(tradeType=tradeType,symbol=symbol)['data']

    #仓位
    netPos=0
    for i in range(0, len(res)):
        if res[i]['positionSide'] == positionSide:
            netPos = res[i]['positionAmt']

    #市场买一价格
    symbolId= dict.symbolList[symbol[:-4]][0]
    res = NTS.muLanOrderBook(symbolId)['body']['bids']
    if len(res)==0:
        bid1 = 0
    else:
        bid1 = res[0][0]

    #标记价格
    makrPriceMap = makerprice(NTS)
    makrPrice = makrPriceMap[symbol]

    # 当前全仓权益 + (委托价 - 标记价) * p *  净仓位数量 - (max( 买一价，委托价格 ) * 委托数量 * taker手续费率 ) > 0
    closePosUsdt = d(crossmarginEquity) + (d(price) - d(makrPrice)) * d(p) * d(netPos) * d(ctVal) - max(d(bid1), d(price)) * d(amount) * d(ctVal) * d(takerRate)


    if closePosUsdt > 0:
        print('本次平仓不穿仓，','剩余账户权益：'+str(closePosUsdt),'，当剩余账户权益小于等于0时穿仓')
        return True
    else:
        print('本次平仓穿仓,可用保证金不足')
        return False

#获取平仓不穿仓价格
def close_wear_Price(NTS,symbol,amount,positionSide):
    p = -1
    if positionSide == 'long':
        p = 1
    r = BD().contractCode(NTS, tradeType=tradeType, symbol=symbol)
    ctVal = r['ctVal']
    takerRate = r['takerRate']


    account = NTS.Balance(currency=currency)['data'][0]
    crossmarginEquity = account['marginEquity']  ## 接口返回的账户权益
    #市场买一价格
    symbolId= dict.symbolList[symbol[:-4]][0]
    res = NTS.muLanOrderBook(symbolId)['body']['bids']
    if len(res)==0:
        bid1 = 0
    else:
        bid1 = res[0][0]

    #标记价格
    makrPriceMap = makerprice(NTS)
    makrPrice = makrPriceMap[symbol]
    # 当前全仓权益 + (委托价 - 标记价) * p * 平仓数量 - (max(买一价，委托价格) * 委托数量 * taker手续费率 ) = 0

    #p * 平仓数量
    ppos=d(p) * d(amount) * d(ctVal)
    #当前全仓权益 + (委托价 - 标记价) * p * 平仓数量  = 0
    closePosUsdt =  d(makrPrice) * ppos - d(crossmarginEquity)

    price = closePosUsdt / ppos
    #   - (max(买一价，委托价格) * 委托数量 * taker手续费率 )
    fee = max(d(bid1), d(price)) * d(amount) * d(ctVal) * d(takerRate)
    priceFee=[]
    priceFee.append(price)
    priceFee.append(fee)


    return priceFee


# 净持仓USDT （多-空）
def netPosValue(NTS, tradeType, symbol):
    ctVal = BD().contractCode(NTS, tradeType, symbol)['ctVal']
    posi = NTS.position(tradeType=tradeType, symbol=symbol)['data']
    markPrice=NTS.webposition(symbol)
    posiLongUsdt = 0  # 多仓仓位价值
    posiShortUsdt = 0  # 空仓仓位价值
    if len(posi) > 0:
        for i in range(0, len(posi)):
            if posi[i]['positionSide'] == 'long':
                posiLongUsdt = d(markPrice) * d(posi[i]['positionAmt']) * d(ctVal)  # 多仓仓位价值
            else:
                posiShortUsdt = d(markPrice) * d(posi[i]['positionAmt']) * d(ctVal)  # 空仓仓位价值

    netPosValue = abs(posiLongUsdt - posiShortUsdt)

    return netPosValue



# #校验下单数量限制；可开多/空数量= min { 可开数量x ，杠杆对应风险限额 / 标记价格 - 持仓数量 - 同向挂单冻结数量，最大单笔下单数量限制}
# def check_olume_limit(NTS,symbol,side,positionSide,price,log_level=None,MarginType=None):
#     # r=BD().contractCode(NTS,tradeType=tradeType,symbol=symbol)
#     instrument= NTS.instrument;currency=symbol[-4:]
#     takerFeeRate=instrument[symbol[:-4]][2]
#     ctVal=instrument[symbol[:-4]][1]
#     markPriceMap=makerprice(NTS)
#     markPrice=markPriceMap[symbol]  #标记价格
#     available_margin = NTS.balances(currency=currency)['data'][0]['marginAvailable']     #可用保证金
#     leverage=NTS.leverage_info(tradeType=tradeType,symbol=symbol,marginType=MarginType)['data'][0]['leverage']    #当前杠杆
#     #查询当前杠杆对应的风险限额
#     MarginTypeNumber=1 if MarginType=='isolated' else 2
#     riskLimit = t_risk_limit_leverage(symbol,leverage,MarginTypeNumber=MarginTypeNumber)[0][0]
#     positionAmt = 0  # 持仓量
#     openAmt = 0  # 同方向挂单冻结数量
#     # import BU.NTS.dataCheck.Formula as Formula
#     # a=Formula.Formula(NTS,symbol)
#     # print(a.Symbol)
#     # 查持仓获取持仓量(张数)
#     pos = NTS.position(tradeType=tradeType, symbol=symbol)['data']
#     if positionSide in str(pos):
#         for i in range(0, len(pos)):
#             if pos[i]['positionSide'] == positionSide:
#                 positionAmt += float(pos[i]['positionAmt']) * float(markPrice) * float(ctVal);
#     else: positionAmt=0
#     # 查当前委托，或者同方向挂单
#     openPos = NTS.openOrders(tradeType=tradeType, symbol=symbol)['data']['list']
#     if len(openPos) > 0:
#         for i in range(0, len(openPos)):
#             if openPos[i]['side'] == side and openPos[i]['positionSide'] == positionSide:
#                 openAmt += float(openPos[i]['leavesQty']) * float(openPos[i]['price']) * float(ctVal)
#             else:openAmt=0
#     else: openAmt = 0
#     # 获取市场买一价格
#     bid1 = 0
#     symbolmap = dict.symbolList[symbol[:-4]]
#     # bids = NTS.muLanOrderBook(symbolmap[0])['body']['bids']
#     bids = [['18000', '1000'], ['16000', '10']]
#     if len(bids) > 0:   bid1 = bids[0][0]
#
#     # 计算最大风险限额对应的最大可开数量： positionAmt持仓价值、openAmt同向挂单价值、riskLimit杠杆对应的风险限额
#     riskLimitOrderQty = cal.risk_limit_orderQty(riskLimit=riskLimit,positionSide=positionSide, positionAmt=positionAmt,openAmt=openAmt, ctVal=ctVal,orderPrice=price,bid1=bid1)
#     # 计算 可用保证金 对应的 最大可开数量
#     MaxOrderNumbe = cal.MaxOpenQty(side=side, orderPrice=price, avail=available_margin, takerRate=takerFeeRate,leverage=leverage, ctVal=ctVal, bid1=bid1)
#     # 数据库配置最大下单数量限制
#     maxorderVolume = cal.t_order_volume_limit(symbol)
#
#     # 实际最大下单数量限制
#     maxOlumeLimit = min(riskLimitOrderQty, MaxOrderNumbe, maxorderVolume)
#
#     # if amount - maxOlumeLimit > 0:
#     # print('下单数量超过最大限制，最大下单数量限制张数='+ str(maxOlumeLimit))
#     printl(log_level,'产品公式: 可开多数量 = min { 可开数量x ，（杠杆对应风险限额 - 仓位价值-当前委托价值） / 委托价格 ，最大单笔下单数量限制}\n 可开空数量 = min { 可开数量x ，（杠杆对应风险限额 - 仓位价值-当前委托价值） / max(bid1，委托价格) ，最大单笔下单数量限制}')
#     printl(log_level, '余额计算的可开数量 = ' + str(MaxOrderNumbe))
#     printl(log_level,f'db中杠杆{leverage}对应的风险限额',riskLimit)
#     printl(log_level,positionSide+'仓位价值:'+str(positionAmt),'当前委托价值:'+str(openAmt)+' db中最大可开数量'+str(maxorderVolume))
#     printl(log_level, '杠杆对应风险限额 / 标记价格 - 持仓数量 - 同向挂单冻结数量 = ' + str(riskLimitOrderQty))
#     printl(log_level, '实际最大下单数量限制=' + str(maxOlumeLimit))
#     return maxOlumeLimit

    # posUsdt = d(price) * d(amount) * d(ctVal)   #下单仓位价值
    # takerFee = posUsdt * d(takerFeeRate)
    # if d(available_margin) - (posUsdt / d(leverage) + takerFee) > 0:
    #     tRiskLimit=t_risk_limit(symbol)
    #     for i in range(0,len(tRiskLimit)):
    #         if posUsdt <= tRiskLimit[i][0]:
    #             riskLimit = tRiskLimit[i][0]   #风险限额
    #             break


#风险率
def cross_risk_rate(NTS,tradeType):
    symbollist=[]
    #获取持仓数据
    crossPosition = NTS.position(tradeType=tradeType)['data']
    if len(crossPosition) > 0:
        for i in range(0, len(crossPosition)):
            if crossPosition[i]['symbol'] not in symbollist:
                symbollist.append(crossPosition[i]['symbol'])
    if len(symbollist) > 0:
        for i in range(0,len(symbollist)):
            #获取仓位价值
            riskLimit=cal.riskLimit(NTS,tradeType=tradeType,symbol=symbollist[i])
            riskLimitValue=max(riskLimit[0],riskLimit[1])
            #计算维持保证金
            cal.maintenance_margin()
    else:
        print('暂无持仓，无需计算风险率')

#一键清空所有仓位和委托
def clearOrder(NTS,symbol,log_level=None):
    from BU.NTS.WebOrder import n_order
    webnts=n_order(6,user_id=face_user)
    markPriceMap = makerprice(NTS)
    markPrice = markPriceMap[symbol]
    pos=NTS.position(tradeType=tradeType,symbol=symbol,pageSize=100,pageNum=1)['data']
    oporder=NTS.OpenOrders(tradeType=tradeType, symbol=symbol, pageSize=100, pageNum=1)['data']['list']
    if len(oporder)>0:
        for i in range(0,len(oporder)):
            NTS.orderCancel(tradeType=tradeType,symbol=symbol,orderId=oporder[i]['orderId'])
        oporder1=NTS.OpenOrders(tradeType=tradeType, symbol=symbol)['data']['list']
        if len(oporder1)<=0:
            printl(log_level,'UID:'+NTS.user_id+','+symbol + '合约当前委托已撤完单')
    else:
        printc('UID:'+NTS.user_id+','+symbol + '合约没有当前委托',p_type='green')
    if len(pos) >0:
        for i in range(0,len(pos)):
            if pos[i]['positionSide']=='long':
                res=NTS.order(price=markPrice,tradeType=pos[i]['tradeType'],side='sell',positionSide=pos[i]['positionSide'],marginType=pos[i]['marginType'],
                          symbol=symbol,orderQty=pos[i]['positionAmt'],orderType='limit')
                if res['code']=='1':
                    webnts.order(price=markPrice, tradeType=pos[i]['tradeType'], side='buy', positionSide=pos[i]['positionSide'],
                            marginType=pos[i]['marginType'],
                            symbol=symbol, orderQty=pos[i]['positionAmt'], orderType='limit')

            else:
                res=NTS.order(price=markPrice, tradeType=pos[i]['tradeType'], side='buy', positionSide=pos[i]['positionSide'],
                          marginType=pos[i]['marginType'],
                          symbol=symbol, orderQty=pos[i]['positionAmt'], orderType='limit')
                if res['code'] == '1':
                    webnts.order(price=markPrice, tradeType=pos[i]['tradeType'], side='sell',
                                 positionSide=pos[i]['positionSide'],
                                 marginType=pos[i]['marginType'],
                                 symbol=symbol, orderQty=pos[i]['positionAmt'], orderType='limit')
        pos1 = NTS.position(tradeType=tradeType, symbol=symbol)['data']
        if len(pos1) <= 0:
            printl(log_level,'UID:' + NTS.user_id + ',' + symbol + '合约持仓已全部平完')
    else:
        printc('UID:' + NTS.user_id + ',' + symbol + '合约没有持仓',p_type='green')
#一键取消当前委托订单
def clearOpenOrder(NTS,symbol,tradeType=None,log_level=None):
    oporder = NTS.OpenOrders(tradeType=tradeType, symbol=symbol, pageSize=100, pageNum=1)
    if  e(oporder)[0]:
        totalPage=oporder['data']['totalPage']
        if totalPage==0:
            return printl(log_level=log_level,title='UID:' + NTS.user_id + ',' + symbol + '合约没有当前委托', p_type='green')
        while(totalPage>0):
            oporder1 = NTS.OpenOrders(tradeType=tradeType, symbol=symbol, pageSize=100, pageNum=1)['data']['list']
            for i in range(0, len(oporder1)):
                NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=oporder1[i]['orderId'])
            oporder2 = NTS.OpenOrders(tradeType=tradeType, symbol=symbol)['data']
            totalPage=oporder2['totalPage']
        return printl(log_level=log_level, P1='UID:' + NTS.user_id + ',' + symbol + '合约当前委托已撤完单')

    else:
        return printc('UID:' + NTS.user_id + ',' + symbol + '查询当前委托失败，'+oporder['code'] + oporder['message'])

# web一键平仓\一键撤单
def oneClickClose_Cancel(NTS,symbol,log_level=None):
    pos = NTS.position(tradeType=tradeType, symbol=symbol, pageSize=100, pageNum=1)['data']
    oporder = NTS.OpenOrders(tradeType=tradeType, symbol=symbol, pageSize=100, pageNum=1)['data']['list']
    if len(oporder) > 0:
        NTS.oneClickCancel(tradeType=tradeType, symbol=symbol,log_level=log_level)
        oporder1 = NTS.OpenOrders(tradeType=tradeType, symbol=symbol)['data']['list']
        if len(oporder1) <= 0:printl(log_level,_t(),'UID:'+NTS.user_id+','+symbol+'撤单完成,当前委托无订单')
    else: printl(log_level,_t(),'UID:'+NTS.user_id+','+symbol+'当前委托无订单')
    if len(pos) > 0:
        NTS.oneClickClose(tradeType=tradeType, symbol=symbol, log_level=log_level)
        pos1 = NTS.position(tradeType=tradeType, symbol=symbol)['data']
        if len(pos1) <= 0:printl(log_level,_t(),'UID:'+NTS.user_id+','+symbol+'平仓完成,持仓无订单')
    else: printl(log_level,_t(),'UID:'+NTS.user_id+','+symbol+'持仓无订单')

if __name__ == '__main__':
    # NTS_WEB=n_order('5',user_id='99999')
    # NTS = n_order(6, user_id='97201938');
    Symbol='BTCUSDT'
    # NTS = NtsApiOrder(6, user_id='10071')
    NTS = n_order(6, user_id='10071')
    # NTS = n_order(6, user_id='97201967');#print(NTS.token)
    # print(NTS_WEB.user_id)
    OrderPrice=newPrice(NTS,Symbol[:-4])
    print("下单推荐价",OrderPrice)
    # Amount = getNowAccount(NTS.user_id) #获取余额
    # print('预估最大可开数量：',MaxOrderQtyCal(NTS,'buy',19957.77)) #下单数量计算
    # AccountCalculater(NTS_WEB,NTS_WEB.user_id)
    # PositionCalculater_Result=PositionCalculater(NTS_WEB)
    # print(PositionCalculater_Result)
    # 平仓不穿仓
    # print(close_wear_no_pos(NTS,'BTCUSDT',14223,30,'long'))
    # 开仓不爆仓
    # print(positionSymbol(NTS, 'ETHUSDT', 'long', 3000, 500))
    # print(close_wear_no_pos(NTS,'BTCUSDT',25000,72,'short'))
    # print('开仓不爆仓结果：',positionSymbol(NTS, 'BTCUSDT', 'long', '23123', '64'))
    # 仓位价值
    # print(posValue(NTS, 'linearPerpetual', 'BTCUSDT'))
    # 查最大可划转
    # print(AccountCalculater(NTS, user_id='10070'))

    # 查询最大支持杠杆
    # print(leverage('"BTCUSDT"'))

    #一键清空仓位
    # print(clearOrder(NTS,'BTCUSDT',3))
    #一键撤单
    # print(clearOpenOrder(NTS,tradeType=tradeType,symbol='BTCUSDT',log_level=2))

    # print('开仓是否爆仓结果：',positionSymbol(NTS, 'BTCUSDT', 'LONG', '1', '1'))