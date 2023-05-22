import UnitTest.HighLevelOrderTest as H
from UnitTest.com import OpenOrdersCheck,HisOrdersCheck,GetOrderPrice, CaseLongTitle
from BU.NTS.WebOrder import n_order as WebOrder
from UnitTest.com import GetBusinessName,CreateOrders
import BU.NTS.dataCheck.check as Check
from common.util import Count,printc
from common.other import httpCheck as e
# Side='buy';
TestTradeType=None


PriceList=[(0,1,'Price传0'),('-1',1,'传负数'),(None,1,'不传'),(13000,1,'传正常价格')]
TimeInForceList=[('GTC',1,'传GTC'),('IOC',1,'传IOC'),('FOK',1,'传FOK'),('AAA',1,'传不存在的timeInForce')]


CaseNumber=0
class MaketOrder:
    def __init__(self,server,user_Id):
        global NTS,OrderPrice,OrderParams,Module
        NTS = WebOrder(server, user_id=user_Id)
        Order=H.HighLevelOrderTest(NTS,server=server,uid=user_Id)
        Module="市价委托"

        OrderPrice = GetOrderPrice(NTS, Order.Symbol, Side="buy", IsTrade=False) if not TestTradeType else GetOrderPrice(NTS,Order.Symbol,"buy",IsTrade=True)

    def MarketOrder_Price(self,CaseLevel,Side="buy",MarginTypeList=None,log_level=None,OpenFlag=True):
        global CaseNumber;
        if CaseLevel==1:
            for MarginType in MarginTypeList:
                Business = GetBusinessName(MarginType=MarginType)
                for Price in PriceList:
                    CaseNumber+=1;
                    OrderParam = CreateOrders(NTS, Side=Side, marginType=MarginType, symbol="BTC", price=Price[0],MarketFlag=True,OpenFlag=OpenFlag)
                    CaseTitle=NTS.source+Business +CaseLongTitle(OrderParam)+ Module+Price[2]
                    if PriceList.index(Price) <20:
                        Resp=NTS.order(caseParam=OrderParam,log_level=0)
                        Check.Case_result_count(NTS, Resp, param=Price, moduleName=NTS.source + Module,casetitle=NTS.source+Business +CaseLongTitle(OrderParam)+ Module, log_level=log_level, _type=2)
                        if e(Resp)[0]:
                            OrderId = Resp['data']['orderId']
                            if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交>当前委托验证失败{OrderId}');
                            if not HisOrdersCheck(NTS, OrderId,Status='canceled', Flag=True,OrderParam=OrderParam): printc(f'<未成交>历史订单验证失败{OrderId}')
                            # NTS.orderCancel(tradeType=OrderParam["tradeType"],symbol=OrderParam["symbol"], orderId=OrderId,log_level=3)
                        else: printc(f'{CaseTitle}验证失败 {Resp}');Count(Module,1,0,1,0)
    def MarketOrder_TimeInForceList(self,CaseLevel,MarginTypeList=None,log_level=None,Side="buy",OpenFlag=True):
        global CaseNumber;Counter=0;ErrorCode="1058"
        if CaseLevel == 1: TimeInForceList = [('IOC', 1, '传IOC')]
        if CaseLevel == 2: TimeInForceList=[('GTC', ErrorCode, '传GTC'),('FOK', ErrorCode, '传FOK'),('AAA', "1046", '传不存在的timeInForce')]
        for MarginType in MarginTypeList:
            Counter += 1;
            Business = GetBusinessName(MarginType=MarginType)
            if (Counter == 1 and CaseLevel == 2) or CaseLevel == 1:
                for TimeInForce in TimeInForceList:
                    CaseNumber+=1;
                    OrderParams['marginType'] = MarginType
                    # OrderParams['timeInForce']=TimeInForce[0]
                    OrderParam = CreateOrders(NTS, Side=Side, marginType=MarginType, symbol="BTC",MarketFlag=True,OpenFlag=OpenFlag)
                    OrderParam["timeInForce"]=TimeInForce[0]
                    # print(f'{Module}市价委托 Price{Price[2]}',OrderParam)
                    if TimeInForceList.index(TimeInForce) < 10:
                        Resp = NTS.order(caseParam=OrderParam, log_level=0)
                        Check.Case_result_count(NTS, Resp, param=TimeInForce, moduleName=NTS.source + Module,casetitle=NTS.source + Business + CaseLongTitle(OrderParam) + Module,log_level=log_level, _type=2)
                        if e(Resp)[0]:
                            OrderId = Resp['data']['orderId']
                            if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交>当前委托验证失败{OrderId}')
                            if not HisOrdersCheck(NTS, OrderId,Status='canceled', Flag=True,OrderParam=OrderParam): printc(f'<未成交>历史订单验证失败{OrderId}')
                            # NTS.orderCancel(tradeType=OrderParam["tradeType"], symbol=OrderParam["symbol"], orderId=OrderId,log_level=3)
                        elif CaseLevel == 1:
                            printc(Resp)
    def MarketOrder_PriceType(self,CaseLevel,MarginTypeList=None,log_level=None,Side="buy"):
        global CaseNumber;Counter=0
        for MarginType in MarginTypeList:
            Counter+=1;
            if (Counter==1 and CaseLevel==2) or CaseLevel==1:
                Business = GetBusinessName(MarginType=MarginType)
                OrderParam = CreateOrders(NTS, Side=Side, marginType=MarginType, symbol="BTC", MarketFlag=True)
                if CaseLevel == 1:PriceTypeList = [('marketPrice', 1, '传市价'), ('optimalFive', 1, '传最优5档')];CaseTitle = NTS.source + Business + CaseLongTitle(OrderParam) + Module;
                if CaseLevel == 2:PriceTypeList = [('0', "1046", 'priceType传0'), ('optimalTen', "1046", 'priceType传最优10档')];Business ="<异常>";CaseTitle=NTS.source+Business+Module;
                for PriceType in PriceTypeList:
                    if PriceTypeList.index(PriceType) < 10:
                        OrderParam["priceType"]=PriceType[0]
                        Resp = NTS.order(caseParam=OrderParam, log_level=1)
                        if CaseLevel == 2: Check.Case_result_count(NTS, Resp, param=PriceType, moduleName=NTS.source + Module,casetitle=CaseTitle,log_level=log_level, _type=2)
                        if e(Resp)[0]:
                            OrderId = Resp['data']['orderId']
                            if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交>当前委托验证失败{OrderId}')
                            if not HisOrdersCheck(NTS, OrderId, Status='canceled', Flag=True, OrderParam=OrderParam): printc(f'<未成交>历史订单验证失败{OrderId}')
                            # NTS.orderCancel(tradeType=OrderParam["tradeType"], symbol=OrderParam["symbol"], orderId=OrderId, log_level=3)
                        elif CaseLevel==1:
                            printc(Resp)
    def MarketOrder_PostOnly(self,CaseLevel,MarginTypeList=None,log_level=None):
          global CaseNumber

          for MarginType in MarginTypeList:
              Business = GetBusinessName(MarginType=MarginType)
              if CaseLevel == 1: PostOnlyList = [(True, 1, 'postOnly传True')]
              if CaseLevel == 2: PostOnlyList = [('-1', "1046", 'postOnly传负数')];Business = Business + "<异常>";
              OrderParam = CreateOrders(NTS, Side=Side, marginType=MarginType, symbol="BTC", MarketFlag=True)
              for PostOnly in PostOnlyList:
                  if PostOnlyList.index(PostOnly) < 10:
                      OrderParam["postOnly"] = PostOnly[0]
                      Resp = NTS.order(caseParam=OrderParam, log_level=0)
                      if CaseLevel==2:  Check.Case_result_count(NTS, Resp, param=PostOnly, moduleName=NTS.source + Module,casetitle=NTS.source + Business + CaseLongTitle(OrderParam) + Module,log_level=log_level, _type=2)
                      if e(Resp)[0] and CaseLevel == 1:
                          OrderId = Resp['data']['orderId']
                          if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交>当前委托验证失败{OrderId}')
                          if not HisOrdersCheck(NTS, OrderId, Status='canceled', Flag=True,OrderParam=OrderParam): printc(f'<未成交>历史订单验证失败{OrderId}')
                          # NTS.orderCancel(tradeType=OrderParam["tradeType"], symbol=OrderParam["symbol"], orderId=OrderId, log_level=3)
                      # else:
                      #     printc(Resp)
