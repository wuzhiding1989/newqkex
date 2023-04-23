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
host = 'http://172.31.24.7'

class QKexSpotOpenAPI:

    def __init__(self, host, access_key, secret_key, api_passphrase):

        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._api_passphrase = api_passphrase

    def request(self, method, path, params=None, auth=False):
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
        if method =='POST':
            response = requests.request('POST', url, json=params, headers=headers).json()
            return response
        if method == 'GET':
            response = requests.request('GET', url, params=params, headers=headers).json()
            return response

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

    def cancelOrders(self, pairCode,orderlist):
        path = f'/openapi/exchange/{pairCode}/orders'
        params = orderlist
        res = self.request(method='DELETE', params=params, path=path, auth=True)
        return res

    def ticker(self, pairCode=None):
        path = f'/openapi/exchange/public/{pairCode}/ticker'
        res = self.request(method='GET', path=path, auth=True)
        return res

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
            res = self.request(method='GET', path=path, params=params, auth=True)
        return res
    def orders1(self,pairCode=None, startDate=None, endDate=None, price=None, amount=None, systemOrderType=None, source=None,
           page=None, pageSize=None):

        path = '/openapi/exchange/orders'
        params = {
            'pairCode': pairCode,
            'startDate': startDate,
            'endDate': endDate,
            'price': price,
            'amount': amount,
            'systemOrderType': systemOrderType,
            'source': source,
            'page': page,
            'pageSize': pageSize
        }
        res = self.request(method='GET', params=params, path=path, auth=True)
        return res
    def orderBook(self, pairCode=None, **kwargs):
        path = f'/openapi/exchange/public/{pairCode}/orderBook'
        params = {}
        for key, value in kwargs.items():
            if value:
                params[key] = value
        if len(params) == 0:
            res = self.request(method='GET', path=path, auth=True)
        else:
            res = self.request(method='GET', path=path, params=params, auth=True)
        return res

    def Kline(self, pairCode, interval, start=None, end=None):
        path = f'/openapi/exchange/public/{pairCode}/candles'
        params = {
            'interval': interval,
            'start': start,
            'end': end
        }
        res = self.request(method='GET', path=path, params=params, auth=False)
        return res

if __name__ == '__main__':
    qk = QKexSpotOpenAPI(host=host,access_key=access_key,secret_key=secret_key,api_passphrase=api_passphrase)
    print(qk.bulkOrders('BTC_USDT', 'buy', '28800', '1', 'limit'))
    # print(qk.cancelOrders(pairCode='BTC_USDT',orderlist=[123,312]))
    # print(qk.orders(pairCode='BTC_USDT'))
    # print(qk.ticker(pairCode='BTC_USDT'))
    # print(qk.orders1(pairCode='BTC_USDT'))
    # print(qk.orderBook(pairCode='BTC_USDT',size=1))
    # print(qk.Kline(pairCode='BTC_USDT',interval='15min'))