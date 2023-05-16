import copy

#--备用字段 ,"timeInForce":"GTC","reduceOnly":"false","priceType":"marketPrice","postOnly":"false"
linear_cross_param = {"tradeType":'linearPerpetual',"symbol":'BTCUSDT',"side":"buy","positionSide":"long","orderType":"limit","marginType":"cross","price":'222',"orderQty":"3","clOrdId":""}
linear_isolated_param = copy.deepcopy(linear_cross_param);linear_isolated_param['marginType'] = 'isolated'