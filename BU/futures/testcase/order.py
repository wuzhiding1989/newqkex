import copy,random
from BU.futures.api import webapi
from param.code_list import code_list as code
import BU.futures.testcase.dataCheck.dataCheck as dataCheck
import param.dict as param_dict
from param.dict import cumQty,avgPrice,lastPrice,leavesQty,commission,orderStatus,base,quote,clOrdId,leverage,price, \
    FailMessage
import BU.NTS.comm.params as PAR
import common.util as ut
from common.asserts import responseCodeAssert as _assert
from common.other import httpCheck as e
from common.util import printc,printl,d, countCaseNumber as u,ModeCount,Count,truncate
from BU.NTS.dataCheck.dataCheck import newPrice
import BU.other.UserDataCheck as UserDataCheck
from BU.futures.api import webapi
NTS=webapi.webapi(2,'test')
caseMark=1
symbol = 'BTCUSDT';price=random.randint(6999,8999);tradeType = 'linearPerpetual';side = 'Buy';positionSide = 'Long';marginType1 = 'cross';marginType = 'cross';orderType = 'limit';orderQty =random.randint(1,5);
for i in param_dict.funtionMap:
    ut.otherCase[i]=0
success_code =code["success"][0]
normal_caseTitle = "下单"
resultVerify_caseTitle = "下单 返参校验"
exception_caseTitle = "下单 异常入参"

# caseTile: 全仓开仓买入下单流程：包括下单、当前委托、撤单、历史委托、资金验证  P0用例
def makerOrderCase_P0(NTS=NTS,log_level=None,_type=None,MarginType=None):
    BusinessName ='全仓开仓买入下单流程'
    marginType=MarginType if MarginType else marginType1
    caseResult=True;global caseMark;caseTitle=f'<{BusinessName}>下单P0 '+ str(side)+str(positionSide)
    if caseMark:
        # 步骤1：下限价单 并验证 当前委托
        r = NTS.order(symbol=symbol, log_level=log_level, price=price, tradeType=tradeType, side=side, positionSide=positionSide, marginType=marginType, orderType=orderType, orderQty=orderQty, com_=1)
        if not r:
            printc(caseTitle+FailMessage+'. 阻塞：当前委托、撤单、历史委托、资金验证P0用例');ModeCount(r, '下单')
            Count('挂单+仓位+资金公式',4,0,0,4);Count('当前委托',1,0,0,1);Count('历史订单',1,0,0,1);Count('撤单',1,0,0,1);orderAssertResult=False;return False
        else:   CaseResult = printl(log_level, NTS.source + f'{caseTitle} {r["data"]["orderId"]} {price}', response=r, RepCode=success_code, remark=NTS,Module='下单')
        if CaseResult:
            if '2' in str(_type):
                caseMark=dataCheck.CheckP0(NTS,r['data']['orderId'], tradeType=tradeType,_type='OpenOrder',caseTitle=caseTitle+'下单后 查询当前委托')
                openOrder_check=printl(log_level, NTS.source + f'<{BusinessName}>当前委托 {r["data"]["orderId"]}', response=caseMark,RepCode=success_code, remark=NTS, Module='当前委托')
                # web_openOrders.openOrdersCase_P0(NTS, log_level,marginTypeList=marginType,orderId=r['data']['orderId'])
                if openOrder_check:
                    DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='13',title=NTS.source+caseTitle+' 挂单')
                    Count('挂单+仓位+资金公式', 2, DataCheckResult, 2 - DataCheckResult, 0)
                else:
                    Count('挂单+仓位+资金公式',2,0,0,2)
        #撤单P0
        if CaseResult:
            cancel=False
            r2 = NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=r['data']['orderId'], log_level=log_level)
            # if e(r2)[0]: u(1);printl(log_level,_t(),caseTitle+' 撤单'+SuccessMessage);Count('撤单',1,1,0,0);cancel=True
            # else: u(0); printc('P0：撤单请求失败.',r2);Count('撤单',1,0,1,0)
            cancel = printl(log_level, NTS.source + f'<{BusinessName}>撤单P0 {r["data"]["orderId"]}', response=r2,RepCode=success_code, remark=NTS, Module='撤单')

            if cancel:
                hisOrderCheckResult = dataCheck.CheckP0(NTS,r['data']['orderId'], _type='HisOrder',caseTitle=caseTitle+'撤单后 查询历史订单',status='canceled')
                printl(log_level, NTS.source + f'<{BusinessName}>历史委托P0', response=hisOrderCheckResult, RepCode=success_code,remark=NTS, Module='历史委托')
                # ModeCount(hisOrderCheckResult, '历史委托');printl(log_level,caseTitle+' 撤单后 查询历史订单'+SuccessMessage,hisOrderCheckResult)
                DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='13', title=NTS.source+caseTitle + ' 撤单后')
                Count('挂单+仓位+资金公式', 2, DataCheckResult, 2 - DataCheckResult, 0)
            else:Count('挂单+仓位+资金公式',2,0,0,2);Count('历史委托',1,0,0,1);
        return caseResult
    else: u(0, block=1);caseResult = False

