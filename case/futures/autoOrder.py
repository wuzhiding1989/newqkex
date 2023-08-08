import random

import requests
import urllib3

urllib3.disable_warnings()
class AutoOrder:
    def __init__(self,user,password):
        self.Authorization=Login().login(user,password)
        # self.Authorization="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0MDEwZGIzMy0xOTdmLTRlYzYtYmMwMy03Nzc2NzgyYmQwYjYxODI5NjE4MDA3IiwidWlkIjoiUVY0U3lPK2ZvemtvK0ZuWklyeE85QT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiIvY2s4bE52T0JwME5WanNoSUhDSG5RPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY5MTQwMDQyOSwiZXhwIjoxNjkxNDg2ODI5LCJpc3MiOiJ3Y3MifQ.HRTofaT77i4GTT0GsDBeq6qw_nUYQjLEL5xpE2rYa0M"
        self.headers={"Content-Type":"application/json",
                      "X-Locale":"zh-HK",
                      "X-Authorization":self.Authorization,
                      "Source":"web"}


    def buy_order(self,price):
        """
        开多
        :param price:
        :return:
        """
        url="https://test-futures-rest.qkex.com/v1/trade/web/orders"
        data={"tradeType":"linearPerpetual",
              "symbol":"BTCUSDT",
              "side":"buy",
              "positionSide":"long",
              "orderType":"limit",
              "orderQty":"1",
              "marginType":"cross",
              "postOnly":False,
              "timeInForce":"GTC",
              "price":price}
        response=requests.request(method="post",url=url,json=data,headers=self.headers,verify=False)
        return response.json()


    def sell_order(self,price):
        """
        开空
        :param price:
        :return:
        """
        url="https://test-futures-rest.qkex.com/v1/trade/web/orders"
        data={"tradeType":"linearPerpetual",
              "symbol":"BTCUSDT",
              "side":"sell",
              "positionSide":"short",
              "orderType":"limit",
              "orderQty":"1",
              "marginType":"cross",
              "postOnly":False,
              "timeInForce":"GTC",
              "price":price}
        response=requests.request(method="post",url=url,json=data,headers=self.headers,verify=False)
        return response.json()

    def get_price(self):
        """
        获取价格
        :return:
        """
        url="https://test-futures-rest.qkex.com/v1/market/ticker/24hr?symbol=BTCUSDT&tradeType=linearPerpetual"
        res=requests.request(method="get",url=url)
        return res.json()


    def get_openOrders(self):
        """
        获取委托列表
        :return:
        """
        url="https://test-futures-rest.qkex.com/v1/trade/web/openOrders?tradeType=linearPerpetual&pageNum=1&pageSize=100"
        res=requests.request(method="get",url=url)
        return res.json()




class Login:

    def login(self, user, password):
        url = "https://test-public-rest.qkex.com/user/login"
        headers = {"Content-Type": "application/json"}
        data = {"account": user, "password": password,
                "verifyCode": "111111"}

        rep = requests.request(method="post", json=data, url=url, headers=headers, verify=False)
        print(rep.json())
        return rep.json()["data"]["accessToken"]

class AutoProcess:
    def process(self):
        user=AutoOrder(user="697Ma@163.com",password="qa123456")
        while True:
            if len(user.get_openOrders()['data'])<50:
                price=user.get_price()["data"][0]["lastPrice"]
                # offset=random.random(0,1)
                # price_order=float(price)+round(offset,2)
                side_list=["buy","sell"]
                if random.choice(side_list)=="buy":
                    offset = random.random(0, 1)
                    price_order = float(price) - round(offset, 2)
                    user.buy_order(price_order)
                else:
                    offset = random.random(0, 1)
                    price_order = float(price) + round(offset, 2)
                    user.sell_order(price_order)
            else:
                pass

if __name__ == '__main__':
    print(AutoOrder(user="697Ma@163.com",password="qa123456").get_price())
