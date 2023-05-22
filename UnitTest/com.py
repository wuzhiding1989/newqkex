from common.other import httpCheck as e
from common.util import printc,d,Count
from BU.NTS.dataCheck.dataCheck import newPrice
import common.mysqlClient as mysql
import copy,random
import BU.NTS.Calculator as cal

LogName = 'py5.log'
#获取挂单 买价、卖价 ；成交  买价、卖价    （待完善）
def getOrderPrice(side,option='maker'):
    if  str(side) in ['1','buy']:
        if option=='maker': return 15000
        if option == 'taker': return 25000
    if  str(side) in ['2','sell']:
        if option=='maker': return 25000
        if option == 'taker': return 15000

#判断是否平仓
def isClosePostionFlag(side,positionMode):
    if str(side) in ['1', 'buy']:
        if str(positionMode).upper() in ['short','2']: return True
        else: return True
    if str(side) in ['2', 'sell']:
        if str(positionMode).upper() in ['long','1']: return True
        else: return True

# 获取业务仓位模式
def GetBusinessName(PositionSide=None,MarginType=None):
    if PositionSide:
        BusinessName_1 = '单向' if PositionSide.lower() in ['both'] else '双向'
    else: BusinessName_1 ='双向'
    if MarginType:
        BusinessName_2 = '全仓' if str(MarginType).lower() in ['cross','none'] else '逐仓'
    else: BusinessName_2 = ''
    return BusinessName_1+BusinessName_2

# 获取反向的保证金模式
def GetFaceMarginType(MarginType=None):
    if MarginType:
        return 'isolated' if MarginType.lower() in ['cross','none'] else 'cross'

# Author: Brian 根据方向 获取对手方下单方向
def GetFaceSide(Side):
    if str(Side) in ['1', 'buy']: return ['sell','short']
    if str(Side) in ['2', 'sell']: return ['buy','long']

# Author: Brian 获取下单价格
def GetOrderPrice(NTS,symbol,Side=None,IsTrade=None):
    if IsTrade: OrderPrice = newPrice(NTS,symbol,_type=3)
    else: OrderPrice = newPrice(NTS,symbol,_type=1) if Side == 'buy' else newPrice(NTS,symbol,_type=2)
    return OrderPrice

# Author: Brian 根据方向 获取持仓方向
def GetPositionSide(Side,IsOpen=None,PositionSide=None):
    if PositionSide and PositionSide.lower() == 'both': return PositionSide
    # open：buy-long、sell-short
    if IsOpen: PositionSide_='long'  if Side == 'buy' else 'short'
    # close：buy-short、sell-long
    else: PositionSide_ = 'short' if  Side == 'buy' else 'long'
    return PositionSide_

def CaseLongTitle(CaseParam):
    PositionSide=CaseParam["positionSide"].lower()
    Side = CaseParam["side"].lower()
    if PositionSide=='long':
        CaseLongTitle="[开仓买入]" if Side=="buy" else "[平仓卖出]"
        return CaseLongTitle
    if PositionSide=='short':
        CaseLongTitle="[开仓卖出]" if Side=="sell" else "[平仓买入]"
        return CaseLongTitle

