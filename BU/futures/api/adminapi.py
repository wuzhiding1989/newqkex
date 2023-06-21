import  requests,time
url="https://test-futures-rest.qkex.com"
headers = {"Content-Type":"application/json","source":"api"}

def symbol_upsert(base):
    params={
        "tradeType": 81,
        "sequence": "1",
        "quoteCurrency": "USDT",
        "baseCurrency": base,
        "basePrecision": "4",
        "quotePrecision": "4",
        "tickSize": "0.001",
        "frontLeverages": "1,25,50,100",
        "leverage": "5",
        "ctVal": "0.001",
        "subject": f"{base}USDT",
        "matchGroup": f"{base}_GROUP"
    }
    path="/v1/admin/manager/symbol/upsert"
    res = requests.post(url=url+path,json=params,headers=headers).json()
    print(res)
def symbol_conf_upsert(symbolId):#btc:81000201 eth:81000301
    path="/v1/admin/manager/symbol/conf/upsert"
    params={
    "symbolId": symbolId,
    "orderMaxVolume": "10000",
    "orderMinVolume": "1",
    "orderPriceCeiling": "0.1",
    "orderPriceFloor": "3.22",
    "orderCount": "50",
    "strategyOrderCount": "100",
    "frontPrecisions": "10,1,0.1,0.01",
    "optimumLevel": "5",
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
    "makerFeeRate": "0.0005",
    "takerFeeRate": "0.001",
    "deliveryFeeRate": "0.0002"
}
    res = requests.post(url=url+path,json=params,headers=headers).json()
    print(res)

if __name__ == '__main__':
    print(symbol_conf_upsert('81000301'))
    #print(symbol_upsert(base='ETH'))
