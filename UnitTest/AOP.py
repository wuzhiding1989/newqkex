import copy
from BU.NTS.ApiOrder import NtsApiOrder
from BU.NTS.dataCheck.dataCheck import isOpen
from common.other import httpCheck as e
from common.util import printc, d
import BU.NTS.Calculator as cal
tradeType = 'linearPerpetual';
class AOP:
    def __init__(self,NTS_,symbol,_type=None):#,NTS,symbol
        global NTS
        self.instrumentList = NTS_.instrumentList;
        Instument = NTS_.instrument[symbol[:-4]]
        self.TakerFeeRate = Instument[2];self.MakerFeeRate = Instument[3]
        self.CtVal = Instument[1]
        self.NTS=NTS_;NTS=NTS_
        self.MarkPrice = {"BTCUSDT": 19500, "ETHUSDT": 1800};
        if '1' in str(_type) or not _type:  self.OpenOrders = self.GetBalanceData()
        if '2' in str(_type) or not _type:  self.OpenOrders = self.GetOpenOrderData(self.instrumentList)
        if '3' in str(_type) or not _type:  self.Positions=self.GetPositionData(self.instrumentList)
        # if '1' in _type  and not _type: 查询持仓
        pass
    # 掛單接口：
    def GetOpenOrderData(self,instrumentList,log_level=None):
        OpenOrderDict={};FrozenMargin=d(0)
        BasicDict={"value": 0 , "coin" : 0}
        for symbol in instrumentList:
            OpenOrderDict[symbol]={"isolated": {"buy": copy.deepcopy(BasicDict), "sell": copy.deepcopy(BasicDict)},
             "cross": {"buy": copy.deepcopy(BasicDict), "sell": copy.deepcopy(BasicDict)}}
            OpenOrderRes = self.NTS.openOrders(tradeType=tradeType, symbol=symbol,pageSize=100);
            if e(OpenOrderRes)[0]:
                for openOrder in OpenOrderRes['data']['list']:
                    coinValue = d(self.NTS.instrument[symbol[:-4]][1])
                    MarginType=openOrder['marginType'];Side=openOrder['side']
                    #分别计算：挂单价值
                    if isOpen(openOrder['side'], openOrder['positionSide']):
                        OpenOrderDict[symbol][MarginType][Side]['value'] = OpenOrderDict[symbol][MarginType][Side]['value'] + d(openOrder['leavesQty']) * d(openOrder['price']) * coinValue
                        OpenOrderDict[symbol][MarginType][Side]['coin'] = OpenOrderDict[symbol][MarginType][Side]['coin'] + d(openOrder['leavesQty']) * d(openOrder['price'])
                        FrozenMargin =FrozenMargin+ cal.FrozenMargin(openOrder['side'], openOrder['price'], openOrder['leavesQty'],self.TakerFeeRate,openOrder['leverage'],self.CtVal)
                if OpenOrderRes['data']['totalPage'] > 1:
                    for i in range(OpenOrderRes['data']['totalPage']):
                        if i + 2 <= OpenOrderRes['data']['totalPage']:
                            OpenOrderRes = NTS.openOrders(symbol=symbol, log_level=log_level, tradeType=tradeType,pageSize=100, pageNum=i + 2);
                            for openOrder in OpenOrderRes['data']['list']:
                                if isOpen(openOrder['side'], openOrder['positionSide']):
                                    FrozenMargin = FrozenMargin + cal.FrozenMargin(openOrder['side'],openOrder['price'],openOrder['leavesQty'],self.TakerFeeRate,openOrder['leverage'], self.CtVal)
            self.FrozenMargin=FrozenMargin
        self.OpenOrders=OpenOrderDict
        return OpenOrderDict
    #持仓接口： 获取持仓价值、维持保证金率
    def GetPositionData(self,instrumentList):
        PositionDic = {};self.PositionMargin_Cross=d(0);self.UnReal_Cross=d(0);self.PositionMargin_Isolated=d(0);self.UnReal_Isolated=d(0);
        self.CalPositionMap={};PositionMap={}
        for symbol in instrumentList:
            BasicDict= {"PositionValue":0,"Equity":0,"MaintMarginRatio":0,"Level":0,"AvailPosition":0,"PositionAmt":0,"MarkPrice":0,"PositionMargin":0};DefaultDic={};
            PositionDic[symbol]={"isolated": {"long": copy.deepcopy(BasicDict), "short": copy.deepcopy(BasicDict)},
             "cross": {"long": copy.deepcopy(BasicDict), "short": copy.deepcopy(BasicDict)}}
            PositionMap[symbol]={'isolated_long': {},'isolated_short':copy.deepcopy(DefaultDic),'cross_long':copy.deepcopy(DefaultDic),'cross_short':copy.deepcopy(DefaultDic)}
        PositionRes = self.NTS.position(log_level=0, tradeType='linearPerpetual')
        if e(PositionRes)[0]:
            if PositionRes['data'].__len__() > 0:
                for i in PositionRes['data']:
                    MarginType=i['marginType'];PositionSide= i['positionSide']
                    Key = i['marginType'] + '_' + i['positionSide'];
                    symbol=i['symbol']
                    positionMargin = 'posMargin' if 'positionMargin' not in i.keys() else 'positionMargin';
                    # MarkPrice = d(19500) if symbol == 'BTCUSDT' else d(1800)
                    TempPositionDict=PositionDic[symbol][MarginType][PositionSide]
                    positionValue = self.MarkPrice[symbol] * d(i['positionAmt']) * d(self.NTS.instrument[symbol[:-4]][1])
                    TempPositionDict['PositionValue']=positionValue
                    if MarginType=='isolated':  TempPositionDict['Equity']=d(i[positionMargin]) + d(i['unrealisedPnl'])
                    if self.NTS.source=='api':
                        TempPositionDict['MaintMarginRatio'] = i['maintMarginRatio']
                        TempPositionDict["Level"] = i['insuranceLevel']
                    TempPositionDict['AvailPosition'] = i['availPos']
                    TempPositionDict["PositionAmt"] = i['positionAmt']
                    TempPositionDict["MarkPrice"] = self.MarkPrice[symbol]
                    TempPositionDict["PositionMargin"] = i[positionMargin]
                    TempPositionDict["AvgOpenPrice"] = i["avgEntryPrice"]

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
        return PositionDic
    def GetBalanceData(self):
        AssetsRes=self.NTS.Assets(currency='USDT');
        if e(AssetsRes)[0]:
            for AssetsDetail in AssetsRes["data"]:
                if AssetsDetail["currency"] == "USDT":
                    self.UnRealized = AssetsDetail["unrealized"]
                    self.FrozenBalance = AssetsDetail["frozenBalance"]
                    self.PositionMargin = AssetsDetail["positionMargin"]
            # BalanceRes=AssetsRes['data'][0]
            # self.Balance_Equity=BalanceRes['marginEquity']
            # self.Balance_Unreal = BalanceRes['profitUnreal'] if self.NTS.source=='API' else  0
            # self.Balance_Frozen = BalanceRes['marginFrozen']
            # self.Balance_MarginPosition=BalanceRes['marginPosition']
            # self.Balance_Available = BalanceRes['marginAvailable']
            # self.Balance_WithDrawAmount= BalanceRes['maxWithdrawAmount']
        else:printc(NTS.source+'资金查询异常',AssetsRes)

