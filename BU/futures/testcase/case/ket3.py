from BU.futures.api import webapi as wb
import random,time,requests,re
symbol = 'LINKUSDT';tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
us=8
user=wb.webapi(us,'test')

def sidess2(num,time1):
    try:
        for i in range(num):
            pores = user.web_position(tradeType=tradeType, symbol=symbol, marginType=marginType)
            availPos = pores['data'][0]['availPos'];availPos1 = pores['data'][1]['availPos']
            print('当前多空可平量分别是',availPos,availPos1)
            pri = getSpotList(symbol,ne=3)
            sides = [('buy', 'short'), ('sell', 'long')]
            random.shuffle(sides)
            for side, position_side in sides:
                ac =min(min(int(availPos),int(availPos1),3000),3000)
                order_response = user.web_order(tradeType=tradeType, symbol=symbol, side=side, positionSide=position_side,
                                                orderType=orderType, reduceOnly=reduceOnly,
                                                marginType=marginType, price=pri, priceType=priceType, orderQty=ac,
                                                postOnly=postOnly, timeInForce=timeInForce)
                print(ac,order_response)
                time.sleep(time1)
        #print(user.web_oneClickClose(tradeType=tradeType))
    except Exception as e:
        print('Error :', e)


def tick(symbol):
    res=user.web_instruments(tradeType=tradeType,symbol=symbol)
    for tmp in res['data']:
        if tmp['symbol']==symbol:
            tmp1=tmp['tickSize']
            decimal_part = str(tmp1).split('.')[1]
            num_decimal_places = len(decimal_part) if tmp1 % 1 != 0 else 0
            return num_decimal_places


def getSpotList1(symbol):
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

def getSpotList(symbol, ne=None):
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
    response = requests.post(url, data=data,timeout=10).json()
    se = response['data']
    for tmp_obj in response['data']:
        if tmp_obj['name'] == name:
            price = float(tmp_obj['last'])
            rounded_price = round(price, ne)
            return rounded_price

if __name__ == '__main__':
    # for i in range(2):
    #     a=getSpotList(symbol='ETHUSDT',ne=1)
    #     print(a)
    #     time.sleep(2)
    #print(getSpotList(symbol='BNBUSDT',ne=2))
    for i in range(10000):
            print(sidess2(num=100,time1=10))

