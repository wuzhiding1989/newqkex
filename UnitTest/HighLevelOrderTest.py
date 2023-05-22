from BU.NTS.WebOrder import n_order as WebOrder
import BU.NTS.comm.params as par
from common.util import printc
from UnitTest.com import GetPositionSide,OpenOrdersCheck,HisOrdersCheck,GetOrderPrice,GetFaceSide,GetFeeAndProfit,HisTradeCheck
import copy,random,time
from common.other import httpCheck as e
import BU.NTS.Calculator as Cal

class HighLevelOrderTest:
    def __init__(self,api,Symbol='BTC',server=6,uid=10071):
        global NTS,Ctval,TakerFeeRate,MakerFeeRate,symbol,SYMBOL,OrderParams,NTS_FACE,FaceSide,FacePositionSide,OrderPrice;
        NTS=api;symbol=Symbol;SYMBOL=symbol+'USDT'
        self.InitOrderParams = copy.deepcopy(par.linear_cross_param)
        self.price=random.randint(13000,16000);self.qty=random.randint(2,9);
        BasicOrderParams={"price":self.price,"orderQty":self.qty}
        self.InitOrderParams.update(BasicOrderParams)
        self.TestResult=False;self.Symbol=Symbol
        Instrument=NTS.instrument[Symbol]
        Ctval=Instrument[1];TakerFeeRate=Instrument[2];MakerFeeRate=Instrument[3];
        OrderParams = self.InitOrderParams;
        NTS_FACE = WebOrder(server, user_id=99999);

    def Limit_IOC_Test(self,TestTradeType=None,TimeInForce='gtc',MarginType=None):
        global OrderPrice
        if not MarginType: MarginType='cross'
        ModuleName='Limit'
        OrderParams=self.InitOrderParams;
        OrderParams['timeInForce'] = TimeInForce;
        import UnitTest.AOP as AOP
        P = AOP.AOP(NTS, symbol=SYMBOL, _type=3).Positions[SYMBOL][MarginType][GetPositionSide('buy',True)]

        for Side in ['buy']: # ,'sell'
            OrderPrice = GetOrderPrice(NTS, symbol, Side, IsTrade=False) if not TestTradeType else GetOrderPrice(NTS,symbol,Side,IsTrade=True)
            OrderPrice=random.randint(16000,16400)
            P = AOP.AOP(NTS, symbol=SYMBOL, _type=3).Positions[SYMBOL][MarginType][GetPositionSide(Side, True)]
            # AvgPrice = Cal.CaulatorAvgPrice(P["AvgOpenPrice"], P["PositionAmt"], OrderPrice, 19) #计算成交后的开仓均价

            #部分成交、完全成交 且 IOC时，对手方先下单
            if TestTradeType not in ['UnFilled'] and TimeInForce=='ioc':
                FaceOrderRes = self.MakerOrder(TestTradeType, Side, Face=True,MarginType=MarginType)
                if e(FaceOrderRes)[0]:  print(f'{NTS_FACE.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{FaceSide} {OrderParamsFace["price"]}-{OrderParamsFace["orderQty"]} {FaceOrderRes["data"]["orderId"]}')
                FeeRate = MakerFeeRate if TimeInForce == 'gtc' else TakerFeeRate
                Fee = GetFeeAndProfit(OrderPrice, OrderParamsFace['orderQty'], Ctval, FeeRate)
            # 模拟用户下单
            OrderRes=self.MakerOrder(TestTradeType, Side)
            if e(OrderRes)[0]:
                # 用户下单成功后，打印 用户、场景、方向、价格数量、订单号
                print(f'{NTS.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{Side} {OrderPrice}-{OrderParams["orderQty"]} {OrderRes["data"]["orderId"]}')

            if e(OrderRes)[0]:
                OrderId=OrderRes['data']['orderId']
                if TimeInForce=="ioc" and TestTradeType=="Partitial":
                    if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<部分成交自动撤销>当前委托验证失败{OrderId}')
                    if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='partially_filled_canceled',Fee=Fee[0]): printc(f'<部分成交自动撤销>历史订单验证失败{OrderId}')
                    if not HisTradeCheck(NTS, OrderId, Flag=True, FilledQty=OrderParamsFace['orderQty'], RealProfit='0',TakerFlag=True, Fee=Fee[0]): printc(f'<部分成交自动撤销>历史成交验证失败{OrderId}')
                if TimeInForce == 'ioc' and TestTradeType == 'Filled':
                    if not OpenOrdersCheck(NTS,OrderId, Flag=False): printc(f'<完全成交>当前委托验证失败{OrderId}')
                    if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='filled',Fee=Fee[0]): printc(f'<完全成交>历史订单验证失败{OrderId}')
                    if not HisTradeCheck(NTS, OrderId, Flag=True, FilledQty=OrderParamsFace['orderQty'], RealProfit='0',TakerFlag=True, Fee=Fee[0]): printc(f'<部分成交自动撤销>历史成交验证失败{OrderId}')
                if TimeInForce == 'ioc' and TestTradeType=='UnFilled':
                    if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交自动撤单>当前委托验证失败{OrderId}')
                    if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='canceled'): printc(f'<未成交自动撤单>历史订单验证失败{OrderId}')
            else: printc(e(OrderRes)[1],e(OrderRes)[2])

            #gtc 交易场景  用户先下单对手方再下单   以下内容： 对手方下单
            if TestTradeType and TimeInForce=='gtc':
                FaceOrderRes=self.MakerOrder(TestTradeType,Side,Face=True)
                if e(FaceOrderRes)[0]:  print(f'{NTS_FACE.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{FaceSide} {OrderParamsFace["price"]}-{OrderParamsFace["orderQty"]} {FaceOrderRes["data"]["orderId"]}')
                FeeRate=MakerFeeRate if TimeInForce=='gtc' else TakerFeeRate
                Fee=GetFeeAndProfit(OrderPrice,OrderParamsFace['orderQty'],Ctval,FeeRate)
                if e(FaceOrderRes)[0]:
                    CaseTitle=f'{Side} {TimeInForce}'
                    if TimeInForce=='gtc':
                        if TestTradeType=='Partitial':
                            #部分成交：当前委托存在 状态为、历史订单不存在
                            if not OpenOrdersCheck(NTS, OrderId, Flag=True,Status='partially_filled',Fee=Fee[0]): printc(f'<部分成交>当前委托验证失败{OrderId}')
                            if not HisOrdersCheck(NTS, OrderId, Flag=False): printc(f'<部分成交>历史订单失败{OrderId}')


                    elif TestTradeType=='Filled':
                        # 完全成交：验证1、当前委托不存在；验证2：历史订单存在 状态为filled
                        if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<完全成交>当前委托验证失败{OrderId}')
                        if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='filled',Fee=Fee[0]): printc(f'<完全成交>历史订单失败{OrderId}')
                        if not HisTradeCheck(NTS, OrderId, Flag=True, FilledQty=OrderParamsFace['orderQty'],RealProfit='0',TakerFlag=False,Fee=Fee[0]): printc(f'<完全成交>历史成交失败{OrderId}')
            # else:
            #     printc(f'对手方下单失败:',e(FaceOrderRes)[1], e(FaceOrderRes)[2])


            if TestTradeType=='Partitial':
                # 限价limit订单：部分成交，需要撤单 ，再检查当前委托、历史订单
                if TimeInForce=='gtc': CancelRes=NTS.orderCancel(tradeType=OrderParams["tradeType"], symbol=SYMBOL, orderId=OrderRes['data']['orderId'],log_level=0)
                # 限价IOC订单：部分成交时会自动撤单,，检查当前委托、历史订单
                # if TimeInForce=='ioc' or e(CancelRes)[0]:
                    # if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<部分成交剩余撤单>当前委托验证失败{OrderId}')
                    # if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='partially_filled_canceled',Fee=Fee[0]): printc(f'<部分成交剩余撤单>历史订单验证失败{OrderId}')
                    # if not HisTradeCheck(NTS, OrderId, Flag=True, FilledQty=OrderParamsFace['orderQty'],RealProfit='0',TakerFlag=False,Fee=Fee[0]): printc(f'<部分成交剩余撤单>历史成交验证失败{OrderId}')

                else: printc(f'撤单请求失败')
            self.TestResult=True
    def Limit_FOK_Test(self,TestTradeType=None,TimeInForce='gtc',MarginType=None):
        global OrderPrice
        ModuleName='Limit';OrderParams=self.InitOrderParams;
        symbol='BTC';SYMBOL=symbol+'USDT'
        Instrument=NTS.instrument[symbol]
        Ctval=Instrument[1];TakerFeeRate=Instrument[2];MakerFeeRate=Instrument[3];
        OrderParams['timeInForce'] =TimeInForce;
        for Side in ['buy']: #,'sell'
            OrderParams['side']=Side;
            OrderParams['symbol'] = symbol+'USDT';
            # OrderPrice=GetOrderPrice(NTS, symbol, Side,IsTrade=False) if not TestTradeType else GetOrderPrice(NTS, symbol, Side,IsTrade=True)
            OrderPrice = random.randint(16000, 16400)
            OrderParams['price']=OrderPrice
            OrderParams['positionSide'] = GetPositionSide(Side,IsOpen=True);
        #FOK - 部分成交,全部成交 场景 - 对手方 先挂单
        if TestTradeType in ["Partitial","Filled"] and TimeInForce == 'fok':
            # FaceSide = GetFaceSide(Side);

            # FacePositionSide = GetPositionSide(FaceSide, IsOpen=True);
            # NTS_FACE = WebOrder(6, user_id=10071);
            # OrderParamsFace = copy.deepcopy(OrderParams)
            # OrderParamsFace['side'] = FaceSide[0]
            # OrderParamsFace['positionSide'] = FacePositionSide
            # OrderParamsFace['orderQty'] = self.qty - 1 if TestTradeType in ['Partitial'] else self.qty
            FaceOrderRes = self.MakerOrder(TestTradeType, Side, Face=True, MarginType=MarginType)
            # FaceOrderRes = NTS_FACE.order(caseParam=OrderParamsFace, log_level=0)
            if e(FaceOrderRes)[0]:
                print(f'{NTS_FACE.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{FaceSide} {OrderParamsFace["price"]}-{OrderParamsFace["orderQty"]} {FaceOrderRes["data"]["orderId"]}')
            else:
                printc(f'{NTS_FACE.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{FaceSide[0]} 下单失败')
        # 模拟用户下单，下单数量>对手方 下单数量
        OrderRes = NTS.order(caseParam=OrderParams, log_level=0)
        if e(OrderRes)[0]:
            # 用户下单成功后，打印 用户、场景、方向、价格数量、订单号
            print(f'{NTS.user_id}<{ModuleName}-{TimeInForce}-{TestTradeType}>{Side} {OrderPrice}-{OrderParams["orderQty"]} {OrderRes["data"]["orderId"]}')
        if e(OrderRes)[0]:
            OrderId = OrderRes['data']['orderId']
            if TimeInForce == 'fok' and TestTradeType in ['Partitial',"UnFilled"]:
                # FOK 未全部成交：用户下单成功后，验证当前委托无数据、历史订单状态为全部撤销
                if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未全部成交自动撤销>当前委托验证失败{OrderId}')
                if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='canceled'): printc(f'<未全部成交自动撤销>历史订单验证失败{OrderId}')
                #FOK 未全部成交：撤掉 对手方的挂单
                CancelFaceOrderRes = NTS_FACE.orderCancel(tradeType=OrderParams["tradeType"], symbol=SYMBOL,orderId=FaceOrderRes['data']['orderId'], log_level=0)
                if not e(CancelFaceOrderRes)[0]: printc('<未全部成交自动撤销> 对手方撤单请求失败',CancelFaceOrderRes)
            if TimeInForce == 'fok' and TestTradeType == 'Filled':
                # <<FOK 全部成交>>：先计算成交手续费，默认用taker费率
                # FeeRate = MakerFeeRate if TimeInForce == 'gtc' else TakerFeeRate
                Fee = GetFeeAndProfit(OrderPrice, OrderParamsFace['orderQty'], Ctval, TakerFeeRate)
                # <<FOK 全部成交>>：用户下单成功后，验证当前委托无数据、历史订单状态为全部成交
                if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<FOK完全成交>当前委托验证失败{OrderId}')
                if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='filled',Fee=Fee[0]): printc(f'<FOK完全成交>历史订单验证失败{OrderId}')
                if not HisTradeCheck(NTS, OrderId, Flag=True, FilledQty=OrderParamsFace['orderQty'], RealProfit='0',TakerFlag=True, Fee=Fee[0]): printc(f'<FOK完全成交>历史成交验证失败{OrderId}')
        else:
            printc(e(OrderRes)[1], e(OrderRes)[2])
    def PostOnly_Test(self,TestTradeType=None,PostOnly=True):
        ModuleName = 'Limit'
        OrderParams = self.InitOrderParams;
        symbol = 'BTC';
        SYMBOL = symbol + 'USDT'
        Instrument = NTS.instrument[symbol]
        Ctval = Instrument[1];
        TakerFeeRate = Instrument[2];
        MakerFeeRate = Instrument[3];
        # newPrice(NTS,'BTC',_type=1)
        OrderParams['timeInForce'] = "gtc";OrderParams['postOnly'] = "True";
        for Side in ['buy', 'sell']:  #
            OrderParams['side'] = Side;
            OrderParams['symbol'] = symbol + 'USDT';
            OrderPrice = GetOrderPrice(NTS, symbol, Side, IsTrade=False) if not TestTradeType else GetOrderPrice(NTS,symbol,Side,IsTrade=True)
            OrderParams['price'] = OrderPrice
            OrderParams['positionSide'] = GetPositionSide(Side, IsOpen=True);
        if TestTradeType in ['Partitial']:
            FaceSide = GetFaceSide(Side);
            FacePositionSide = GetPositionSide(FaceSide, IsOpen=True);
            NTS_FACE = WebOrder(6, user_id=10071);
            OrderParamsFace = copy.deepcopy(OrderParams)
            OrderParamsFace['side'] = FaceSide
            OrderParamsFace['positionSide'] = FacePositionSide
            OrderParamsFace['orderQty'] = self.qty - 1 if TestTradeType in ['Partitial'] else self.qty
            FaceOrderRes = NTS_FACE.order(caseParam=OrderParamsFace, log_level=0)
            if e(FaceOrderRes)[0]:
                print(f'{NTS_FACE.user_id}<{ModuleName}-{PostOnly}-{TestTradeType}>{FaceSide} {OrderParamsFace["price"]}-{OrderParamsFace["orderQty"]} {FaceOrderRes["data"]["orderId"]}')
        # 模拟用户下单，下单数量>对手方 下单数量
        OrderRes = NTS.order(caseParam=OrderParams, log_level=0)
        if e(OrderRes)[0]:
            # 用户下单成功后，打印 用户、场景、方向、价格数量、订单号
            print(f'{NTS.user_id}<{ModuleName}-{PostOnly}-{TestTradeType}>{Side} {OrderPrice}-{OrderParams["orderQty"]} {OrderRes["data"]["orderId"]}')
        if e(OrderRes)[0]:
            OrderId = OrderRes['data']['orderId']
            if TestTradeType == 'Partitial':
                # PostOnly 能成交时，则自动撤销
                if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<postOnly成交自动撤销>当前委托验证失败{OrderId}')
                if not HisOrdersCheck(NTS, OrderId, Flag=True, Status='canceled'): printc(f'<postOnly成交自动撤销>历史订单验证失败{OrderId}')
            if TestTradeType == 'UnFilled':
                # PostOnly 不成交时，则继续挂单
                if not OpenOrdersCheck(NTS, OrderId, Flag=True, Status='active'): printc(f'<postOnly未成交>当前委托验证失败{OrderId}')
                if not HisOrdersCheck(NTS, OrderId, Flag=False): printc(f'<postOnly未成交>历史订单验证失败{OrderId}')
                #PostOnly 不成交时 验证完毕后撤单
                CancelFaceOrderRes = NTS.orderCancel(tradeType=OrderParams["tradeType"], symbol=SYMBOL,orderId=OrderRes['data']['orderId'], log_level=0)
                if not e(CancelFaceOrderRes)[0]: printc('<postOnly未成交手动撤销> 对手方撤单请求失败',CancelFaceOrderRes)
    def MakerOrder(self,TestTradeType=None,Side='buy',Face=False,MarginType=None,OpenFlag=True):
        global FaceSide,FacePositionSide,OrderParamsFace,NTS_FACE;

        OrderParams['symbol'] = SYMBOL
        OrderParams['price'] = OrderPrice
        if MarginType=='isolated': OrderParams['marginType']='isolated'
        if Face:
            FaceSide = GetFaceSide(Side)[0];
            FacePositionSide = GetPositionSide(FaceSide, IsOpen=True);  #对手方一直开仓
            # NTS_FACE = WebOrder(6, user_id=10071);
            OrderParamsFace = copy.deepcopy(OrderParams)
            OrderParamsFace['timeInForce'] = "gtc";
            OrderParamsFace['side'] = FaceSide
            OrderParamsFace['positionSide'] = FacePositionSide
            OrderParamsFace['orderQty'] = self.qty - 1 if TestTradeType == 'Partitial' else self.qty
            return NTS_FACE.order(caseParam=OrderParamsFace, log_level=0)
        else:

            OrderParams['positionSide'] = GetPositionSide(Side, IsOpen=OpenFlag);
            OrderParams['side'] = Side;
            return NTS.order(caseParam=OrderParams, log_level=0)


