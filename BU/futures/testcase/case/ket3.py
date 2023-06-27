from BU.futures.api import webapi as wb
import random,time,requests,re
symbol = 'ETHUSDT';tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
us=7
user=wb.webapi(us,'test')

def sidess2():
    try:
        pores = user.web_position(tradeType=tradeType, symbol=symbol, marginType=marginType)
        availPos = pores['data'][0]['availPos'];availPos1 = pores['data'][1]['availPos']
        print('当前多空可平量分别是',availPos,availPos1)
        pri = getSpotList(symbol)
        sides = [('buy', 'short'), ('sell', 'long')]
        random.shuffle(sides)
        for side, position_side in sides:
            order_response = user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=position_side,
                                            orderType=orderType, reduceOnly=reduceOnly,
                                            marginType=marginType, price=pri, priceType=priceType, orderQty=min(availPos,availPos1),
                                            postOnly=postOnly, timeInForce=timeInForce)
            print(order_response)
    except Exception as e:
        print('Error getting availPos:', e)


def getSpotList(symbol):
    match = re.match(r'([A-Za-z]+)USDT', symbol)
    if match:
        name = match.group(1).lower() + '_usdt'
    else:
        print('Invalid symbol')
    # 请求参数
    data = {
        'device_id': 'e03ff510-06b1-11ee-9950-db5348877881',
        'token': '',
        'lang': 'zh_CN',
        'app_id': 'an38PVWu2b6UgiRa94c68Cmy',
        '__platform': 3,
        'nonce': 307164,
        '_CDCODE': '8ea89804b788344153b54f4a6caaeae2'
    }
    url = 'https://app.ueex.com/MarketV2/getSpotList'
    response = requests.post(url, data=data).json()
    se=response['data']
    for tmp in response['data']:
        if tmp['name']==name:
            tmp=tmp['last']
            return tmp
if __name__ == '__main__':
    # for i in range(2):
    #     a=getSpotList('ETHUSDT')
    #     print(a)
    #     time.sleep(2)
    for i in range(1000):
        print(sidess2())
        time.sleep(60)