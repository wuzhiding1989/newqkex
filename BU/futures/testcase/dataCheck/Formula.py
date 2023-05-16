import copy
from BU.NTS.dataCheck.dataCheck import getNowAccount,warning_rate,isOpen,t_risk_limit_leverage
from param.dict import SuccessMessage,FailMessage
from common import mysqlClient
from common.other import httpCheck as e
from UnitTest.com import LogName
from common.util import truncate, printc, printl, d, Count,LogOut
import BU.NTS.Calculator as cal

log_level = 0
thisCaseNumber = 0
tradeType = 'linearPerpetual';
symbol = 'BTCUSDT'
currency = 'USDT'
pageNum = 1
pageSize = 100
t = mysqlClient.mysql(7)

class Formula():
    def __init__(self,NTS_,symbol):
        MarginIsolated=0;unRealIsolated=0;MarginCross=0;unReal=0;Isolated={};OpenOrderDic={};PositionDic={}
        global NTS
        self.NTS = NTS_;NTS = NTS_
        self.instrumentList = NTS.instrumentList;Instument=NTS.instrument[symbol[:-4]]
        self.TakerFeeRate=Instument[2]
        self.CtVal = Instument[1]
        self.FundingRate=-0.0018830852
        self.MarkPrice = {"BTCUSDT": 16000, "ETHUSDT": 1600};self.Symbol=symbol
        self.IndexPrice = {"BTCUSDT": 16000, "ETHUSDT": 1600};
        self.CalOpenOrderDic=self.CalOpenOrder(self.instrumentList)
        self.CalPositionDic=self.CalPosition(self.instrumentList)
        self.Balance=self.Balance()
        self.Leverage=self.GetLeverage()
        self.WarnX=self.GetWarnX()
        if self.CalPositionDic:
            self.Equity_Isolated_Long=self.CalPositionDic[self.Symbol]['isolated_long'][1]#逐仓-多仓权益
            self.Equity_Isolated_Short = self.CalPositionDic[self.Symbol]['isolated_short'][1] #逐仓-空仓权益
            self.PositionQty_Isolated_Long=self.CalPositionDic[self.Symbol]['isolated_long'][5] #逐仓- 多仓 持仓数量
            self.PositionQty_Isolated_Short = self.CalPositionDic[self.Symbol]['isolated_short'][5]  # 逐仓- 多仓 持仓数量
            self.PositionValue_Isolated_Long=self.CalPositionDic[self.Symbol]['isolated_long'][0] #逐仓-多仓 持仓价值
            self.PositionValue_Isolated_Short = self.CalPositionDic[self.Symbol]['isolated_short'][0]  # 逐仓-多仓 持仓价值
            self.PositionValue_Cross_Short = self.CalPositionDic[self.Symbol]['cross_short'][0]  # 全仓-空仓 持仓价值
            self.PositionValue_Cross_Long = self.CalPositionDic[self.Symbol]['cross_long'][0]  # 全仓-多仓 持仓价值

    # 掛單接口：
    def CalOpenOrder(self,instrumentList):
        OpenOrderDic={};FrozenMargin=d(0);DefaultList=[0,0];
        for symbol in instrumentList:
            OpenOrderDic[symbol]={'isolated_buy':copy.deepcopy(DefaultList),'isolated_sell':copy.deepcopy(DefaultList),'cross_buy':copy.deepcopy(DefaultList),'cross_sell':copy.deepcopy(DefaultList)};
        OpenOrderRes = self.NTS.OpenOrders(tradeType=tradeType, pageSize=100);
        if e(OpenOrderRes)[0]:
            for openOrder in OpenOrderRes['data']['list']:
                symbol=openOrder['symbol']
                coinValue = d(self.NTS.instrument[symbol[:-4]][1])
                Key = openOrder['marginType'] + '_' + openOrder['side']
                #分别计算：挂单价值
                if isOpen(openOrder['side'], openOrder['positionSide']):
                    OpenOrderDic[symbol][Key][0] = OpenOrderDic[symbol][Key][0] + d(openOrder['leavesQty']) * d(openOrder['price']) * coinValue
                    FrozenMargin =FrozenMargin+ cal.FrozenMargin(openOrder['side'], openOrder['price'], openOrder['leavesQty'],self.TakerFeeRate,openOrder['leverage'],self.CtVal)
                else:
                    OpenOrderDic[symbol][Key][1]=OpenOrderDic[symbol][Key][1]+float(openOrder['leavesQty'])
                    # print(openOrder['symbol'],openOrder['positionSide'],openOrder['leavesQty'])
            if OpenOrderRes['data']['totalPage'] > 1:
                for i in range(OpenOrderRes['data']['totalPage']):
                    if i + 2 <= OpenOrderRes['data']['totalPage']:
                        OpenOrderRes = NTS.openOrders(log_level=log_level, tradeType=tradeType,pageSize=100, pageNum=i + 2);
                        for openOrder in OpenOrderRes['data']['list']:
                            symbol = openOrder['symbol']
                            if isOpen(openOrder['side'], openOrder['positionSide']):
                                FrozenMargin = FrozenMargin + cal.FrozenMargin(openOrder['side'],openOrder['price'],openOrder['leavesQty'],self.TakerFeeRate,openOrder['leverage'], self.CtVal)
        self.FrozenMargin=FrozenMargin
        return OpenOrderDic
    #持仓接口： 获取持仓价值、维持保证金率
    def CalPosition(self,instrumentList):
        PositionDic = {};self.PositionMargin_Cross=d(0);self.UnReal_Cross=d(0);self.PositionMargin_Isolated=d(0);self.UnReal_Isolated=d(0);
        self.CalPositionMap={};PositionMap={};self.PositionMap=PositionMap
        for symbol in instrumentList:
            DefaultList=[0,0,0,0,0,0];DefaultDic={};
            PositionDic[symbol]={'isolated_long':copy.deepcopy(DefaultList),'isolated_short':copy.deepcopy(DefaultList),'cross_long':copy.deepcopy(DefaultList),'cross_short':copy.deepcopy(DefaultList)}
            PositionMap[symbol]={'isolated_long': {},'isolated_short':copy.deepcopy(DefaultDic),'cross_long':copy.deepcopy(DefaultDic),'cross_short':copy.deepcopy(DefaultDic)}
        PositionRes = self.NTS.position(log_level=0, tradeType='linearPerpetual')
        if e(PositionRes)[0]:
            if PositionRes['data'].__len__() > 0:
                for i in PositionRes['data']:
                    Key = i['marginType'] + '_' + i['positionSide'];symbol=i['symbol']
                    positionMargin = 'posMargin' if 'positionMargin' not in i.keys() else 'positionMargin';
                    # MarkPrice = d(19500) if symbol == 'BTCUSDT' else d(1800)

                    positionValue = self.MarkPrice[symbol] * d(i['positionAmt']) * d(self.NTS.instrument[symbol[:-4]][1])
                    PositionDic[symbol][Key][0]=positionValue
                    PositionDic[symbol][Key][1]=d(i[positionMargin]) + d(i['unrealisedPnl'])
                    if self.NTS.source=='API':
                        PositionDic[symbol][Key][2] = i['maintMarginRatio']
                        PositionDic[symbol][Key][3] = i['insuranceLevel']
                    PositionDic[symbol][Key][4] = i['availPos']
                    PositionDic[symbol][Key][5] = i['positionAmt']

                    CalUnRealisePnl=cal.UnRealisePnl(i['positionSide'], self.MarkPrice[symbol], i['avgEntryPrice'], i['positionAmt'],self.CtVal)
                    CalPositionMargin=cal.PositionMargin(self.MarkPrice[symbol], i['positionAmt'],self.CtVal,i['leverage'])
                    PositionMap[symbol][Key]['CalUnRealisePnl']=CalUnRealisePnl
                    PositionMap[symbol][Key]['CalPositionMargin'] = CalPositionMargin
                    PositionMap[symbol][Key]['UnRealisePnl']=i['unrealisedPnl']
                    PositionMap[symbol][Key]['positionSide']=i['positionSide']
                    PositionMap[symbol][Key]['symbol'] = i['symbol']
                    PositionMap[symbol][Key]['markPrice'] =self.MarkPrice[symbol]
                    PositionMap[symbol][Key]['positionMargin'] = i['positionMargin'] if not self.NTS.source=='web' else i['posMargin']
                    if self.NTS.source=='web' : PositionMap[symbol][Key]['earningRate'] = i['earningRate']
                    PositionMap[symbol][Key]['avgEntryPrice_positionAmt_ctVal'] = i['avgEntryPrice']+'_'+i['positionAmt']+'_'+self.CtVal
                    # self.CalPositionMap[symbol]={}
                    # self.CalPositionMap[symbol].update({Key:CalUnRealisePnl})
                    #单独 计算 全仓、逐仓 的 总持仓冻结、总未实现盈亏
                    if i['marginType']=='cross':    self.PositionMargin_Cross+=d(i[positionMargin]);self.UnReal_Cross+=d(i['unrealisedPnl']);
                    else:   self.PositionMargin_Isolated += d(i[positionMargin]);self.UnReal_Isolated+=d(i['unrealisedPnl']);
            self.PositionMap=PositionMap
        else:print(f'{self.NTS.user_id}持仓查询异常:',e(PositionRes));return False
        return PositionDic
    # 资金接口
    def Balance(self):
        BalanceRes=self.NTS.Balance(currency='USDT');
        if e(BalanceRes)[0]:
            BalanceRes=BalanceRes['data'][0]
            self.Balance_Equity=BalanceRes['marginEquity']
            self.Balance_Unreal = BalanceRes['profitUnreal'] if self.NTS.source=='API' else  0
            self.Balance_Frozen = BalanceRes['marginFrozen']
            self.Balance_MarginPosition=BalanceRes['marginPosition']
            self.Balance_Available = BalanceRes['marginAvailable']
            self.Balance_WithDrawAmount= BalanceRes['maxWithdrawAmount']
        else:printc(NTS.source+'资金查询异常',BalanceRes)
    #获取风险系数
    def GetWarnX(self):
        warnX = warning_rate(self.Symbol);warningX = warnX[0][0]
        return warningX
    #最大划转、可用保证金计算
    def MaxTransferOut(self,marginType,log_level=None):
        symbol=self.Symbol; result=True
        if marginType=='isolated':
            # warnX = warning_rate(symbol);warningX = warnX[0][0]  #风险系数
            MaintMarginRatio=self.CalPositionDic[symbol][marginType+'_long'][2]
            Equity=self.CalPositionDic[symbol][marginType+'_long'][1]
            PositionAviQty=self.CalPositionDic[symbol][marginType+'_long'][4]
            MarkPrice=self.MarkPrice[symbol]
            WarnMarginRate=d(self.WarnX)*d(MaintMarginRatio)
            printl(log_level,f'marginType={marginType},权益={Equity},WarnMarginRate={WarnMarginRate},FundingRate={self.FundingRate},PositionQty={PositionAviQty},MarkPrice{MarkPrice}')
            TransferAmout=cal.TransferAmount(MarginType=marginType,EquityIsolated=Equity,WarnMarginRate=WarnMarginRate,Side='buy',FundingRate=self.FundingRate,TakerFeeRate=self.TakerFeeRate,PositionQty=PositionAviQty,MarkPrice=MarkPrice,Ctval=self.CtVal,log_level=log_level)
            printl(log_level,f'{symbol} {marginType} buy 最大可转出',TransferAmout)
        else:
            self.Amount = getNowAccount(NTS.user_id)
            equity=d(self.Amount)+d(self.UnReal_Isolated)+d(self.UnReal_Cross)
            # printl(log_level,f'全仓保证金: {self.PositionMargin_Cross}')
            # printl(log_level,f'逐仓保证金: {self.PositionMargin_Isolated}')
            # printl(log_level, f'逐仓未实现盈亏: {self.UnReal_Isolated}')
            # printl(log_level, f'冻结资金: {self.Balance_Frozen}')
            AvailMargin=cal.AvailMargin(equity, self.Balance_Frozen, self.PositionMargin_Cross, self.PositionMargin_Isolated + self.UnReal_Isolated, 0)
            TransferAmout = cal.TransferAmount(AvailMargin,self.Amount)
            if float(AvailMargin)==float(self.Balance_Available): pass #printl(log_level,'可用保证金'+SuccessMessage);Count('公式-可用保证金',1,1,0,0)
            else: pass
                # printc('公式-可用保证金'+FailMessage,' 预期:',AvailMargin,'实际:',self.Balance_Available);Count('公式-可用保证金',1,1,0,0)
                # LogOut('公式-可用保证金'+FailMessage,LogName)
                # LogOut(f' 账户权益 {equity}  余额{self.Amount}+ 逐仓未实现盈亏{self.UnReal_Isolated}+ 全仓未实现盈亏{self.UnReal_Cross}',LogName)
                # LogOut(f'冻结资金: {self.Balance_Frozen}全仓保证金: {self.PositionMargin_Cross}逐仓保证金: {self.PositionMargin_Isolated} ',LogName)
            self.MaxTransferOut_={"Cal_TransferAmout":TransferAmout,"Balance_WithDrawAmount":self.Balance_WithDrawAmount,"Equity":equity,"PositionMargin_Cross":self.PositionMargin_Cross,"PositionMargin_Isolated":self.PositionMargin_Isolated,"UnReal_Isolated":self.UnReal_Isolated,"Balance_Frozen":self.Balance_Frozen}
            if float(TransferAmout)==float(self.Balance_WithDrawAmount): printl(log_level,self.NTS.source+'公式-最大可划转'+SuccessMessage);Count(self.NTS.source+'公式-最大可划转',1,1,0,0);
            else: printc(NTS.user_id+NTS.source+'公式-最大可划转'+FailMessage,' 预期:',TransferAmout,'实际:',self.Balance_WithDrawAmount);Count('公式-最大可划转',1,0,1,0);LogOut('公式-最大可划转'+FailMessage+str(self.MaxTransferOut_),LogName);result=False
        return [TransferAmout,result]
    #维持保证金、风险率 计算 - brian
    def MaintMaringCal(self,marginType,log_level=None,PositionSide='long'):
        O=self.CalOpenOrderDic[self.Symbol]
        MaintMargin = d(0)
        if marginType=='cross':
            for symbol in self.instrumentList:
                P = self.CalPositionDic[symbol]
                Number=0
                for i in P:
                    if marginType in str(i):
                        Number+=1
                        #维持保证金=维持保证金率*数量*面值*标记价
                        Tem=d(P[i][2])*d(P[i][4])*d(self.CtVal)*self.MarkPrice[symbol]
                        MaintMargin+=Tem
                        # print(symbol,i,Tem)
            printl(log_level,'总维持保证金',MaintMargin)
            Equity=(d(self.Balance_Available) + d(self.PositionMargin_Cross))
            RiskRate=d(MaintMargin)/Equity
            printl(log_level,'风险率:',RiskRate)
            return [MaintMargin, Equity, MaintMargin / Equity]
        else:
            P = self.CalPositionDic[self.Symbol]
            for i in P:
                if marginType+'_'+PositionSide in str(i):
                    MaintMargin=d(P[i][2])*d(P[i][4])*d(self.CtVal)*d(self.MarkPrice[self.Symbol])
                    Equity=self.PositionMargin_Isolated+self.UnReal_Isolated
                    printl(log_level,f'维持保证金={MaintMargin},权益={Equity},风险率={MaintMargin/Equity}')
                    return [MaintMargin,Equity,MaintMargin/Equity]
    #冻结保证金 对比 - Case
    def FrozenMarginAssert(self,log_level=None):
        ModuleName='公式-冻结保证金'
        printl(log_level,f'挂单计算的冻结保证金:{self.FrozenMargin}, 资金接口返回的冻结保证金:{self.Balance_Frozen}')
        if float(self.FrozenMargin)==float(self.Balance_Frozen):
            printl(log_level,ModuleName+SuccessMessage);Count(ModuleName,1,1,0,0);return True
        else:
            printc(str(NTS.user_id)+ModuleName+FailMessage+f'挂单计算的冻结保证金:{self.FrozenMargin}, 资金接口返回的冻结保证金:{self.Balance_Frozen}')
            Count(ModuleName, 1, 0, 1, 0);LogOut(ModuleName+FailMessage+f'挂单计算的冻结保证金:{self.FrozenMargin}, 资金接口返回的冻结保证金:{self.Balance_Frozen}',LogName);return False

    # 冻结仓位 对比 - Case  Author : Brian
    def FrozenPositionAssert(self,log_level=None):
       # print(self.CalOpenOrderDic)
       # print(self.CalPositionDic)
       ModuleName='公式-冻结仓位';CaseResult=True
       for symbol in self.CalPositionDic:
           for _type in self.CalPositionDic[symbol]:
               OpenOrderKey=_type.replace('long','sell').replace('short','buy') #多仓 对应 挂单的平仓卖、空仓对应挂单的平仓买  有点绕
               Temp_Postiton=self.CalPositionDic[symbol][_type]
               Temp_OpenOrder=self.CalOpenOrderDic[symbol][OpenOrderKey]
               if not float(Temp_Postiton[5])-float(Temp_Postiton[4])==float(Temp_OpenOrder[1]):
                   ErrorMessage=f'{NTS.user_id} {symbol} {_type}冻结仓位不一致 仓位数量{Temp_Postiton[5]} 仓位可平{Temp_Postiton[4]}仓位冻结{float(Temp_Postiton[5])-float(Temp_Postiton[4])} 平仓挂单冻结{Temp_OpenOrder[1]}'
                   printc(ErrorMessage);LogOut(ErrorMessage,LogName);CaseResult=False
       if  CaseResult: printl(log_level,NTS.user_id+ModuleName+SuccessMessage);Count(ModuleName,1,1,0,0);
       else: Count(ModuleName, 1, 0, 1, 0);
       return CaseResult
       #获取杠杆
    def GetLeverage(self,MarginType=None):
        l={}
        LeverageRes=self.NTS.leverage_info(tradeType='linearPerpetual', symbol=self.Symbol,marginType=MarginType)
        if e(LeverageRes)[0]:
            for i in LeverageRes['data']:   l[i['marginType']]=i['leverage']
        return l
    #获取风险限额
    def GetRiskLimit(self,MarginType=None):
        Leverage=self.Leverage[MarginType]
        MarginTypeNumber=2 if MarginType=='cross' else 1
        RiskLimit=t_risk_limit_leverage(self.Symbol,Leverage,MarginTypeNumber)
        self.RiskLimit=RiskLimit[0][0]
        return RiskLimit[0][0]
    #获取用户风险额度
    def GetRiskAmout(self,MarginType=None,Side=None):
        OpenValue=F.CalOpenOrderDic[self.Symbol]
        PositionValue = F.CalPositionDic[self.Symbol]
        # PositionSide='long' if Side=='buy' else 'short'
        if MarginType=='cross':
            KeyOpen_Buy = MarginType + '_' + 'buy';KeyPosition_Buy=MarginType+'_'+'long'
            KeyOpen_Sell = MarginType + '_' + 'sell';KeyPosition_Sell = MarginType + '_' + 'short'
            LongValue=OpenValue[KeyOpen_Buy][0]+PositionValue[KeyPosition_Buy][0] #多仓总价值：持仓+挂单
            ShortValue = OpenValue[KeyOpen_Sell][0] + PositionValue[KeyPosition_Sell][0] #空仓总价值：持仓+挂单
            RiskAmout=[LongValue,'long',ShortValue,'short'] if LongValue>=ShortValue else [ShortValue,'short',LongValue,'long']
            return RiskAmout
    def GetMaxOpenQty(self,MarginType=None,Side=None,Price=None):
            #获取MarginType、Leverage对应的风险限额
            RiskLimit=self.GetRiskLimit(MarginType=MarginType);
            if MarginType == 'cross':
                Key=['cross_buy','cross_long'] if Side.lower()=='buy' else ['cross_sell','cross_short']
            else:
                Key = ['isolated_buy', 'isolated_long'] if Side.lower() == 'buy' else ['isolated_sell', 'isolated_short']
            #获取MarginType对应的仓位价值、挂单价值
            PositionValue=self.CalPositionDic[self.Symbol][Key[1]][0] #仓位价值
            OpenValue = self.CalOpenOrderDic[self.Symbol][Key[0]][0] #挂单价值
            # print('杠杆,风险额度,持仓价值,挂单价值',self.Leverage[MarginType],RiskLimit,PositionValue,OpenValue)
            #用可用 计算的最大可开[资金接口返回的可用]
            AvailMaxOpenQty = cal.MaxOpenQty(Side, self.Balance_Available, Price, self.Leverage[MarginType], self.TakerFeeRate, self.CtVal, bid1=0);self.AvailMaxOpenQty = AvailMaxOpenQty

            #用风险额度 计算最大可开
            if Side=='Buy' :self.RiskLimitOpenQty=(d(RiskLimit)-d(PositionValue)-OpenValue)/d(Price)/d(self.CtVal)
            else: self.RiskLimitOpenQty=(d(RiskLimit)-d(PositionValue)-OpenValue)/max(0,d(Price))/d(self.CtVal)

            # Mysql数据库中最大下张数量限制
            MysqlMaxOpenQtyLimitNumber = cal.t_order_volume_limit(self.Symbol)
            #可用计算的最大可开、风险限额最大可开 取小值
            #可开多数量 = min { 可开数量x ，（杠杆对应风险限额 - 仓位价值-当前委托价值） / 委托价格 ，最大单笔下单数量限制}
            Qty=min(AvailMaxOpenQty,self.RiskLimitOpenQty,MysqlMaxOpenQtyLimitNumber)

            #提供计算参数
            self.MaxOpenQty={'leverage':self.Leverage[MarginType],'RiskLimit':float(RiskLimit),'PositonValue':float(PositionValue),'OpenValue':float(OpenValue),'AvailMaxOpenQty':AvailMaxOpenQty,'RiskLimitOrderQty':float(self.RiskLimitOrderQty),"Ctval":float(self.CtVal),'TakerFeeRate':float(self.TakerFeeRate)}
            #返回最后结果
            return [Qty,truncate(Qty,0)]
    #持仓 浮动盈亏、浮动盈亏率、持仓保证金 验证 Case
    def PositionAssert(self,log_level=None):
        AssertResult=True;BlankPositionNumber=0
        Module_UnRealisePnl_Formula=self.NTS.source+'公式-未实现盈亏';Assert_UnRealisePnl_Formula=True
        Module_PositionMargin_Formula = self.NTS.source+'公式-持仓保证金';Assert_PositionMargin_Formula=True
        Module_UnRealisePnlRate_Formula = self.NTS.source+'公式-浮动盈亏率';Assert_UnRealisePnlRate_Formula = True
        for symbol in self.PositionMap:
            for MarginType_PositionSide in self.PositionMap[symbol]:
                if self.PositionMap[symbol][MarginType_PositionSide].__len__()>0:
                    PositionData=self.PositionMap[symbol][MarginType_PositionSide]

                    CalUnRealisePnlRate = d(PositionData['CalUnRealisePnl'] / d(PositionData['positionMargin']))
                    #未实现盈亏 检查
                    if float(PositionData['CalUnRealisePnl'])==float(PositionData['UnRealisePnl']): pass
                    else:
                        printc(f' {symbol}{MarginType_PositionSide}{Module_UnRealisePnl_Formula} {FailMessage} 预期 {PositionData["CalUnRealisePnl"]} 实际 {PositionData["UnRealisePnl"]}');
                        LogOut(f'{Module_UnRealisePnl_Formula} {FailMessage} {PositionData}',LogName);
                        Count(Module_UnRealisePnl_Formula,1,0,1,0);Assert_UnRealisePnl_Formula=False
                    #浮动盈亏率检查，仅支持web端
                    if self.NTS.source == 'web':
                        if not float(CalUnRealisePnlRate) == float(PositionData['earningRate']):
                            printc(f' {symbol}{MarginType_PositionSide}{Module_UnRealisePnlRate_Formula} {FailMessage} 预期 {float(CalUnRealisePnlRate)} 实际 {float(PositionData["earningRate"])}');
                            LogOut(f'{Module_UnRealisePnlRate_Formula} {FailMessage} 预期 {float(CalUnRealisePnlRate)} 实际 {float(PositionData["earningRate"])}', LogName);
                            Count(Module_UnRealisePnlRate_Formula, 1, 0, 1, 0);Assert_UnRealisePnlRate_Formula = False
                    # 持仓保证金检查
                    if float(PositionData['CalPositionMargin'])==float(PositionData['positionMargin']): pass
                    else:
                        printc(f'{symbol}{MarginType_PositionSide}{Module_PositionMargin_Formula} {FailMessage} 预期 {PositionData["CalPositionMargin"]} 实际 {PositionData["positionMargin"]}');
                        LogOut(f'{Module_PositionMargin_Formula} {FailMessage} {PositionData}',LogName);
                        Count(Module_PositionMargin_Formula,1,0,1,0);Assert_PositionMargin_Formula=False
                    if not Assert_UnRealisePnl_Formula or not Assert_PositionMargin_Formula or not Assert_UnRealisePnlRate_Formula:
                        if Assert_UnRealisePnl_Formula: Count(Module_UnRealisePnl_Formula,1,1,0,0);printl(log_level,f'{Module_UnRealisePnl_Formula} {SuccessMessage}');
                        if Assert_PositionMargin_Formula: Count(Module_PositionMargin_Formula,1,1,0,0);printl(log_level,f'{Module_PositionMargin_Formula} {SuccessMessage}');
                        if self.NTS.source=='web' and Assert_UnRealisePnlRate_Formula: Count(Module_UnRealisePnlRate_Formula, 1, 1, 0, 0);printl(log_level,f'{Module_UnRealisePnlRate_Formula} {SuccessMessage}');
                        return False
                else:BlankPositionNumber+=1
        #如果无仓位：则公式验证结果为 阻塞
        if  BlankPositionNumber==self.PositionMap.__len__():
            Count(Module_UnRealisePnl_Formula, 1, 0, 0, 1);
            Count(Module_PositionMargin_Formula, 1, 0, 0, 1);
            if self.NTS.source=='web': Count(Module_UnRealisePnlRate_Formula, 1, 0, 0, 1);
        #最终都成功
        if Assert_UnRealisePnl_Formula: Count(Module_UnRealisePnl_Formula,1,1,0,0);printl(log_level,f'{Module_UnRealisePnl_Formula} {SuccessMessage}');
        if Assert_PositionMargin_Formula: Count(Module_PositionMargin_Formula,1,1,0,0);printl(log_level,f'{Module_PositionMargin_Formula} {SuccessMessage}');
        if self.NTS.source=='web' and Assert_UnRealisePnlRate_Formula: Count(Module_UnRealisePnlRate_Formula, 1, 1, 0, 0);printl(log_level,f'{Module_UnRealisePnlRate_Formula} {SuccessMessage}');
        return True
    #资金 总持仓保证金、权益、验证
    def AccountAssert(self,log_level=None):
        MarginAll=self.PositionMargin_Cross+self.PositionMargin_Isolated
        Module_PositionMargin_Formula = self.NTS.source + '公式-持仓保证金';Assert_PositionMargin_Formula = True
        Module_Equity_Formula = self.NTS.source + '公式-账户权益';Assert_Equity_Formula = True
        Module_AvilMargin_Formula = self.NTS.source + '公式-可用保证金';Assert_AvilMargin_Formula = True

        #验证持仓保证金 ，如果校验失败，输出case失败、日志、统计失败case
        if not float(MarginAll) == float(self.Balance_MarginPosition):
            printc(f' {self.NTS.user_id}{Module_PositionMargin_Formula} {FailMessage} 预期 {MarginAll} 实际 {self.Balance_MarginPosition}');
            LogOut(f'{self.NTS.user_id}{Module_PositionMargin_Formula} {FailMessage} 预期 {MarginAll} 实际 {self.Balance_MarginPosition} ', LogName);
            Count(Module_PositionMargin_Formula, 1, 0, 1, 0); Assert_PositionMargin_Formula = False

        self.GetEquity()
        #验证账户权益 ，如果校验失败，输出case失败、日志、统计失败case
        if not float(self.Equity["Equity"]) == float(self.Balance_Equity):
            ErrorMessage=f' {self.NTS.user_id}{Module_Equity_Formula} {FailMessage} 预期 {self.Equity["Equity"]} 实际 {self.Balance_Equity}'
            printc(ErrorMessage);LogOut(f'{ErrorMessage} {self.Equity} ',LogName);
            Count(Module_Equity_Formula, 1, 0, 1, 0); Assert_Equity_Formula = False

        # 产品公式：可用 = 账户权益 - 委托保证金 - 全仓持仓保证金 - 逐仓权益 - 划转冻结； 逐仓权益=逐仓保证金+逐仓未实现盈亏
        self.AvilMargin = cal.AvailMargin(self.Equity["Equity"], self.Balance_Frozen, self.PositionMargin_Cross, self.PositionMargin_Isolated + self.UnReal_Isolated, 0)
        #可用保证金验证
        if not float(self.AvilMargin)==float(self.Balance_Available):
            ErrorMessage = f' {self.NTS.user_id}{Module_AvilMargin_Formula} {FailMessage} 预期 {self.AvilMargin} 实际 {self.Balance_Available}'
            printc(ErrorMessage);LogOut(f'{ErrorMessage} 账户权益={self.Equity["Equity"]}冻结={self.Balance_Frozen} 全仓保证金={self.PositionMargin_Cross}逐仓权益={self.PositionMargin_Isolated + self.UnReal_Isolated} ', LogName);
            Count(Module_AvilMargin_Formula, 1, 0, 1, 0);Assert_AvilMargin_Formula = False
        #最大可划转 验证
        Assert_MaxTransferOut=self.MaxTransferOut('cross',log_level=log_level)[1]

        if Assert_PositionMargin_Formula: Count(Module_PositionMargin_Formula,1,1,0,0);printl(log_level,f'{Module_PositionMargin_Formula} {SuccessMessage}');
        if Assert_Equity_Formula: Count(Module_Equity_Formula,1,1,0,0);printl(log_level,f'{Module_Equity_Formula} {SuccessMessage}');
        if Assert_AvilMargin_Formula: Count(Module_AvilMargin_Formula, 1, 1, 0, 0);printl(log_level,f'{Module_AvilMargin_Formula} {SuccessMessage}');
        if not Assert_PositionMargin_Formula or not Assert_Equity_Formula or not Assert_AvilMargin_Formula and not Assert_MaxTransferOut:
            return False
    #获取账户权益
    def GetEquity(self):
        UnReal_All=self.UnReal_Cross+self.UnReal_Isolated
        # print(self.Amount,self.UnReal_Cross,self.UnReal_Isolated)
        self.Amount = getNowAccount(NTS.user_id)
        Equity=cal.Equity(self.Amount, UnReal_All)
        self.Equity={"Equity":Equity,"Amount":self.Amount,"UnReal_All":UnReal_All,"UnReal_Cross":self.UnReal_Cross,"UnReal_Isolated":self.UnReal_Isolated}
        return Equity
    #获取预估资金费
    def ForecastFunding(self,marginType,log_level=None):
        if marginType=='cross':
            for symbol in self.instrumentList:
                crossPos = self.CalPositionDic[symbol]
                funding = 0
                totalFunding=0
                for tmp in crossPos:
                    funding = (crossPos[tmp]['cross_long'][5] - crossPos[tmp]['cross_short'][5]) * self.FundingRate
                    totalFunding += funding
                    printl(log_level, f'{tmp}的预估资金费={funding}')
                return
        else:
            isolatedfunding = {}
            for symbol in self.instrumentList:
                isolatedPos = self.CalPositionDic[symbol]
                for tmp in isolatedPos:
                    funding = (isolatedPos[tmp]['isolated_long'][5] - isolatedPos[tmp]['cross_short'][5]) * self.FundingRate
                    isolatedfunding[tmp]['funding']=funding
            return isolatedfunding
    #获取最高价格限制
    def LimitOrderPriceLimit(self,OrderPrice,OrderQty,Ctval):
        MarkPrice=self.MarkPrice[self.Symbol]
        IndexPrice=self.IndexPrice[self.Symbol]
        T=False
        if OrderPrice*OrderQty*Ctval>50000:
            MarkPriceRate = 0.05;IndexPriceRate = 0.08;T=True  # 临时写死,需要从db查询获取
        else:
            MarkPriceRate = 0.08;IndexPriceRate = 0.1;T=False  # 临时写死,需要从db查询获取
        MaxBuyPrice=min( d(MarkPrice)*(d(1+MarkPriceRate)),d(IndexPrice)*d(1+IndexPriceRate) )
        MinSellPrice = min(d(MarkPrice) * (d(1 - MarkPriceRate)), d(IndexPrice) * d(1 - IndexPriceRate))
        return [MaxBuyPrice,MinSellPrice,T]
