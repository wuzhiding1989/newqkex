import time,random
import UnitTest.HighLevelOrderTest as H
from UnitTest.com import GetPositionSide,OpenOrdersCheck,HisOrdersCheck,GetOrderPrice,GetFaceSide,GetFeeAndProfit,HisTradeCheck,CaseLongTitle
from UnitTest.com import OpenOrdersCheck,HisOrdersCheck,GetOrderPrice
from BU.NTS.WebOrder import n_order as WebOrder
from UnitTest.com import GetBusinessName,CreateOrders
from common.util import Count,printc
from common.other import httpCheck as e

NTS=WebOrder(5, user_id='99999')
Side='buy';TestTradeType=None
Order=H.HighLevelOrderTest(NTS,server=5,uid='99999')
OrderPrice = GetOrderPrice(NTS, Order.Symbol, Side, IsTrade=False) if not TestTradeType else GetOrderPrice(NTS, Order.Symbol, Side,IsTrade=True)
# print(OrderPrice)
OrderParam=H.OrderParams
OrderParam['orderType']='market';OrderParam.pop('timeInForce')

CaseNumber=0
PriceList=[(0,1,'传0'),('-1',1,'传负数'),(None,1,'不传'),(13000,1,'传正常价格')]
class LimitOrder:
    def __init__(self,server,user_Id):
        global NTS,OrderPrice,OrderParams,Module
        NTS = WebOrder(server, user_id=user_Id)
        Order=H.HighLevelOrderTest(NTS,server=server,uid=user_Id)
        Module="限价高级委托"
        OrderPrice = GetOrderPrice(NTS, Order.Symbol, Side="buy", IsTrade=False) if not TestTradeType else GetOrderPrice(NTS,Order.Symbol,"buy",IsTrade=True)
        OrderPrice=random.randint(13000,13300)
    def LimitOrder_TimeInForce(self,CaseLevel,MarginTypeList=None,OpenFlag=True,Side="buy",log_level=None):
        global CaseNumber
        if CaseLevel==1:
            TimeInForceList = [('GTC', 1, 'timeInForce传GTC'), ('IOC', 1, 'timeInForce传IOC'), ('FOK', 1, 'timeInForce传FOK')]#
        if CaseLevel==2:
            TimeInForceList = [('AAA', 1, '传不存在的timeInForce')]
        for MarginType in MarginTypeList:
            Business = GetBusinessName(MarginType=MarginType)
            OrderParam = CreateOrders(NTS, Side=Side, marginType=MarginType,price=OrderPrice, symbol="BTC", MarketFlag=False,OpenFlag=OpenFlag)

            for TimeInForce in TimeInForceList:
                CaseNumber += 1;
                OrderParam['timeInForce'] = TimeInForce[0]
                CaseTitle = NTS.source + Business + CaseLongTitle(OrderParam) + Module
                Resp = NTS.order(caseParam=OrderParam, log_level=0)
                Check.Case_result_count(NTS, Resp, param=TimeInForce, moduleName=NTS.source + Module,casetitle=CaseTitle,log_level=log_level, _type=2)

                if e(Resp)[0]:
                    OrderId = Resp['data']['orderId']
                    if TimeInForceList.index(TimeInForce) not in [0]:
                        if not OpenOrdersCheck(NTS, OrderId, Flag=False): printc(f'<未成交>当前委托验证失败{OrderId}');
                        if not HisOrdersCheck(NTS, OrderId, Status='canceled', Flag=True, OrderParam=OrderParam): printc(f'<未成交>历史订单验证失败{OrderId}')
                    else:
                        if not OpenOrdersCheck(NTS, OrderId, Flag=True): printc(f'<未成交>当前委托验证失败{OrderId}');
                        if not HisOrdersCheck(NTS, OrderId,Flag=False): printc(f'<未成交>历史订单验证失败{OrderId}')
                        NTS.orderCancel(tradeType=OrderParam["tradeType"],symbol=OrderParam["symbol"], orderId=OrderId,log_level=0)
                else:
                    printc(f'{CaseTitle}验证失败 {Resp}');Count(Module, 1, 0, 1, 0)

def LimitOrder_PostOnly(CaseLevel,MarginTypeList=None):
    global CaseNumber
    if CaseLevel==1:
        PostOnlyList = [(True, 1, '传True')]
    if CaseLevel==2:
        PostOnlyList = [('567', 1, '传不存在的PostOnly'),('onlyMaker', 1, '传字符onlyMaker')]
    for MarginType in MarginTypeList:
        Module = GetBusinessName(MarginType=MarginType)
        for PostOnly in PostOnlyList:
            CaseNumber += 1;
            OrderParams['postOnly'] = PostOnly[0]
            print(f'{Module}限价委托 postOnly{PostOnly[2]}', OrderParams)
def LimitOrder_PriceType(CaseLevel,MarginTypeList=None):
    global CaseNumber
    if CaseLevel==1:
        PriceTypeList = [('marketPrice', 1, '传市价 无效果'),('optimalFive', 1, '传最优5档 无效果'),('optimalTen', 1, '传最优10档 无效果')]
    for MarginType in MarginTypeList:
        Module = GetBusinessName(MarginType=MarginType)
        for PriceType in PriceTypeList:
            CaseNumber += 1;
            OrderParams['priceType'] = PriceType[0]
            print(f'{Module}限价委托 priceType{PriceType[2]}', OrderParams)
if __name__ == '__main__':
    M=LimitOrder("5",97121927)
    M.LimitOrder_TimeInForce(CaseLevel=1,MarginTypeList=['cross'],log_level=2) #'isolated'
    # LimitOrder_TimeInForce(CaseLevel=2,MarginTypeList=['cross'])
    # LimitOrder_PostOnly(CaseLevel=1,MarginTypeList=['isolated','cross'])
    # LimitOrder_PostOnly(CaseLevel=2,MarginTypeList=['cross'])
    # LimitOrder_PriceType(CaseLevel=1,MarginTypeList=['isolated','cross'])
    # print(CaseNumber)