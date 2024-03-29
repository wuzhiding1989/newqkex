"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: c2cprocess
@time: 2023-05-18 
@desc: 
"""
from BU.spot.api.webapi import otc_orders, otc_orders_ads_select, otc_pending, consumer_otc_pending, consumer_my_order, \
    otc_pendings_paid, consumer_otc_pendings_paid, otc_pendings_complete
from common.getCookie import login
from common.get_googleAuthenticator import read_google_authenticator_code


class C2CProcess:
    _Authorization1=login(account="42345678@qq.com",password="qa123456",verifyCode="111111")
    _Authorization2=login(account="52345678@qq.com",password="qa123456",verifyCode="111111")
    def c2cprocess_one(self):
        """广告商发布卖币广告-用户全买-用户支付-广告商放币"""
        #广告商发布广告
        res=otc_orders(amount="0.10000000", side="sell", base="BTC", quote="USD", price="30000.00000000", payType=[3])
        if res["code"]==0:
            print("广告商发布广告成功")
        #广告商查询广告地址
        res=otc_orders_ads_select()

        id=res["data"][0]["id"]
        #用户下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization1,orderId=id,amount="0.09090909")
        # print(res)
        #用户我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization1,status="98",page="1",pageSize="1000")
        orderid=res['data']['items'][0]["id"]
        #用户我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization1,orderid=orderid,payment=403)
        # googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS")
        res=otc_pendings_complete(orderid=orderid,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        print("res:---",res)

    def c2cprocess_two(self):
        """广告商发布卖币广告-2个用户全买-用户支付-广告商放币"""
        res=otc_orders(amount="0.10000000", side="sell", base="BTC", quote="USD", price="30000.00000000", payType=[3])
        #广告商查询广告地址
        res=otc_orders_ads_select()
        id=res["data"][0]["id"]
        # print(id)
        #用户1下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization1,orderId=id,amount="0.05")
        # print(res)
        #用户1我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization1,status="98",page="1",pageSize="1000")
        orderid1=res['data']['items'][0]["id"]
        #用户1我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization1,orderid=orderid1,payment=403)
        #用户2下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization2,orderId=id,amount="0.04090909")
        # print(res)
        #用户2我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization2,status="98",page="1",pageSize="1000")
        orderid2=res['data']['items'][0]["id"]
        #用户2我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization2,orderid=orderid2,payment=403)
        #广告商放币
        res=otc_pendings_complete(orderid=orderid1,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        res=otc_pendings_complete(orderid=orderid2,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        print("广告商成功放币")

    def c2cprocess_three(self):
        """广告商发布卖币广告-用户全买-用户支付-广告商放币"""
        #广告商发布广告
        res=otc_orders(amount="0.10000000", side="sell", base="BTC", quote="USD", price="30000.00000000", payType=[3])
        if res["code"]==0:
            print("广告商发布广告成功")
        #广告商查询广告地址
        res=otc_orders_ads_select()
        # if res["code"]==0:
        id=res["data"][0]["id"]
            # print("广告商发布广告成功")
        # print(id)
        #用户下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization1,orderId=id,amount="0.09090909")
        # print(res)
        #用户我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization1,status="98",page="1",pageSize="1000")
        orderid=res['data']['items'][0]["id"]
        #用户我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization1,orderid=orderid,payment=403)
        # googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS")

        #广告商我已付币
        # res=otc_pendings_complete(orderid=orderid,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        # print("res:---",res)

    def c2cprocess_four(self):
        """广告商发布卖币广告-2个用户全买-用户支付-广告商放币"""
        res=otc_orders(amount="0.10000000", side="sell", base="BTC", quote="USD", price="30000.00000000", payType=[3])
        #广告商查询广告地址
        res=otc_orders_ads_select()
        id=res["data"][0]["id"]
        # print(id)
        #用户1下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization1,orderId=id,amount="0.05")
        # print(res)
        #用户1我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization1,status="98",page="1",pageSize="1000")
        orderid1=res['data']['items'][0]["id"]
        #用户1我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization1,orderid=orderid1,payment=403)
        #用户2下C2C单
        res=consumer_otc_pending(Authorization1=self._Authorization2,orderId=id,amount="0.04090909")
        # print(res)
        #用户2我的订单列表
        res=consumer_my_order(Authorization1=self._Authorization2,status="98",page="1",pageSize="1000")
        orderid2=res['data']['items'][0]["id"]
        #用户2我已支付
        res=consumer_otc_pendings_paid(Authorization1=self._Authorization2,orderid=orderid2,payment=403)
        #广告商放币
        res=otc_pendings_complete(orderid=orderid1,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        res=otc_pendings_complete(orderid=orderid2,tradePassword="qa123456",googleVerifyCode=read_google_authenticator_code("2KYSFNGE3YJCZGTS"))
        print("广告商成功放币")





if __name__ == '__main__':
    C2CProcess().c2cprocess_three()