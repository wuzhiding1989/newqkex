import random
from time import sleep

from BU.spot.api import webapi as wp
from common import util as ut, data as dt


headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzMjkzZDhiMi00MzA3LTQ4YjktODQ3ZS05MmVhOWFhZWJmMzE0MDcxMzQzNzUiLCJ1aWQiOiJ5YlRXQzNSU1VKbVhndkdJLzNWbFlnPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6IkE0akhmalBoeWxKbVJWa2VubTdmRWc9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjc5NTY4NTQ0LCJleHAiOjE2Nzk2NTQ5NDQsImlzcyI6IndjcyJ9.005ekNPToC9T-7tD0QksQt0sUx-ADexnOD47Ryd45mQ'
headers['X-Authorization']=Authorization
url = 'http://13.215.135.141'
account='10081@qq.com'
password='aa123456'
verifyCode='111111'


symbol = 'DOT_USDT';
source = 'web'


def order():
    sides = ['buy','sell']
    for side in sides:
        # 获取买卖盘数据
        priceamount = ut.price(symbol=symbol)
        # 买入btc
        if side == 'buy':
            buyprice = priceamount['ask'][0]
            buyamount = round(random.uniform(5, 10), 2)

            quoteVolume = float(buyprice) * float(buyamount)
            # buyamount = priceamount['ask'][1]
            limitres = wp.orders(symbol=symbol, side=side, price=buyprice, systemOrderType='limit', volume=buyamount, source='web')
            print("限价买入：",limitres)
            sleep(1)
            #{"systemOrderType":"market","side":"buy","volume":"","quoteVolume":"13","source":"web","price":""}
            marketres = wp.orders(symbol=symbol, side=side, price='',quoteVolume=quoteVolume, systemOrderType='market', volume='',source='web')
            print("市价买入：",marketres)
        else:
            sellprice = priceamount['bid'][0]
            sellamount = round(random.uniform(5, 10), 2)
            limitres = wp.orders(symbol=symbol, side=side, price=sellprice, systemOrderType='limit', volume=sellamount, source='web')
            print("限价卖出：",limitres)
            sleep(1)
            #{"systemOrderType":"market","side":"sell","volume":"2.1","quoteVolume":"","source":"web","price":""}
            marketres = wp.orders(symbol=symbol, side=side, price='', systemOrderType='market', volume=sellamount, source='web')
            print("市价卖出：", marketres)
def placeorder(x):
    for i in range(1,x):
        try:
            order()
        except :
            print("The file does not exist.")


if __name__ == '__main__':
    placeorder(100000)