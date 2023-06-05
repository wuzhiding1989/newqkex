import time,requests,pygsheets


symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'sell';marginType = 'cross';positionSide = 'short'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce=None
fromAccountType='exchange';toAccountType='perpetual';currency='USDT';amount=40;pairCode='P_R_USDT_USD';gear='depth0';limit=1000
period='1m'
from datetime import datetime
from BU.futures.api import webapi as wb


def market_kline():
    user = wb.webapi(2, 'test')
    c = user.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit, period=period)
    print(f'k线接口{period}', c)
    ts=datetime.fromtimestamp(int(c['ts'])//1000)
    print('打印接口返回的ts时间',ts)
    for data in c['data'][:5]:
        # 将时间戳转换为日期时间格式
        timestamp_start = int(data[1]) // 1000
        datetime_start = datetime.fromtimestamp(timestamp_start)

        timestamp_end = int(data[2]) // 1000
        datetime_end = datetime.fromtimestamp(timestamp_end)

        # 打印所有数据
        print(f"周期: {data[0]}, 开盘时间: {datetime_start}, 收盘时间: {datetime_end}, "
              f"开盘价: {data[3]}, 收盘价: {data[4]}, 最高价: {data[5]}, 最低价: {data[6]}, "
              f"成交量: {data[7]}, 成交额: {data[8]}, 成交笔数: {data[9]}, 涨跌额: {data[10]}, "
              f"涨跌幅: {data[11]}")
    time.sleep(60)
def maker_trade():
    user = wb.webapi(2, 'test')
    res=user.web_market_trade(tradeType=tradeType, symbol=symbol, limit=limit)
    print('实时成交',res)
    ts=datetime.fromtimestamp(int(res['ts'])//1000)
    print('打印接口返回的ts时间',ts)
    for item in res['data'][:6]:
        ts = item['time'] / 1000
        dt = datetime.fromtimestamp(ts)
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        print({'side': item['side'], 'price': item['price'], 'qty': item['qty'], 'time': formatted_time})

        #print(f"方向: {data[0]}, 价格: {data[1]}, 数量: {data[2]},时间: {datetime_start}")
def kk():
    url='https://test-futures-rest.qkex.com/v1/market/kline?tradeType=linearPerpetual&symbol=BTCUSDT&period=1m'
    response1 = requests.get(url=url).json()
    time.sleep(60)
    response2 = requests.get(url=url).json()

    # 比较两次请求返回的数据是否一样
    data1_sorted = sorted(response1['data'], key=lambda x: x[2])
    data2_sorted = sorted(response2['data'], key=lambda x: x[2])

    # 找到 data2 最后更新的一条数据项
    last_updated_item = None
    for item in data2_sorted:
        if item not in data1_sorted:
            last_updated_item = item

    # 输出最后更新的数据项
    if last_updated_item:
        print(f"最后更新的数据项为：{last_updated_item}")
    else:
        print("data2 中没有新数据")

if __name__ == '__main__':
    # for i in range(2):
    # #     #print(market_kline())
    # #     print(maker_trade())
    #     print(kk())
    pygsheets.debug_level = 3
    client = pygsheets.authorize(service_file="lively-oxide-388602-33b9719fd3c6.json")
    # 打开谷歌表格testPygSheets
    sh = client.open('testqk')
    # 获取表格中的而第一张工作表
    wks = sh.sheet1
    # 更新A1数据
    wks.update_value('A1', "我是元素A1")
