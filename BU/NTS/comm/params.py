import copy

import param.dict as dict
from param.dict import cumQty,avgPrice,lastPrice,leavesQty,commission,orderStatus,base,quote

ExceptionParam=[['1e+3',0,'传科学计数法'],['1e+30',0,'传科学计数法2'],]

#下单参数
orderParams={
    'tradeType':'linearPerpetual',
    'symbol':'BTCUSDT',
    'marginType' :'cross',
    'orderType':'limit',
    'price':'18700',
    'orderQty':'2',
    'side':'buy',
    'positionSide':'LONG',
    'postOnly':False,
    'timeInForce':'GTC',
    'priceType':'marketPrice',
    'clOrdId':''
}

#查看当前委托参数
openOrdersParams={
    'tradeType':'linearPerpetual',
    'symbol':'BTCUSDT',
    'side':'',
    'orderId':'',
    'clOrdId':'',
    'pageNum':1,
    'pageSize':10

}
#撤单参数
cancelOrderParams={
    'tradeType':'linearPerpetual',
    'symbol':'BTCUSDT',
    'orderId':'',
    'clOrdId':''

}

#查看仓位参数
positionParams={
    'tradeType':'linearPerpetual',
    'symbol':'BTCUSDT',
    'positionSide':'long',
    'marginType':'cross'

}
linear_cross_param={'tradeType': dict.linear_tradeType, 'marginType' : 'cross', 'orderType': 'limit', 'postOnly':False, 'timeInForce': 'GTC', 'priceType':None, 'clOrdId': ''}
linear_isolated_param=copy.deepcopy(linear_cross_param);linear_isolated_param['marginType']='isolated'

OpenOrderAssert = {cumQty:'0',avgPrice:'',lastPrice:'',leavesQty:'',commission:'',orderStatus:'active',base:'', quote:'USDT'}
HisTradeAssert={'taker':False,'createTime':(int,'len',13),'updateTime':(int,'len',13),'commissionAsset':'USDT'}
HisAccountAssert={'tradeType': dict.linear_tradeType, 'income': '', 'details':None, 'currency': 'USDT', 'createTime': (int, 'len', 13)}

SideList=['buy','sell']
PositionSideList=['long','short']

