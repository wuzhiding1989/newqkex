from BU.futures.api import webapi as wb
import random,time,datetime
import concurrent.futures
from BU.futures.testcase.case import ket3
tradeType = 'linearPerpetual';side ='buy';marginType = 'cross';positionSide = 'long';name='eth_usdt'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount='40';pairCode='P_R_USDT_USD';gear='depth-3';limit=1000;period='1m'##short，long
user=wb.webapi(ket3.us,'test')
symbol =ket3.symbol
data_list = []
def place_order(side, position_side, **kwargs):
    try:
        order = user.web_order(orderType=orderType, reduceOnly=reduceOnly,tradeType=tradeType,priceType=priceType,postOnly=postOnly, timeInForce=timeInForce,symbol=symbol,marginType=marginType, side=side, positionSide=position_side, **kwargs)
        return order
    except Exception as e:
        print(e)



def sidess2(num=None,acc1=None,acc2=None,time11=None):#成交控制
    try:
    #for i in range(num):
        pri = float(ket3.getSpotList(symbol, ne=3))
    # def execute_place_order():
        for i in range(num):
            d = round(random.uniform(acc1, acc2))
            swq = random.randint(0, 1)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if swq == 1:
                b=place_order('buy', 'long', price=pri, orderQty=d)
                a=place_order('sell', 'short', price=pri, orderQty=d)
                print(b['msg'],pri,current_time)
            else:
                b=place_order('sell', 'short', price=pri, orderQty=d)
                a=place_order('buy', 'long', price=pri, orderQty=d)
                print(b['msg'],pri,d,current_time)
            time.sleep(time11)
    except Exception as e:
        print(e)


    # #创建线程池
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     # 提交任务给线程池
    #     results = [executor.submit(execute_place_order) for _ in range(num)]
    #
    #     # 获取结果
    #     for future in concurrent.futures.as_completed(results):
    #         future.result()

def save_data():
    # 获取当前时间
    current_minute = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 从数据列表中筛选出本分钟的数据
    minute_data = [data for data in data_list if data['time'].startswith(current_minute)]

    if not minute_data:
        return

    # 按时间排序
    sorted_data = sorted(minute_data, key=lambda x: x['time'])

    # 获取最高价和最低价
    highest_price = max(sorted_data, key=lambda x: x['high'])['high']
    lowest_price = min(sorted_data, key=lambda x: x['low'])['low']

    # 获取总成交量
    total_volume = sum(data['volume'] for data in sorted_data)

    # 将结果写入文件或数据库等
    with open('minute_data.txt', 'a') as file:
        file.write(f"{current_minute}, {highest_price}, {lowest_price}, {total_volume}\n")

if __name__ == '__main__':
    for i in range(10000):
        print(sidess2(num=50,time11=1,acc1=2,acc2=10))