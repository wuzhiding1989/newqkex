import  requests,time
from decimal import Decimal

tradeTyp='linearPerpetual'
url="https://test-futures-rest.qkex.com"
headers = {"Content-Type":"application/json","source":"api"}

def admin_symbol_upsert(base): #修改交易对配置
    params={
        "tradeType": 81,
        "sequence": "1",
        "quoteCurrency": "USDT",
        "baseCurrency": base,
        "basePrecision": "4",
        "quotePrecision": "4",
        "tickSize": "0.001",
        "frontLeverages": "1,25,50,75",
        "leverage": "5",
        "ctVal": "0.001",
        "subject": f"{base}USDT",
        "matchGroup": "OTHER_GROUP"
    }###OTHER_GROUP---f"{base}_GROUP"
    path="/v1/admin/manager/symbol/upsert"
    res = requests.post(url=url+path,json=params,headers=headers).json()
    print(res)

def admin_query_order(uid=None,tradeTyp=None,symbol=None):#查询uid下的当前委托订单
    path=f'/v1/admin/memory/query/order?conditionUid={uid}&currency=USDT&tradeType={tradeTyp}&symbol={symbol}'
    res = requests.get(url=url+path,headers=headers).json()
    return res
def admin_symbol_conf_upsert(symbolId):#btc:81000201 eth:81000301  FIL 81000401  修改交易对配置
    path="/v1/admin/manager/symbol/conf/upsert"
    params={
      "symbolId": "81000301",
      "orderMaxVolume": "10000",
      "orderMinVolume": "1",
      "orderPriceCeiling": "0.1",
      "orderPriceFloor": "3.22",
      "orderCount": "50",
      "strategyOrderCount": "100",
      "frontPrecisions": "10,1,0.1,0.01,0.001",
      "optimumLevel": "5",
      "maxNumAlgoOrders": "5000",
      "maxNumOrders": "500",
      "optimumRate": "0.003",
      "orderValueLimit": "50000",
      "indexPriceGreaterRatio": "0.05",
      "markPriceGreaterRatio": "0.05",
      "indexPriceLessRatio": "0.05",
      "markPriceLessRatio": "0.05",
      "fixedVal": 0,
      "quoteCurrencyRate": "0.002",
      "baseCurrencyRate": "0.002",
      "maxCapitalRate": "0.05",
      "minCapitalRate": "0.001",
      "makerFeeRate": "0.0002",
      "takerFeeRate": "0.0002",
      "deliveryFeeRate": "0.0002"
}
    res = requests.post(url=url+path,json=params,headers=headers).json()
    print(url+path)
    print(params)
    print(res)

def admin_memory_query_position(uid=None,tradeTyp=None,symbol=None):#查询uid下的当前委托订单
    path=f'/v1/admin/memory/query/position?conditionUid={uid}&currency=USDT&tradeType={tradeTyp}&symbol={symbol}'
    res = requests.get(url=url+path,headers=headers).json()
    print(res)#availPos返回为空

def admin_bigdata_reconciliation_amend(id):
    path=f'/v1/admin/bigdata/reconciliation/amend/check/{id}'
    res = requests.post(url=url+path,headers=headers).json()
    print(url+path)
    print(res)
if __name__ == '__main__':
    #print(admin_symbol_conf_upsert('81000301'))
    # a=admin_query_order(uid=10122333,tradeTyp=tradeTyp,symbol='ETHUSDT')
    # print(a)
    #print(admin_memory_query_position(tradeTyp=tradeTyp,uid='10122688',symbol='LINKUSDT'))
    #print(admin_bigdata_reconciliation_amend(30004))
    id1 = [Decimal('997.720194440000000000'), Decimal('997.720194440000000000'), Decimal('997.720194440000000000')]
    id2 = [Decimal('0E-18'), Decimal('0E-18'), Decimal('-0.000119620000000000'), Decimal('0.000143550000000000')]

    for i in range(len(id1) - 1):
        if id1[i] - id2[i] == id1[i + 1]:
            print("数据当前的ID：", i + 1)
            print("id1[{}]-id2[{}] 不等于 id1[{}]: ".format(i, i, i + 1))
            print("id1[{}]-id2[{}] = {}".format(i, i, id1[i] - id2[i]))
            print("id1[{}] = {}".format(i + 1, id1[i + 1]))