if __name__ == '__main__':
    import BUS.API.WebOrder as WebOrder
    import BUS.Futures.basic as basic
    api = WebOrder.WebOrder(3, token=basic.token1)
    A=AOP(api, symbol='BTC',_type=1)
            ##🀆🀆🀆🀆🀆★★★★★Get 基础值★★★★★🀆🀆🀆🀆🀆
    # print('taker,maker费率,面值',A.TakerFeeRate,A.MakerFeeRate,A.CtVal)
            ##🀆🀆🀆🀆🀆★★★★★Get 挂单字典:价值、冻结保证金★★★★★🀆🀆🀆🀆🀆
    # print('OpenOrder',A.OpenOrders)
    # print('FrozenMargin',A.FrozenMargin)
        ##🀆🀆🀆🀆🀆★★★★★Get 持仓字典:★★★★★🀆🀆🀆🀆🀆
                #"PositionValue"持仓价值、"Equity":权益(逐仓可以用)、"MaintMarginRatio":维持保证金率
                #"Level"风险档位、"AvailPosition"可平数量、"PositionAmt":持仓数量、"PositionMargin":持仓保证金
    # print('Positions',A.Positions)
        ##🀆🀆🀆🀆🀆★★★★★Get 资金字典:★★★★★🀆🀆🀆🀆🀆
            # A.Balance_MarginPosition 总持仓保证金 A.Balance_Frozen总冻结资金 A.Balance_Equity 账户权益
            # A.Balance_Unreal未实现盈亏 A.Balance_WithDrawAmount最大划转金额 A.Balance_Available 可用保证金
    print('Account:',A.UnRealized)