# 下单-->当前委托验证-->撤单-->历史委托验证
def open_cancel_hisOrder(NTS,symbol,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level=None,_type=None):

    caseParam=copy.deepcopy(PAR.linear_cross_param)
    caseResult = True;global caseMark;global title
    if str(side) in ["buy"] and str(positionSide) in ['long']: title = "买入开多"
    if str(side) in ["sell"] and str(positionSide) in ['short']: title = "卖出开空"
    if str(side) not in ["sell", "buy"] or str(positionSide) not in ['short', 'long']: return print("<< side&positionSide >>输入错误")
    caseTitle = f'双向全仓 下单--{caseTitle}'+ title
    paramList = param
    paramListAssert = OpenTrust_Assert
    if caseMark:
        for p in paramList:
            if p[1]:  caseParam[p[0]]=p[1]
            else : caseParam.pop(p[0])
        caseParamAssert=copy.deepcopy(caseParam)
        for p1 in paramListAssert: caseParamAssert[p1[0]]=p1[1]
        order_r = NTS.order(log_level=log_level, caseParam=caseParam)
        orderAssertResult = _assert(order_r, (0, code["success"][0], ' '), '', caseTitle, log_level);Count(caseTitle,1,1,0,0)
        caseMark = dataCheck.openOrdersChecks(NTS, order_r, orderAssertResult, caseTitle + ' 当前委托', log_level,tradeType, symbol, param=caseParamAssert);Count(caseTitle,1,1,0,0)
        UserDataCheck.UsderDataCheckCase(NTS, log_level, option='13', title=caseTitle + ' 当前委托');Count(caseTitle,2,2,0,0)

        Cancel_r = NTS.orderCancel(tradeType=tradeType, symbol=symbol, orderId=order_r['data']['orderId']);Count(caseTitle,1,1,0,0)
        caseMark = dataCheck.openOrdersChecks(NTS, Cancel_r, orderAssertResult, caseTitle + ' 撤单', log_level, tradeType, symbol, openFlag=False);Count(caseTitle,1,1,0,0)
        UserDataCheck.UsderDataCheckCase(NTS, log_level, option='13', title=caseTitle + ' 撤单后');Count(caseTitle,2,2,0,0)

        HisOrder_Assert = HisOrder_Assert
        caseParamAssert = copy.deepcopy(caseParam)
        for p1 in HisOrder_Assert: caseParamAssert[p1[0]] = p1[1]
        caseMark = dataCheck.openOrdersChecks(NTS, order_r, True, caseTitle + ' 历史委托', log_level, tradeType, symbol,param=caseParamAssert, _type='HisOrder');Count(caseTitle,1,1,0,0)
        ut.otherCase[2] = ut.otherCase[2] + 1
        return caseResult
    else: u(0, block=1);caseResult = False

# caseTile: 全仓开仓买入+postOnly不传+[clOrdId不传、priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_002(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS, symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', None],['priceType', None],[clOrdId, None],['postOnly', None],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty', d(orderQty)], ['realProfit', str(0)],['commissionAsset', 'USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'postOnly不传'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

# caseTile: 全仓开仓买入+postOnly传False+[clOrdId不传、priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_003(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS,symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', None],['priceType', None],[clOrdId, None],['postOnly', False],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty', d(orderQty)], ['realProfit', str(0)],['commissionAsset', 'USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'postOnly传False'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

# caseTile: 全仓开仓买入+postOnly传True+[clOrdId不传、priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_004(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS, symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', None],['priceType', None],[clOrdId, None],['postOnly', True],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty', d(orderQty)], ['realProfit', str(0)],['commissionAsset', 'USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'postOnly传True'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

