from UnitTest.com import CreateOrders
from BU.NTS.WebOrder import n_order as WebOrder

NTS = WebOrder(5, user_id='10071')


# 双向全仓下单组装参数:
print("BTC全仓做多限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True))
print("BTC全仓做多对手方限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True, faceFlag=True))
print("BTC全仓做空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="cross", symbol="BTC", TradeFlag=True,MarketFlag=True, OpenFlag=True))
print("BTC全仓平多限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=False))
print("BTC全仓平空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="cross", symbol="BTC", TradeFlag=True,MarketFlag=True, OpenFlag=False))

print("ETH逐仓做多限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="isolated", symbol="ETH", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True))
print("ETH逐仓做空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="isolated", symbol="ETH", TradeFlag=True,MarketFlag=True, OpenFlag=True))
print("ETH逐仓平多限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="isolated", symbol="ETH", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=False))
print("ETH逐仓平空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="isolated", symbol="ETH", TradeFlag=True,MarketFlag=True, OpenFlag=False))

print("BTC全仓批量做多限价挂单参数->", CreateOrders(NTS, Side='buy', marginType="cross", symbol=["BTC"], price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True, number=5))
print("BTC全仓批量做空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="cross", symbol=["BTC"], TradeFlag=True,MarketFlag=True, OpenFlag=True, number=5))
print("BTC\ETH逐仓批量做空限价挂单参数->", CreateOrders(NTS, Side='sell', marginType="isolated", symbol=["BTC","ETH"], price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True, number=5))
print("BTC\ETH逐仓批量做空市价成交参数->", CreateOrders(NTS, Side='sell', marginType="isolated", symbol=["BTC","ETH"], TradeFlag=True,MarketFlag=True, OpenFlag=True, number=19))
print("BTC全仓+逐仓批量做多挂单参数->", CreateOrders(NTS, Side='sell', marginType="isolated", symbol=["BTC","ETH"], TradeFlag=True,MarketFlag=True, OpenFlag=True, Cro_Iso=True, number=3))

# 计划委托
TriggerParam = CreateOrders(NTS, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True)
TriggerParam.update({'orderType':'TriggerLimit','triggerPxType':'last','ordPx': 30000})
print("BTC全仓做多计划委托限价挂单参数->",TriggerParam)

# 单向持仓组装参数:
print("BTC全仓做多限价挂单参数->", CreateOrders(NTS, Side='buy', PositionSide='both', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True))
print("BTC全仓批量做多限价挂单参数->", CreateOrders(NTS, Side='buy', PositionSide='both', marginType="cross", symbol=["BTC"], price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True, number=5))
