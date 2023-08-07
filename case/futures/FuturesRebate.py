import requests

from BU.admin.web import getAccessToken
from common.mysql_san import add_wallet_account


class FuturesRebate:
    def __init__(self,user,password):
        self.Authorization=Login().login(user,password)
        # self.Authorization="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0MDEwZGIzMy0xOTdmLTRlYzYtYmMwMy03Nzc2NzgyYmQwYjYxODI5NjE4MDA3IiwidWlkIjoiUVY0U3lPK2ZvemtvK0ZuWklyeE85QT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiIvY2s4bE52T0JwME5WanNoSUhDSG5RPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY5MTQwMDQyOSwiZXhwIjoxNjkxNDg2ODI5LCJpc3MiOiJ3Y3MifQ.HRTofaT77i4GTT0GsDBeq6qw_nUYQjLEL5xpE2rYa0M"
        self.headers={"Content-Type":"application/json",
                      "X-Locale":"zh-HK",
                      "X-Authorization":self.Authorization,
                      "Source":"web"}


    def futures_order(self):#市价买入
        url="https://test-futures-rest.qkex.com/v1/trade/web/orders"
        data={"tradeType":"linearPerpetual",
              "symbol":"BTCUSDT",
              "side":"buy",
              "positionSide":"long",
              "orderType":"market",
              "orderQty":"160",
              "marginType":"cross"}
        response=requests.request(method="post",url=url,json=data,headers=self.headers,verify=False)
        return response.json()

    def sell_order(self,availPos):#平仓
        url="https://test-futures-rest.qkex.com/v1/trade/web/orders"
        data={"tradeType":"linearPerpetual",
              "symbol":"BTCUSDT",
              "side":"sell",
              "positionSide":"long",
              "marginType":"cross",
              "priceType":"optimalN",
              "orderType":"market",
              "orderQty":availPos}
        response=requests.request(method="post",url=url,json=data,headers=self.headers,verify=False)
        return response.json()

    def get_position(self):#仓位查询
        url="https://test-futures-rest.qkex.com/v1/trade/web/position?tradeType=linearPerpetual"
        res=requests.request(method="get",url=url,headers=self.headers,verify=False)
        return res.json()

    def get_tradingAccount(self):#资产查询
        url="https://test-futures-rest.qkex.com/v1/trade/web/tradingAccount"
        res=requests.request(method="get",headers=self.headers,url=url,verify=False)

        return res.json()
    def get_uid(self):
        url="https://test-public-rest.qkex.com/user/detail"
        res=requests.request(method="get",headers=self.headers,url=url,verify=False)
        return res.json()

class Login:

    def login(self,user,password):
        url="https://test-public-rest.qkex.com/user/login"
        headers={"Content-Type":"application/json"}
        data={"account":user,"password":password,
              "verifyCode":"111111"}

        rep=requests.request(method="post",json=data,url=url,headers=headers,verify=False)
        print(rep.json())
        return rep.json()["data"]["accessToken"]


if __name__ == '__main__':
    user_list=["697Ma@163.com","629Ma@163.com","639Ma@163.com","649Ma@163.com","659Ma@163.com"]
    for item in user_list:
    #登录
        user=FuturesRebate(user=item,password="qa123456")
        #资产查询
        tradeingAccount=user.get_tradingAccount()
        uid=user.get_uid()["data"]["userId"]
        try:
            if float(tradeingAccount['data'][0]["marginAvailable"])>4999:
            #下单
               print("用户资产够5000")
            else:
                add_wallet_account(uid=uid,currency="USDT",balance="5000")
        except Exception as e:
            print(e)

        finally:
            for i in range(5):
                order_data=user.futures_order()
                print("用户下单",order_data)
                while len(user.get_position()["data"]) > 0:
                    availPos = user.get_position()["data"][0]["availPos"]
                    # 平仓
                    sell_order_data=user.sell_order(availPos)
                    print("用户平仓",sell_order_data)