# caseTile: 全仓开仓买入+clOrdId传int类型+[priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_005(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS, symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', None],['priceType', None],[clOrdId, str(88888888)],['postOnly', False],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty', d(orderQty)], ['realProfit', str(0)],['commissionAsset', 'USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'clOrdId传int类型'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

# caseTile: 全仓开仓买入+clOrdId传string类型+[clOrdId不传、priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_006(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS, symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', None],['priceType', None],[clOrdId, 'abcdefghijk'],['postOnly', False],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty', d(orderQty)], ['realProfit', str(0)],['commissionAsset', 'USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'clOrdId传string类型'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

# caseTile: 全仓开仓买入+timeInForce传GTC+[clOrdId不传、priceType不传、reduceOnly不传、timeInForce不传]
def makerOrderCase_007(NTS,symbol,side,positionSide,log_level=None,_type=None):

    symbol_ = symbol + 'USDT'
    if side == 'buy': OrderPrice = newPrice(NTS, symbol, _type=1)
    else : OrderPrice = newPrice(NTS, symbol, _type=2)
    Leverage_r = NTS.leverage_info(PAR.linear_cross_param['tradeType'], symbol_, marginType)
    Leverage = Leverage_r['data'][0]['leverage']
    param = [['timeInForce', 'GTC'],['priceType', None],[clOrdId, None],['postOnly', False],[param_dict.side, side],[param_dict.positionSide, positionSide],[param_dict.price, str(OrderPrice)],['symbol', symbol_],['orderQty', str(orderQty)]]
    if NTS.source == 'API':OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active']]
    else:OpenTrust_Assert = [[cumQty, '0'], ['price', d(OrderPrice)], [avgPrice, ''], [lastPrice, ''], [leverage, d(Leverage)],[leavesQty, str(orderQty)], [commission, ''], [orderStatus, 'active'], [base, symbol], [quote, 'USDT']]
    HisOrder_Assert = [['price', d(OrderPrice)], ['orderQty',d(orderQty)], ['realProfit', str(0)],['commissionAsset','USDT'], [cumQty, str(0)], [avgPrice,str(0)], [lastPrice,str(0)], [commission, str(0)], [orderStatus, 'canceled'],[leverage, d(Leverage)]]
    caseTitle = 'timeInForce传GTC'
    open_cancel_hisOrder(NTS,symbol_,side,positionSide,caseTitle,param,OpenTrust_Assert,HisOrder_Assert,log_level,_type)

