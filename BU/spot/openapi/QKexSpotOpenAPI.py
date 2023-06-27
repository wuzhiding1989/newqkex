import base64
import hashlib
import hmac
import json
import threading
import time
import uuid
from urllib.parse import urljoin
import xlwt
import xlrd
import requests as requests

access_key = "d880ea3876955c91e295c097f693f879"
secret_key = "648b2c96822894236cec0fdc490bc788f639762c4f481ece8c41fbafc3745230"
api_passphrase = "123456"
host = 'https://test.qkex.com/'


class QKexSpotOpenAPI:

    def __init__(self, host, access_key, secret_key, api_passphrase):

        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._api_passphrase = api_passphrase

    def request(self, method, path, params=None,data=None, auth=False):
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = urljoin(self._host, path)

        headers = {
            "Content-Type": "application/json",
            "Cookie": "locale=en-US",
            "x-locale": "en-US"
        }

        if auth:
            now = int(time.time() * 1000)
            if params:
                # if type(params)!=list:
                #     if len(params) == 1:
                #         data = str(next(iter(params.values())))
                #         str_to_sign = str(now) + method + path + data
                #     else:
                #     data_json = json.dumps(params)
                #     str_to_sign = str(now) + method + path + data_json
                # else:
                data_json = json.dumps(params)

                str_to_sign = str(now) + method + path + data_json
            else:
                str_to_sign = str(now) + method + path

            signature = base64.b64encode(
                hmac.new(self._secret_key.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
            headers['ACCESS-SIGN'] = signature
            headers['ACCESS-TIMESTAMP'] = str(now)
            headers['ACCESS-KEY'] = self._access_key
            headers['ACCESS-PASSPHRASE'] = self._api_passphrase

        if params == None:
            response = requests.request(method, url, headers=headers).json()
            return response
        if method == 'POST':
            response = requests.request('POST', url, json=params, headers=headers).json()
            return response
        if method == 'GET':
            if data:
                response = requests.request('GET', url, json=params, headers=headers).json()
                return response
            else:
                response = requests.request('GET', url, params=params, headers=headers).json()
                return response
    #批量下单
    def bulkOrders(self, symbol, side, price, volume, systemOrderType):

        params = [{
            "side": side,
            "price": price,
            "volume": volume,
            "systemOrderType": systemOrderType
        }]
        path = f'/openapi/exchange/{symbol}/bulkOrders'

        res = self.request(method='POST', params=params, path=path, auth=True)
        return res
    #批量撤单
    def cancelOrdersAll(self, pairCode, orderlist):
        path = f'/openapi/exchange/{pairCode}/orders'
        params = orderlist
        res = self.request(method='DELETE', params=params, path=path, auth=True)
        return res

    #查询市场价格
    def ticker(self, pairCode=None):
        path = f'/openapi/exchange/public/{pairCode}/ticker'
        res = self.request(method='GET', path=path, auth=True)
        return res
    #查询订单
    def orders(self, **kwargs):
        """
        | 参数名 | 参数类型 | 是否必填 | 参数说明 |
        | ----- | ------ | ------ | ------ |
        | pairCode | String | 否 | 交易对名称 |
        | startDate | Long | 否 | 开始时间 |
        | endDate | Long | 否 | 结束时间 |
        | price | BigDecimal | 否 | 价格 |
        | amount | BigDecimal | 否 | 数量 |
        | systemOrderType | Integer | 订单类型 0：限价单，1：市价单 |
        | source | String | 否 | 订单来源 固定 web |
        | page | Integer | 否 | 页数 不传默认1 |
        | pageSize | Integer | 否 | 每页大小 不传默认10 |
        """
        params = {}
        path = '/openapi/exchange/orders'
        for key, value in kwargs.items():
            if value:
                params[key] = value
        if len(params) == 0:
            res = self.request(method='GET', path=path, auth=True)
        else:
            res = self.request(method='GET', path=path, params=params, auth=True).json()
        return res

    # def orders1(self, pairCode=None, startDate=None, endDate=None, price=None, amount=None, systemOrderType=None,
    #             source=None,
    #             page=None, pageSize=None):
    #
    #     path = '/openapi/exchange/orders'
    #     params = {
    #         'pairCode': pairCode,
    #         'startDate': startDate,
    #         'endDate': endDate,
    #         'price': price,
    #         'amount': amount,
    #         'systemOrderType': systemOrderType,
    #         'source': source,
    #         'page': page,
    #         'pageSize': pageSize
    #     }
    #     res = self.request(method='GET', json=params, path=path, auth=True).json()
    #     return res

    #查询盘口数据
    def orderBook(self, pairCode=None, **kwargs):
        path = f'/openapi/exchange/public/{pairCode}/orderBook'
        params = {}
        for key, value in kwargs.items():
            if value:
                params[key] = value
        if len(params) == 0:
            res = self.request(method='GET', path=path, auth=True).json()
        else:
            res = self.request(method='GET', path=path, data=params, auth=True)
        return res
    #查询k线
    def Kline(self, pairCode, interval, start=None, end=None):
        path = f'/openapi/exchange/public/{pairCode}/candles'
        params = {
            'interval': interval,
            'start': start,
            'end': end
        }
        res = self.request(method='GET', path=path, params=params, auth=False).json()
        return res
    #单个下单
    def plranorder(self, pairCode=None, side=None, volume=None, price=None, quoteVolume=None, systemOrderType=None,
                   source=None):
        path = f'/openapi/exchange/{pairCode}/orders'
        params = {
            "price": price,
            "quoteVolume": quoteVolume,
            "side": side,
            "source": source,
            "systemOrderType": systemOrderType,
            "volume": volume
        }

        res = self.request(method='POST', params=params, path=path, auth=True)
        return res
    #单个撤单
    def cancelOrders(self,pairCode,id):
        path = f'/openapi/exchange/{pairCode}/orders/{id}'
        res = self.request(method='DELETE', path=path, auth=True)
        if res.status_code == 200:
            return res
        else:
            return res.json()

    # 历史成交
    def fulfillment(self,pairCode, isHistory, startDate=None, endDate=None, systemOrderType=None, price=None, amount=None,
                    source=None, page=None, pageSize=None):
        path = f'/openapi/exchange/{pairCode}/fulfillment'
        params = {
            'isHistory': isHistory,
            'startDate': startDate,
            'endDate': endDate,
            'systemOrderType': systemOrderType,
            'price': price,
            'amount': amount,
            'source': source,
            'page': page,
            'pageSize': pageSize

        }
        res = self.request(method='GET', data=params, path=path, auth=True).json()
        return res
    #查询最新成交
    def fills(self,pairCode):
        path = f'/openapi/exchange/public/{pairCode}/fills'
        res = self.request(method='GET', path=path, auth=True).json()
        return res

    #查所有资产
    def assetsAll(self):
        path = '/openapi/exchange/assets'
        res = self.request(method='GET', path=path, auth=True).json()
        return res

    #获取单个币对资产
    def assets(self,symbol):
        path = f'/openapi/exchange/{symbol}/assets'
        res = self.request(method='GET', path=path, auth=True).json()
        return res


if __name__ == '__main__':
    qk = QKexSpotOpenAPI(host=host, access_key=access_key, secret_key=secret_key, api_passphrase=api_passphrase)
    # print(qk.bulkOrders('BTC_USDT', 'buy', '28800', '1', 'limit'))
    # print(qk.cancelOrdersALl(pairCode='BTC_USDT',orderlist=[123,312]))
    #print(qk.orders(pairCode='QK_USDT'))
    print(qk.ticker(pairCode='BTC_USDT'))
    # print(qk.orders1(pairCode='BTC_USDT'))
    # print(qk.orderBook(pairCode='BTC_USDT',size=1))
    # print(qk.Kline(pairCode='BTC_USDT',interval='15min'))
    # print(qk.plranorder(pairCode='QK_USDT',side='buy',price='0.06',volume='100',systemOrderType='limit',source='api'))
    # print(qk.cancelOrders(pairCode='QK_USDT', id=171616134583360))
    # print(qk.fulfillment(pairCode='QK_USDT', isHistory=True, systemOrderType=0))
    # print(qk.fills(pairCode='QK_USDT'))
    # print(qk.assetsAll())
    # print(qk.assets(symbol='QK'))