def GetMarkPrice(MarkPrice=None,OrderRange=None,Side='buy'):
    P=1 if Side=='buy' else -1
    MarketPrice=d(MarkPrice)*(d(1)+d(OrderRange)*d(0.03)*d(P))
    return MarketPrice

if __name__ == '__main__':
    from BU.NTS.WebOrder import n_order
    Symbol='BTCUSDT'
    # NTS = NtsApiOrder(6, user_id='97201979')
    NTS = n_order(5, user_id='97201979')
    MaxTransferOut=Formula(NTS,Symbol).MaxTransferOut(marginType='isolated',log_level=0) #最大转出金额 计算
    # print(MaxTransferOut)
    # F=Formula(NTS, Symbol)
    # time.sleep(10000)
    # print(F.CalOpenOrderDic) #挂单价值
    # print(F.CalPositionDic)  # 持仓相关
                # 🀆🀆🀆🀆🀆★★★★★Formula Case - 3 ★★★★★🀆🀆🀆🀆🀆
    # F.FrozenMarginAssert(log_level=0)  # 1- 挂单冻结金额结果 验证
    # F.PositionAssert(log_level= 0) #2-持仓验证
    # F.AccountAssert(log_level= 0) #3-资金
    # Count(summary=1, log_level=2)
    # print('最高买入价\最低卖出价:',F.LimitOrderPriceLimit(19000,200,0.01))
    # print('市价:',GetMarkPrice(19500,0.9,'sell'))
    # time.sleep(10000)
    # print(F.CalOpenOrderDic) #挂单价值
    # print(F.CalPositionDic)  #仓位价值、保证金+未实现盈亏、维持保证金率、风险等级、可用仓位
    # Formula(NTS, Symbol).MaintMaringCal(marginType='cross',log_level=2) #维持保证金计算
    # Formula(NTS, Symbol).MaintMaringCal(marginType='isolated',log_level=2)
    # print('挂单冻结',f'{F.FrozenMargin}') #打印持仓冻结

    # F.GetRiskLimit(MarginType='isolated'); #获取风险限额(全仓、逐仓)
    # print(F.Leverage)
    # print('风险限额 ',f'{F.RiskLimit}') #打印风险限额
    # F.GetRiskAmout(MarginType='cross',Side='buy')
    # MaxQty=F.GetMaxOpenQty(MarginType='cross',Side='buy',Price=16000)
    # print(MaxQty)
    # print(F.MaxOpenQty)
    # time.sleep(10000)