#taker 多笔不同价格的订单 部分成交后->剩余撤单
def makerOrderCase_takerMany_restCancel(NTS,face_userID,symbol,side,positionSide,log_level=None,_type=None):

    print(' CaseTitle = <<双向全仓 taker->maker->部分成交->剩余撤单>>')
    symbol_ = symbol + 'USDT'
    NTS_face = n_order(6, user_id=face_userID)  #对手方
    OrderPrice = newPrice(NTS_face, symbol, _type=3) #成交价
    tickSize = float(NTS.instrument[symbol][0])
    face = pre.GetFaceSide(Side=side)
    paramList = [['tradeType',tradeType],['marginType',marginType],['orderType',orderType],['symbol',symbol_],['postOnly',False],['timeInForce','GTC'],['side',face[0]],['positionSide',face[1]],['price',str(OrderPrice)],['orderQty',2]]
    maker=0;case_mark=1;S=0
    for i in range(5): #先铺盘口maker多单，数量2,下5次订单共10张
        orderPrice = truncate(d(OrderPrice)-d(i+1)*d(tickSize),2)
        caseParamFace = dict(paramList);caseParamFace['price'] = str(orderPrice)
        face_r = NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        if e(face_r)[0]:maker=maker+1;printl(log_level,' maker下单->price='+str(orderPrice) + ' orderId='+ face_r['data']['orderId']);Count('Maker下单请求',1,1,0,0)
        else: printl(log_level,' maker下单失败',face_r);u(0);Count('maker下单失败',1,0,1,0)
    if maker == 5: #下taker订单,数量15张,剩余5张挂盘口(taker变成maker)
        caseParam = dict(paramList);caseParam['side'] = side;caseParam['positionSide'] = positionSide;caseParam['price'] = str(OrderPrice);caseParam['orderQty'] = 15
        taker_r = NTS.order(log_level=log_level, caseParam=caseParam)
        if  e(taker_r)[0]: printl(log_level,' taker下单->price='+str(OrderPrice) + ' orderId='+ taker_r['data']['orderId']);S=S+1;Count('Maker下单请求',1,1,0,0)
        else:  printl(log_level,' taker下单失败',taker_r);case_mark=0;Count('taker下单失败',1,0,1,0)
    else: printl(log_level,' 对手方下单笔数小于5笔,实际=', maker);return 0
    P=0;block=0
    if case_mark:
        r = NTS.OpenOrders(log_level=log_level, tradeType=tradeType, orderId=taker_r['data']['orderId'])
        if r['data']['list'][0]['orderStatus'] == 'partially_filled': printl(log_level,' 当前委托-订单状态为部分成交: 验证成功');S=S+1;Count('当前委托',1,1,0,0)
        else: printl(log_level,' 当前委托-订单状态为部分成交: 验证失败,预期=partially_filled'+ '实际='+r['data']['list'][0]['orderStatus']);Count('当前委托验证失败',1,0,1,0)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize']==5: printl(log_level,'历史成交-成交明细-数据条数5条: 验证成功');P=1;S=S+1;Count('历史成交-成交明细',1,1,0,0)
        else: P=0; u(0);printl(log_level,'历史成交-成交明细-数据条数5条：验证失败',r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        if P:
            for  i in r1['data']['list']:
                if not float(i['filledQty'])==2: case_mark=0 ;u(0);break;
                else: P=P+1
            if P==6:    S = S+1
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer=truncate(_balances['data'][0]['maxWithdrawAmount'],8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        # 撤单
        cancel=NTS.orderCancel(tradeType, symbol_, taker_r['data']['orderId'], log_level=log_level)
        if e(cancel)[0]:printl(log_level,' 撤单成功');S=S+1;Count('撤单成功',1,1,0,0)
        else:printl(log_level,' 撤单失败',cancel);Count('撤单失败',1,0,1,0)
        hisOrders_r = NTS.hisOrders(log_level=log_level,orderId=taker_r['data']['orderId'])
        if e(hisOrders_r)[0]:
            if  hisOrders_r['data']['list'][0]['orderStatus'] == 'partially_filled_canceled':
                printl(log_level,' 撤单成功--历史订单-状态为部分成交撤单：验证成功');S =S +1;Count('历史订单',1,1,0,0)
            else:  printl(log_level,' 撤单成功--历史订单-状态为部分成交撤单：验证失败,预期=partially_filled_canceled'+ '实际='+ hisOrders_r['data']['list'][0]['orderStatus']);u(0);Count('历史订单',1,0,1,0)
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer = truncate(_balances['data'][0]['maxWithdrawAmount'], 8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'funding';toAccountType = 'Futures'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        u(1,all=S,pass_=S-block)

#taker 多笔不同价格的订单 部分成交后->全部成交
def makerOrderCase_takerToMaker(NTS,face_userID,symbol,side,positionSide,log_level=None,_type=None):

    print(' CaseTitle = <<双向全仓 taker->maker->部分成交->全部成交>>')
    symbol_ = symbol + 'USDT'
    NTS_face = n_order(6, user_id=face_userID)  #对手方
    OrderPrice = newPrice(NTS_face, symbol, _type=3) #成交价
    tickSize = float(NTS.instrument[symbol][0])
    face = pre.GetFaceSide(Side=side)
    paramList = [['tradeType',tradeType],['marginType',marginType],['orderType',orderType],['symbol',symbol_],['postOnly',False],['timeInForce','GTC'],['side',face[0]],['positionSide',face[1]],['price',str(OrderPrice)],['orderQty',2]]
    maker=0;case_mark=1;S=0
    for i in range(5): #先铺盘口maker多单，数量2,下5次订单共10张
        orderPrice = truncate(d(OrderPrice)-d(i+1)*d(tickSize),2)
        caseParamFace = dict(paramList);caseParamFace['price'] = str(orderPrice)
        face_r = NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        if e(face_r)[0]:maker=maker+1;printl(log_level,' maker下单->price='+str(orderPrice) + ' orderId='+ face_r['data']['orderId']);Count('Maker下单请求',1,1,0,0)
        else: printl(log_level,' maker下单失败',face_r);u(0);Count('maker下单失败',1,0,1,0)
    if maker == 5: #下taker订单,数量15张,剩余5张挂盘口(taker变成maker)
        caseParam = dict(paramList);caseParam['side'] = side;caseParam['positionSide'] = positionSide;caseParam['price'] = str(OrderPrice);caseParam['orderQty'] = 15
        taker_r = NTS.order(log_level=log_level, caseParam=caseParam)
        if  e(taker_r)[0]: printl(log_level,' taker下单->price='+str(OrderPrice) + ' orderId='+ taker_r['data']['orderId']);S=S+1;Count('Maker下单请求',1,1,0,0)
        else:  printl(log_level,' taker下单失败',taker_r);case_mark=0;Count('taker下单失败',1,0,1,0)
    else: printl(log_level,' 对手方下单笔数小于5笔,实际=', maker);return 0
    P=0;block=0
    if case_mark:
        r = NTS.OpenOrders(log_level=log_level, tradeType=tradeType, orderId=taker_r['data']['orderId'])
        if r['data']['list'][0]['orderStatus'] == 'partially_filled': printl(log_level,' 当前委托-订单状态为部分成交: 验证成功');S=S+1;Count('当前委托',1,1,0,0)
        else: printl(log_level,' 当前委托-订单状态为部分成交: 验证失败,预期=partially_filled'+ '实际='+r['data']['list'][0]['orderStatus']);Count('当前委托验证失败',1,0,1,0)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize']==5: printl(log_level,' 历史成交-成交明细-数据条数5条: 验证成功');P=1;S=S+1;Count('历史成交-成交明细',1,1,0,0)
        else: P=0; u(0);printl(log_level,' 历史成交-成交明细-数据条数5条：验证失败',r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        if P:
            for  i in r1['data']['list']:
                if not float(i['filledQty'])==2: case_mark=0 ;u(0);break;
                else: P=P+1
            if P==6:    S = S+1
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer=truncate(_balances['data'][0]['maxWithdrawAmount'],8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        # 剩余部分 对手方全部吃掉
        caseParamFace = dict(paramList);caseParamFace['orderQty'] = 5
        face_r = NTS_face.order(log_level=log_level,caseParam=caseParamFace)
        if e(face_r)[0]: printl(log_level,' 剩余部分全部成交> 对手方下单成功', face_r['data']['orderId']);Count('对手方下单请求成功',1,1,0,0)
        dataCheck.openOrdersCheck(NTS, taker_r, e(taker_r), 1, '当前委托查询', log_level, tradeType, symbol_,openFlag=False)
        dataCheck.HistoryOrdersCheck(NTS, taker_r, e(taker_r), 1, '历史委托查询', log_level, tradeType, symbol_)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize'] == 5:printl(log_level, ' 历史成交-成交明细-数据条数5条: 验证成功');P = 1;S = S + 1;Count('历史成交-成交明细',1,1,0,0)
        else:P = 0; u(0);printl(log_level, ' 历史成交-成交明细-数据条数5条：验证失败', r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer = truncate(_balances['data'][0]['maxWithdrawAmount'], 8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        u(1,all=S,pass_=S-block)

#taker 多笔不同价格的订单 部分成交后->剩余被部分成交->用户撤单
def makerOrderCase_takerMany_restPartialFilled_restCancel(NTS,face_userID,symbol,side,positionSide,log_level=None,_type=None):

    print(' CaseTitle = <<双向全仓 taker->maker->部分成交->部分成交->撤单>>')
    symbol_ = symbol + 'USDT'
    NTS_face = n_order(6, user_id=face_userID)  #对手方
    OrderPrice = newPrice(NTS_face, symbol, _type=3) #成交价
    tickSize = float(NTS.instrument[symbol][0])
    face = pre.GetFaceSide(Side=side)
    paramList = [['tradeType',tradeType],['marginType',marginType],['orderType',orderType],['symbol',symbol_],['postOnly',False],['timeInForce','GTC'],['side',face[0]],['positionSide',face[1]],['price',str(OrderPrice)],['orderQty',2]]
    maker=0;case_mark=1;S=0
    for i in range(5): #先铺盘口maker多单，数量2,下5次订单共10张
        orderPrice = truncate(d(OrderPrice)-d(i+1)*d(tickSize),2)
        caseParamFace = dict(paramList);caseParamFace['price'] = str(orderPrice)
        face_r = NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        if e(face_r)[0]:maker=maker+1;printl(log_level,' maker下单->price='+str(orderPrice) + ' orderId='+ face_r['data']['orderId']);Count('Maker下单请求',1,1,0,0)
        else: printl(log_level,' maker下单失败',face_r);u(0);Count('maker下单失败',1,0,1,0)
    if maker == 5: #下taker订单,数量15张,剩余5张挂盘口(taker变成maker)
        caseParam = dict(paramList);caseParam['side'] = side;caseParam['positionSide'] = positionSide;caseParam['price'] = str(OrderPrice);caseParam['orderQty'] = 15
        taker_r = NTS.order(log_level=log_level, caseParam=caseParam)
        if  e(taker_r)[0]: printl(log_level,' taker下单->price='+str(OrderPrice) + ' orderId='+ taker_r['data']['orderId']);S=S+1;Count('Maker下单请求',1,1,0,0)
        else:  printl(log_level,' taker下单失败',taker_r);case_mark=0;Count('taker下单失败',1,0,1,0)
    else: printl(log_level,' 对手方下单笔数小于5笔,实际=', maker);return 0
    P=0;block=0
    if case_mark:
        r = NTS.OpenOrders(log_level=log_level, tradeType=tradeType, orderId=taker_r['data']['orderId'])
        if r['data']['list'][0]['orderStatus'] == 'partially_filled': printl(log_level,' 当前委托-订单状态为部分成交: 验证成功');S=S+1;Count('当前委托',1,1,0,0)
        else: printl(log_level,' 当前委托-订单状态为部分成交: 验证失败,预期=partially_filled'+ '实际='+r['data']['list'][0]['orderStatus']);Count('当前委托验证失败',1,0,1,0)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize']==5: printl(log_level,' 历史成交-成交明细-数据条数5条: 验证成功');P=1;S=S+1;Count('历史成交-成交明细',1,1,0,0)
        else: P=0; u(0);printl(log_level,' 历史成交-成交明细-数据条数5条：验证失败',r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        if P:
            for  i in r1['data']['list']:
                if not float(i['filledQty'])==2: case_mark=0 ;u(0);break;
                else: P=P+1
            if P==6:    S = S+1
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer=truncate(_balances['data'][0]['maxWithdrawAmount'],8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)

        # 剩余订单,部分成交3张
        caseParamFace = dict(paramList);caseParamFace['orderQty'] = 3
        NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        dataCheck.openOrdersCheck(NTS, taker_r, e(taker_r), 1, '当前委托查询', log_level, tradeType, symbol_,openFlag=True)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize'] == 6: printl(log_level,' 剩余数量部分成交--成交明细-数据条数6条: 验证成功');Count('历史成交-成交明细',1,1,0,0)
        else:printl(log_level, ' 剩余数量部分成交--成交明细-数据条数6条: 验证失败', r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        # 最后剩余部分,进行撤单
        cancel = NTS.orderCancel(tradeType, symbol, taker_r['data']['orderId'], log_level=log_level)
        if e(cancel)[0]: printl(log_level,' 最后剩余数量-再撤单：撤单成功');Count('撤单',1,1,0,0)
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer = truncate(_balances['data'][0]['maxWithdrawAmount'], 8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        u(1,all=S,pass_=S-block)

#taker 多笔不同价格的订单 部分成交后->剩余被部分成交->全部成交
def makerOrderCase_takerMany_restPartialFilled_filled(NTS,face_userID,symbol,side,positionSide,log_level=None,_type=None):

    print(' CaseTitle = <<双向全仓 taker->maker->部分成交->部分成交->全部成交>>')
    symbol_ = symbol + 'USDT'
    NTS_face = n_order(6, user_id=face_userID)  #对手方
    OrderPrice = newPrice(NTS_face, symbol, _type=3) #成交价
    tickSize = float(NTS.instrument[symbol][0])
    face = pre.GetFaceSide(Side=side)
    paramList = [['tradeType',tradeType],['marginType',marginType],['orderType',orderType],['symbol',symbol_],['postOnly',False],['timeInForce','GTC'],['side',face[0]],['positionSide',face[1]],['price',str(OrderPrice)],['orderQty',2]]
    maker=0;case_mark=1;S=0
    for i in range(5): #先铺盘口maker多单，数量2,下5次订单共10张
        orderPrice = truncate(d(OrderPrice)-d(i+1)*d(tickSize),2)
        caseParamFace = dict(paramList);caseParamFace['price'] = str(orderPrice)
        face_r = NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        if e(face_r)[0]:maker=maker+1;printl(log_level,' maker下单->price='+str(orderPrice) + ' orderId='+ face_r['data']['orderId']);Count('Maker下单请求',1,1,0,0)
        else: printl(log_level,' maker下单失败',face_r);u(0);Count('maker下单失败',1,0,1,0)
    if maker == 5: #下taker订单,数量15张,剩余5张挂盘口(taker变成maker)
        caseParam = dict(paramList);caseParam['side'] = side;caseParam['positionSide'] = positionSide;caseParam['price'] = str(OrderPrice);caseParam['orderQty'] = 15
        taker_r = NTS.order(log_level=log_level, caseParam=caseParam)
        if  e(taker_r)[0]: printl(log_level,' taker下单->price='+str(OrderPrice) + ' orderId='+ taker_r['data']['orderId']);S=S+1;Count('Maker下单请求',1,1,0,0)
        else:  printl(log_level,' taker下单失败',taker_r);case_mark=0;Count('taker下单失败',1,0,1,0)
    else: printl(log_level,' 对手方下单笔数小于5笔,实际=', maker);return 0
    P=0;block=0
    if case_mark:
        r = NTS.OpenOrders(log_level=log_level, tradeType=tradeType, orderId=taker_r['data']['orderId'])
        if r['data']['list'][0]['orderStatus'] == 'partially_filled': printl(log_level,' 当前委托-订单状态为部分成交: 验证成功');S=S+1;Count('当前委托',1,1,0,0)
        else: printl(log_level,' 当前委托-订单状态为部分成交: 验证失败,预期=partially_filled'+ '实际='+r['data']['list'][0]['orderStatus']);Count('当前委托验证失败',1,0,1,0)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize']==5: printl(log_level,' 历史成交-成交明细-数据条数5条: 验证成功');P=1;S=S+1;Count('历史成交-成交明细',1,1,0,0)
        else: P=0; u(0);printl(log_level,' 历史成交-成交明细-数据条数5条：验证失败',r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        if P:
            for  i in r1['data']['list']:
                if not float(i['filledQty'])==2: case_mark=0 ;u(0);break;
                else: P=P+1
            if P==6:    S = S+1
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer=truncate(_balances['data'][0]['maxWithdrawAmount'],8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)

        # 剩余订单,部分成交3张
        caseParamFace = dict(paramList);caseParamFace['orderQty'] = 3
        NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        dataCheck.openOrdersCheck(NTS, taker_r, e(taker_r), 1, '当前委托查询', log_level, tradeType, symbol_,openFlag=True)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize'] == 6: printl(log_level,' 剩余数量部分成交--成交明细-数据条数6条: 验证成功');Count('历史成交-成交明细',1,1,0,0)
        else:printl(log_level, ' 剩余数量部分成交--成交明细-数据条数6条: 验证失败', r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        # 剩余部分,对手方全部成交2张
        caseParamFace = dict(paramList);caseParamFace['orderQty'] = 2
        face_r = NTS_face.order(log_level=log_level, caseParam=caseParamFace)
        if e(face_r)[0]: printl(log_level, ' 剩余部分全部成交> 对手方下单成功', face_r['data']['orderId']);Count('对手方下单请求成功', 1, 1, 0,0)
        dataCheck.openOrdersCheck(NTS, taker_r, e(taker_r), 1, ' 当前委托查询', log_level, tradeType, symbol_,openFlag=False)
        dataCheck.HistoryOrdersCheck(NTS, taker_r, e(taker_r), 1, ' 历史委托查询', log_level, tradeType, symbol_)
        r1 = NTS.hisTrades(log_level=log_level, orderId=taker_r['data']['orderId'])
        if r1['data']['totalSize'] == 7: printl(log_level,' 剩余部分全部成交--成交明细-数据条数7条: 验证成功');Count('历史成交-成交明细',1,1,0,0)
        else:printl(log_level, ' 剩余部分全部成交--成交明细-数据条数7条: 验证失败', r1['data']['totalSize']);Count('历史成交-成交明细',1,0,1,0)
        DataCheckResult = UserDataCheck.UsderDataCheckCase(NTS, log_level, option='123', )
        Count('冻结保证金、仓位、资金', 2, DataCheckResult, 2 - DataCheckResult, 0)
        _balances = NTS.Balance(currency="USDT")
        maxTransfer = truncate(_balances['data'][0]['maxWithdrawAmount'], 8)
        currency = 'USDT';amount = maxTransfer;fromAccountType = 'Futures';toAccountType = 'funding'
        if float(maxTransfer)==0:printl(log_level,' 最大可划转=0, 不进行划转');u(0,block=2);block=block+2;Count('合约转出资金请求失败',1,0,1,0)
        else:
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=toAccountType,toAccountType=fromAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 合约转出资金请求成功',str(amount));Count('合约转出资金请求成功',1,1,0,0)
            else : printl(log_level,' 合约转出资金请求失败',r);Count('合约转出资金请求失败',1,0,1,0)
            r = NTS.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType,toAccountType=toAccountType, log_level=log_level)
            if e(r)[0]:printl(log_level,' 资金转入合约请求成功');Count('资金转入合约请求成功',1,1,0,0)
            else: printl(log_level,' 资金转入合约请求失败', r);Count('资金转入合约请求失败',1,0,1,0)
        u(1,all=S,pass_=S-block)

def makerOrderCase_FrozenMarginCal(NTS,symbol,tradeType,log_level=None,_type=None):
    r=dataCheck.frozenMaringCheck(NTS, symbol, tradeType, log_level, title='<测试场景 冻结保证金验证>')
    if r: u(1);
    else: u(0);

def makerOrderCase_Other(NTS,symbol='',side='buy',positionSide='long',log_level=None,caseLevel=1,_type=None):
    if caseLevel >= 2:
        makerOrderCase_FrozenMarginCal(NTS,symbol,tradeType)

def makerOrderCaseList(NTS,symbol,side,positionSide,log_level=None,caseLevel=0,_type=None):
    if caseLevel == 0:
        makerOrderCase_P0(NTS,log_level,2)
    if caseLevel == 1:
        if len(str(side)) == 2:
            sideList=[param_dict.sideMap[int(str(side)[:1])],param_dict.sideMap[float(str(side)[1:2])]]
        else: sideList=[param_dict.sideMap[side]]
        if len(str(positionSide)) == 2:
            positionSideList=[param_dict.positionSideMap[int(str(positionSide)[:1])],param_dict.positionSideMap[int(str(positionSide)[1:2])]]
        else: positionSideList=[param_dict.positionSideMap[positionSide]]
        for positionSide in positionSideList:
            for side in sideList:
                if (side == 'buy'and positionSide == 'long') or (side == 'sell'and positionSide == 'short'):
                    makerOrderCase_002(NTS,symbol,side,positionSide,log_level,_type)
                    makerOrderCase_003(NTS,symbol,side,positionSide,log_level,_type)
                    makerOrderCase_004(NTS,symbol,side,positionSide,log_level,_type)
                    makerOrderCase_007(NTS,symbol,side, positionSide, log_level, _type)
                    if NTS.source=='API':
                        makerOrderCase_005(NTS,symbol,side,positionSide,log_level,_type) #web不支持 clOrdId
                        makerOrderCase_006(NTS,symbol,side,positionSide, log_level,_type) #web不支持 clOrdId

if __name__ == '__main__':
    pass
    # NTS = n_order(6, user_id=118958)
    # NTS = NtsApiOrder(6, user_id="10070")
    # makerOrderCase_P0(NTS, 2)  # 下单、当前委托、撤单、验证资金P0 (5个用例)
    # Count(summary=2)
    # makerOrderCase_002(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_003(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_004(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_005(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_006(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_007(NTS,"BTC","sell","short",2,2)
    # makerOrderCase_takerMany_restCancel(NTS,'97201979',"BTC",'sell','short',2)
    # makerOrderCase_takerToMaker(NTS,'97201979',"BTC",'buy','long',2)
    # makerOrderCase_takerMany_restPartialFilled_restCancel(NTS,'97201979',"BTC",'buy','long',2)
    # makerOrderCase_takerMany_restPartialFilled_filled(NTS,'97201979',"BTC",'buy','long',2)