if __name__ == '__main__':
    M=MaketOrder('5','99999')
    # M.MarketOrder_Price(MarginTypeList=['cross','isolated'],CaseLevel=1,log_level=2,Side="sell",OpenFlag=False) #
    # M.MarketOrder_Price(MarginTypeList=['cross', 'isolated'], CaseLevel=1, log_level=2, Side="sell", OpenFlag=True)

    # M.MarketOrder_Price(MarginTypeList=['cross', 'isolated'], CaseLevel=1, log_level=2, Side="buy", OpenFlag=False)  #
    # M.MarketOrder_Price(MarginTypeList=['cross', 'isolated'], CaseLevel=1, log_level=2, Side="buy", OpenFlag=True)

    # M.MarketOrder_TimeInForceList(MarginTypeList=['cross','isolated'],CaseLevel=1,log_level=2,Side="sell", OpenFlag=False)
    # M.MarketOrder_TimeInForceList(MarginTypeList=['cross', 'isolated'], CaseLevel=1, log_level=2, Side="sell",OpenFlag=True)
    # M.MarketOrder_TimeInForceList(MarginTypeList=['cross'],CaseLevel=2)
    M.MarketOrder_PriceType(MarginTypeList=['cross',"isolated"],CaseLevel=1,log_level=2)
    # M.MarketOrder_PriceType(MarginTypeList=['cross'],CaseLevel=2,log_level=2)
    # M.MarketOrder_PostOnly(MarginTypeList=['cross','isolated'],CaseLevel=1,log_level=2) #
    # M.MarketOrder_PostOnly(MarginTypeList=['cross'],CaseLevel=2,log_level=2)
    print(f'CaseNumber:{CaseNumber}')
    Count(summary=2)