# CreateOrders函数使用说明: 默认全仓模式、开BTC限价买单不成交
# 下限价挂单 OrderParam=CreateOrders(NTS,marginType="cross",symbol="BTC",TradeFlag=False,MarketType=False,OpenFlag=True)
# 下限价成交 OrderParam=CreateOrders(NTS,marginType="cross",symbol="BTC",TradeFlag=True,MarketType=False,OpenFlag=True)
# 下市价成交 OrderParam=CreateOrders(NTS,marginType="cross",symbol="BTC",TradeFlag=True,MarketType=True,OpenFlag=True)
# 批量下单 BatchOrderParam=CreateOrders(NTS,marginType="cross",symbol=["BTC"],number=5,TradeFlag=False,MarketType=False,OpenFlag=True)
# 批量下单 BatchOrderParam=CreateOrders(NTS,marginType="cross",symbol=["BTC","ETH"],number=5,TradeFlag=False,MarketType=False,OpenFlag=True)
def CreateOrders(NTS, PositionSide=False, Side='buy', marginType='cross', symbol='BTC', OpenFlag=True, TradeFlag=False, MarketFlag=False,OrderQty=None, number=None, Lim_Mar=False,Cro_Iso=False, price=False, faceFlag=False):
    import param.OrderParams as OP
    # from UnitTest.com import GetPositionSide, GetOrderPrice, GetFaceSide
    BatchParam = []
    param = copy.deepcopy(OP.linear_isolated_param) if marginType=='isolated' else copy.deepcopy(OP.linear_cross_param)
    positionSide = GetPositionSide(Side, IsOpen=OpenFlag,PositionSide=PositionSide)
    face = GetFaceSide(Side)
    param['orderType'] = 'market' if MarketFlag else 'limit'
    if not type(symbol) == list :
        if price : param['price']= price
        else: param['price'] = GetOrderPrice(NTS, symbol, Side, IsTrade=False) if not TradeFlag else GetOrderPrice(NTS, symbol, Side, IsTrade=True)
        param['symbol'] = symbol + 'USDT'
    Map = {'side':face[0] if faceFlag else Side,'positionSide': face[1] if faceFlag else ('both' if positionSide.lower() in ('both') else positionSide)}
    for i in Map: param[i] = Map[i]
    if OrderQty: param["orderQty"]=OrderQty
    if not number: return param
    # 批量下单前置
    if number and 0 < number <= 20 and len(symbol) <= 2:
        if type(symbol) == list :
            for i in range(number):
                if len(symbol) == 1:symbol_1=symbol[0]
                else:symbol_1 = symbol[0] if i % 2 == 0 else symbol[1]
                BatchParam.append(copy.deepcopy(param))
                if price :  BatchParam[i]['price'] = price
                else: BatchParam[i]['price'] = GetOrderPrice(NTS, symbol_1, Side, IsTrade=False) if not TradeFlag else GetOrderPrice(NTS, symbol_1, Side, IsTrade=True)
                if Cro_Iso : BatchParam[i]['marginType']=random.choice(["cross","isolated"]) # 兼容批量下单全仓+逐仓模式混合
                if Lim_Mar : BatchParam[i]['orderType']=random.choice(["market","limit"]) # 兼容批量下单限价+市价订单混合
                BatchParam[i]['symbol'] = symbol_1 + 'USDT'
            return BatchParam
    else: printc(f'批量下单数量超过最大限制20笔,实际: {number}笔; 交易对数量最大2个,实际: {symbol}')

# Author: xie 获取最优N档价格
# 最优N档的多单Price = Min (卖(N)档,OrderRange(3%)）
# 最优N档的空单Price = Max (买(N)档,OrderRange(3%)）
# 多单OrderRange(3%) = 标记价格（1+3%）
# 空单OrderRange(3%) = 标记价格（1-3%）
def GetOptimumPrice(symbol='BTC',Side=None,PositionSide=None):
    # optimum_level = cal.t_symbol_optimum_level(symbol=symbol+'USDT')   # 最优N档从数据库获取
    # OrderRange = cal.t_symbol_optimum_rate(symbol=symbol+'USDT')   # 订单幅度从数据库获取
    optimum_level = 5
    OrderRange = 3
    indexPrice = '1111' # 获取标记价格
    bidsList =  sorted([1000,900,1100,1400,1300,1500],reverse=True)[optimum_level-1] # 买N档的值,从大到小取第N档的值
    asksList =  sorted([1000,1700,1200,1400,1300,1800],reverse=False)[optimum_level-1] # 卖N档的值,从小到大取第N档的值
    LongOrderRange = float(indexPrice) * (1+(OrderRange/100))
    ShortOrderRange = float(indexPrice) * (1-(OrderRange/100))
    if (Side == 'buy' and PositionSide == 'long') or (Side == 'sell' and PositionSide == 'long'):
        Price = min(float(bidsList),float(LongOrderRange))
    if (Side == 'sell' and PositionSide == 'short') or (Side == 'buy' and PositionSide == 'short'):
        Price = max(float(asksList),float(ShortOrderRange))
    return Price

