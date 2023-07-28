from BU.futures.api import webapi as wb
import random,time, threading,requests,multiprocessing
from functools import partial
from  BU.futures.testcase.case import ket3
symbol =ket3.symbol;tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long';name='eth_usdt'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(ket3.us,'test')


def sides(number, min1, max1, accmax, accmin, symbol, time1):
    # 定义买卖方向及其他参数
    try:
        sides = ['buy', 'sell']
        pri = ket3.getSpotList(symbol, ne=3)  # 获取当前价格
        pri = float(pri)

        # 计算价格区间
        def get_price_range(tmp):
            if tmp == 'buy':
                positionSide = 'long'
                pri1 = max(pri - max1, 0)
                pri2 = pri - min1
            else:
                positionSide = 'short'
                pri1 = pri + min1
                pri2 = pri + max1
            return positionSide, round(random.uniform(pri1, pri2), 3)

        # 下单
        retries = 0
        max_retries = 3
        while retries < max_retries:
            try:
                for i in range(number):
                    tmp = random.choice(sides)
                    positionSide, price = get_price_range(tmp)
                    d = round(random.uniform(accmin, accmax))
                    se = user.web_order(tradeType=tradeType, symbol=symbol, side=tmp, positionSide=positionSide,
                                        orderType=orderType,
                                        reduceOnly=reduceOnly,
                                        marginType=marginType, price=price, priceType=priceType, orderQty=d,
                                        postOnly=postOnly,
                                        timeInForce=timeInForce)  # 下单
                    print(se['msg'], price, d, tmp, positionSide)
                    time.sleep(time1)

                break  # 请求成功，跳出循环

            except Exception as e:
                print('Error getting availPos:', e)
                retries += 1
                if retries >= max_retries:
                    print('Max retries exceeded')
                else:
                    print('Retrying...')
                    time.sleep(1)  # 重试前等待1秒

    except Exception as e:
        print('Error getting availPos:', e)


def tipicer():
    a=user.tickpre()
    cc=a['data'][1][3]
    return cc

if __name__ == '__main__':
   a=user.web_tradingAccount();
   c=user.web_uid()
   print('当前账号的uid',c['data']['userId'])
   if not a['data'] or (a['data'][0]['marginAvailable']) !='null' or float(a['data'][0]['marginAvailable']) < 2000:
       #print('请求数据为空')
       print(user.web_transfer(currency="USDT", amount="100000", fromAccountType="funding", toAccountType="futures"))
       #print(result)
   else:
       print('当前账号的可用资产为', a['data'][0]['marginAvailable'])
   for i in range(10000):
        sides(symbol=symbol,number=100,min1=0.07,max1=0.2,accmax=100,accmin=200,time1=0.5)
        #time.sleep(5)