if __name__ == '__main__':
    NTS=WebOrder(5, user_id='97121927')
    from BU.NTS.WebOrder import n_order as WebOrder
    # BatchOrderParam=CreateOrders(NTS,marginType="cross",symbol=["BTC","ETH"],number=5,TradeFlag=False,MarketType=False,OpenFlag=True)   #批量下单 参数 组装测试
    # OrderParam= CreateOrders(NTS, marginType="cross", symbol="BTC", MarketType=False,OpenFlag=False)  # 组装 下单参数 - 挂单
    # OrderParam = CreateOrders(NTS, marginTypeList="cross", symbol="BTC", MarketType=False,OpenFlag=False,TradeFlag=True)  # 组装 下单参数 - 成交
    # a= CreateOrders(NTS, marginTypeList=['cross','isolated'],symbol="BTC",MarketType=False,OpenFlag=True)  # 组装批量下单参数
    # print("批量下单参数: ",json.dumps(BatchOrderParam))
    # print("<全仓>单笔下单参数: ",OrderParam)
    # CreateOrders(NTS,Number=3,Price=[13000,14000]) #组装批量下单参数
    order=HighLevelOrderTest(NTS,server=5)
    IocFlag=0;FokFlag=1;
    if IocFlag:
        # order.Limit_IOC_Test(TestTradeType='Partitial') #GTC限价 部分成交场景
        order.Limit_IOC_Test(TestTradeType='Partitial',TimeInForce="ioc")  #Limit-IOC
        order.Limit_IOC_Test(TestTradeType='UnFilled', TimeInForce="ioc")  # Limit-IOC
        order.Limit_IOC_Test(TestTradeType='Filled', TimeInForce="ioc")  # Limit-IOC
    if FokFlag:
        order.Limit_FOK_Test(TestTradeType='Filled', TimeInForce="fok")
        # order.Limit_FOK_Test(TestTradeType='Partitial', TimeInForce="fok")
        # order.Limit_FOK_Test(TestTradeType='UnFilled', TimeInForce="fok")