# Author: xie 检查持有仓位存在数据、仓位数量是否等于持仓数量
def PositionCheck(NTS,tradeType='linearPerpetual',symbol=None,availPos=None,AvgPrice=None,Flag=None,CaseTitle=''):
        r= NTS.position(tradeType=tradeType,symbol=symbol)
        r1=r['data']['list'];
        if e(r)[0]:
            if r1.__len__()==1:
                if Flag:
                   AssertFieldList=([availPos,'positionAmt','仓位可平数量'],[AvgPrice,'avgEntryPrice','持仓均价'])
                   FieldNumber = 0
                   for Field in AssertFieldList:
                       if Field[0]:
                           if type(Field[0])==str: A=r1[0][Field[1]];B=Field[0]
                           else: A=float(r1[0][Field[1]]);B=float(Field[0])
                           if A==B:FieldNumber+=1
                           else: printc(f'{CaseTitle}持有仓位 {availPos}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                       else:FieldNumber+=1 #如果该字段不校验，则+1
                   if FieldNumber==AssertFieldList.__len__(): return True #预期 都正确,包括不校验也认为正确 则返回True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',r)

#  Author: Brian 检查当前委托是否存在，状态是否正确
def OpenOrdersCheck(NTS, OrderId, tradeType='linearPerpetual', Flag=None, CaseTitle='', Status=None,Fee=None):
        r= NTS.OpenOrders(tradeType=tradeType, orderId=OrderId)
        r1=r['data']['list'];
        if e(r)[0]:
            if r1.__len__()==1:
                if Flag:
                   AssertFieldList=([Status,'orderStatus','状态'],[Fee,'commission','手续费'])
                   FieldNumber = 0
                   for Field in AssertFieldList:
                       if Field[0]:
                           if type(Field[0])==str: A=r1[0][Field[1]];B=Field[0]
                           else: A=float(r1[0][Field[1]]);B=float(Field[0])
                           if A==B:FieldNumber+=1
                           else: printc(f'{CaseTitle}当前委托 {OrderId}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                       else:FieldNumber+=1 #如果该字段不校验，则+1
                   if FieldNumber==AssertFieldList.__len__(): return True #预期 都正确,包括不校验也认为正确 则返回True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',r)

# Author: xie 检查条件单存在数据、订单是否存在
def TriggerOrdersCheck(NTS,tradeType='linearPerpetual',symbol=None,stopOrderId=None,Flag=None,CaseTitle=''):
        r= NTS.OpenTriggerOrder(tradeType=tradeType,symbol=symbol,stopOrderId=stopOrderId)
        r1=r['data']['list']
        if e(r)[0]:
            if r1.__len__()==1:
                if Flag:
                   AssertFieldList=([stopOrderId,'stopOrderId','计划委托订单Id'])
                   FieldNumber = 0
                   for Field in AssertFieldList:
                       if Field[0]:
                           if type(Field[0])==str: A=r1[0][Field[1]];B=Field[0]
                           else: A=float(r1[0][Field[1]]);B=float(Field[0])
                           if A==B:FieldNumber+=1
                           else: printc(f'{CaseTitle}条件单 {stopOrderId}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                       else:FieldNumber+=1 #如果该字段不校验，则+1
                   if FieldNumber==AssertFieldList.__len__(): return True #预期 都正确,包括不校验也认为正确 则返回True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',r)

# Author: xie 检查已完全平仓记录存在数据、订单是否存在
def PositionClosedCheck(NTS,tradeType='linearPerpetual',symbol=None,Profit=None,Fee=None,Flag=None,CaseTitle=''):
        r= NTS.position_closed(tradeType=tradeType,symbol=symbol)
        r1=r['data']['list']
        if e(r)[0]:
            if r1.__len__()==1:
                if Flag:
                   AssertFieldList=([Profit,'realProfit','已实现盈亏'],[Fee,'commission','手续费'])
                   FieldNumber = 0
                   for Field in AssertFieldList:
                       if Field[0]:
                           if type(Field[0])==str: A=r1[0][Field[1]];B=Field[0]
                           else: A=float(r1[0][Field[1]]);B=float(Field[0])
                           if A==B:FieldNumber+=1
                           else: printc(f'{CaseTitle}已平仓 {Profit}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                       else:FieldNumber+=1 #如果该字段不校验，则+1
                   if FieldNumber==AssertFieldList.__len__(): return True #预期 都正确,包括不校验也认为正确 则返回True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',r)

# Author: xie 检查历史条件单是否存在，状态是否正确
def HisTriggerOrderCheck(NTS,tradeType='linearPerpetual',orderType=None,OrderId=None,Flag=None,CaseTitle=''):
        r= NTS.TriggerOrdersHistory(tradeType=tradeType,orderType=orderType,stopOrderId=OrderId)
        r1=r['data']['list']
        if e(r)[0]:
            if r1.__len__()==1:
                if Flag:
                   AssertFieldList=([OrderId,'stopOrderId','条件单id'],[orderType,'orderType','条件单类型'])
                   FieldNumber = 0
                   for Field in AssertFieldList:
                       if Field[0]:
                           if type(Field[0])==str: A=r1[0][Field[1]];B=Field[0]
                           else: A=float(r1[0][Field[1]]);B=float(Field[0])
                           if A==B:FieldNumber+=1
                           else: printc(f'{CaseTitle}历史条件单 {OrderId}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                       else:FieldNumber+=1 #如果该字段不校验，则+1
                   if FieldNumber==AssertFieldList.__len__(): return True #预期 都正确,包括不校验也认为正确 则返回True
                else:   return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',r)

# Author: Brian 检查历史委托是否存在，状态是否正确
def HisOrdersCheck(NTS, OrderId, tradeType='linearPerpetual',Flag=None, CaseTitle='', Status=None,Fee=None,OrderParam=None):
        hisOrders_r = NTS.hisOrders(tradeType=tradeType,orderId=OrderId)
        r1 = hisOrders_r['data']['list'];
        if e(hisOrders_r)[0]:
            if hisOrders_r['data']['list'].__len__()==1:
                if Flag:
                    list=[]
                    if OrderParam: list=[OrderParam["orderType"],"orderType","订单类型"]
                    AssertFieldList = [[Status, 'orderStatus', '状态'], [Fee, 'commission', '手续费']]+list
                    FieldNumber = 0
                    for Field in AssertFieldList:
                        #是否校验
                        if Field[0]:
                            if type(Field[0]) == str:   A = r1[0][Field[1]];B = Field[0]
                            else:   A = float(r1[0][Field[1]]);B = float(Field[0])
                            if A == B:  FieldNumber += 1
                            else:    printc(f'{CaseTitle} 历史订单-普通单 {OrderId}{Field[1]} 预期{Field[0]} 实际{r1[0][Field[1]]}');Count("历史订单",1,0,1,0);return False
                        else:   FieldNumber += 1  # 如果该字段不校验，则+1
                    if FieldNumber == AssertFieldList.__len__(): return True  # 预期 都正确,包括不校验也认为正确 则返回True
                else:
                    return False
            else:
                if Flag: return False
                else: return True
        else: printc(CaseTitle+'请求失败',hisOrders_r)

# Author: Brian 检查历史成交是否存在，状态是否正确
def HisTradeCheck(NTS, OrderId, tradeType='linearPerpetual', Flag=None, CaseTitle='', FilledQty=None, Fee=None,RealProfit=None,TakerFlag=None):
    HisTradesRes = NTS.hisTrades(orderId=OrderId)
    r1 = HisTradesRes['data']['list'];
    if e(HisTradesRes)[0]:
        if HisTradesRes['data']['list'].__len__() == 1:
            if Flag:
                AssertFieldList = ([FilledQty, 'filledQty', '状态'], [Fee, 'commission', '手续费'],[RealProfit,'realProfit','盈亏'],[TakerFlag,'taker','是否taker'])
                FieldNumber = 0
                for Field in AssertFieldList:
                    # 是否校验
                    if Field[0] is not None:
                        if type(Field[0]) == str:   A = r1[0][Field[1]];B = Field[0]
                        else:   A = float(r1[0][Field[1]]);B = float(Field[0])
                        if A == B:  FieldNumber += 1
                        else:   printc(f'{CaseTitle} 历史成交 {OrderId}{Field[2]} 预期{Field[0]} 实际{r1[0][Field[1]]}');return False
                    else:   FieldNumber += 1  # 如果该字段不校验，则+1
                if FieldNumber == AssertFieldList.__len__(): return True  # 预期 都正确,包括不校验也认为正确 则返回True
            else:   return False
        else:
            if Flag:    return False
            else:   return True
    else:   printc(CaseTitle + '请求失败', HisTradesRes)


# Author: Brian 试算手续费,盈亏
def GetFeeAndProfit(TradePrice,TradeQty,Ctval,FeeRate):
    Fee=d(TradePrice)*d(TradeQty)*d(Ctval)*d(FeeRate)
    return [Fee]
# print(GetFeeAndProfit(19303,2,0.01,0.0004))

# Author: Brian 获取平台所有交易用户 from db
def GetAllUsers():
    db = mysql.mysql(6, 1)
    dbName = 'qa_mulan_btc1.'
    r = db.mysql(f'select distinct uid from {dbName}t_order')
    UserList=r[:-1].split(',')
    return UserList
# print(GetAllUsers())