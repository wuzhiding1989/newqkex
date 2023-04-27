import base64
import hashlib
import hmac
import json
import time
from common.mysql_san import mysql_select
from common.util import d,symbolbase,price,exchange_fee

import requests as requests

api_key = "d880ea3876955c91e295c097f693f879"
api_secret = "648b2c96822894236cec0fdc490bc788f639762c4f481ece8c41fbafc3745230"
api_passphrase = "123456"
base_url = 'http://13.215.135.141'


def placeOrder(symbol, side, price, volume, systemOrderType):
    path = '/openapi/exchange/' + symbol + '/bulkOrders'
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data = [{
        "side": side,
        "price": price,
        "volume": volume,
        "systemOrderType": systemOrderType
    }]
    data_json = json.dumps(data)

    signature = sign(now, 'POST', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('POST', url, headers=headers, data=data_json).json()
    return response


def cancelOrders(symbol):
    path = f'/openapi/exchange/{symbol}/orders'
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data = [123, 345]
    data_json = json.dumps(data)
    signature = sign(now, 'DELETE', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('DELETE', url, headers=headers, json=data).json()
    return response


def ticker(pairCode):
    path = f'/openapi/exchange/public/{pairCode}/ticker'
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    signature = sign(now, 'POST', path, '', '')
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('POST', url, headers=headers).json()
    return response


def orders(pairCode=None, startDate=None, endDate=None, price=None, amount=None, systemOrderType=None, source=None,
           page=None, pageSize=None):
    path = f'/openapi/exchange/orders'
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
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers, data=data_json).json()
    return response


def orderBook(pairCode, size=None):
    path = f'/openapi/exchange/public/{pairCode}/orderBook'
    params = {
        'size': size,
    }
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers, data=data_json).json()
    return response


def kline(pairCode, interval, start=None, end=None):
    path = f'/openapi/exchange/public/{pairCode}/candles'
    params = {
        # 'pairCode': pairCode,
        "interval": interval,
        'start': start,
        'end': end
    }
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers,params=params).json()
    return response


# 历史成交
def fulfillment(pairCode, isHistory, startDate=None, endDate=None, systemOrderType=None, price=None, amount=None,
                source=None, page=None, pageSize=None):
    path = f'/openapi/exchange/{pairCode}/fulfillment'
    params = {
        'pairCode': pairCode,
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
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers, data=data_json).json()
    return response
#最新成交
def fills(pairCode):
    path = f'/openapi/exchange/public/{pairCode}/fills'
    params = {
        'pairCode': pairCode
    }
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers, data=data_json).json()
    return response

def assetsAll():
    path = '/openapi/exchange/assets'
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    # data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', '')
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers).json()
    return response

def assets(symbol):
    path = f'/openapi/exchange/{symbol}/assets'
    params ={
        'symbol': symbol
    }
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data_json = json.dumps(params)
    signature = sign(now, 'GET', path, '', data_json)
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": "locale=en-US",
        "x-locale": "en-US"
    }
    response = requests.request('GET', url, headers=headers, data=data_json).json()
    return response

def sign(timestamp, method, requestPath, queryString, body):
    if len(queryString) == 0:
        queryString = ""
    else:
        queryString = "?" + queryString
    preHash = str(timestamp) + method + requestPath + queryString + body
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), preHash.encode('utf-8'), hashlib.sha256).digest())
    return signature

def order(pairCode=None, side=None, volume=None, price=None, quoteVolume=None, systemOrderType=None, source=None,locale=None):
    path = '/openapi/exchange/' + pairCode + '/orders'#单个下单接口
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    data = {
        "side": side,
        "price": price,
        "volume": volume,
        "quoteVolume": quoteVolume,
        "source": source,
        "systemOrderType": systemOrderType
    }
    data_json = json.dumps(data)

    signature = sign(now, 'POST', path, '', data_json)#zh-HK,en-US
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": f"locale={locale}",
        "x-locale": locale
    }
    response = requests.request('POST', url, headers=headers, data=data_json).json()
    return response

def delete_order(pairCode,id,locale=None):#撤销单个订单
    path = f'/openapi/exchange/{pairCode}/orders/{id}'
    url = base_url + path
    timestamp = time.time()
    now = int(timestamp * 1000)
    signature = sign(now, 'DELETE', path, '', '')
    headers = {
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": str(now),
        "ACCESS-KEY": api_key,
        "ACCESS-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json",
        "Cookie": f"locale={locale}",
        "x-locale": locale
    }
    response = requests.request('DELETE', url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return response.json()
def te_test(locale='en-US',side='sell',pairCode='ABF_USDT',systemOrderType='limit'):#zh-HK,en-US
    base=(symbolbase(pairCode))['base'];quote=(symbolbase(pairCode))['quote']
    if side=='buy':
        assets1=assets(quote)
        available=assets1['available'];hold=assets1['hold']
        print(f'{quote}初始可用资产为{available},初始冻结资产为{hold}')
        order_id = order(pairCode=pairCode, side=side, price='0.0802', volume='310', systemOrderType=systemOrderType,
                         source='api',locale=locale)
        time.sleep(2)
        print(order_id)
        data=orders(pairCode=pairCode)
        ids = [item['id'] for item in data]
        sql_select=f"SELECT id,side,entrust_price,amount,entrust_price*amount,source_info,`status` FROM exchange.qk_usdt_orders WHERE id={order_id}"
        cc=mysql_select(sql_select)
        print(ids,cc)
        print('数据库查询订单数据',cc)
        if order_id in ids:
            print("当前委托订单包含当前订单id")
        else:
            print("当前委托订单不包含当前订单id")
        assets2 = assets('USDT')
        available1 = assets2['available'];hold1 = assets2['hold']
        ava=d(available)-d(available1);una=d(hold1)-d(hold)
        print(f'{quote}变化后可用资产为{available1},变化后冻结资产为{hold1},可用减少了{ava},冻结增多了{una}')
    else:
        assets1 = assets(base)
        available = assets1['available'];hold = assets1['hold']
        print(f'{base}初始可用资产为{available},初始冻结资产为{hold}')
        order_id = order(pairCode=pairCode, side=side, price='0.0803', volume='310', systemOrderType=systemOrderType,
                         source='api', locale=locale)
        time.sleep(2)
        print(order_id)
        data = orders(pairCode=pairCode)
        ids = [item['id'] for item in data]
        sql_select = f"SELECT id,side,entrust_price,amount,entrust_price*amount,source_info,`status` FROM exchange.qk_usdt_orders WHERE id={order_id}"
        cc = mysql_select(sql_select)
        print(ids)
        print('数据库查询订单数据', cc)
        if order_id in ids:
            print("当前委托订单包含当前订单id")
        else:
            print("当前委托订单不包含当前订单id")
        assets2 = assets(base)
        available1 = assets2['available'];
        hold1 = assets2['hold']
        ava = d(available) - d(available1);
        una = d(hold1) - d(hold)
        print(f'{base}变化后可用资产为{available1},变化后冻结资产为{hold1},可用减少了{ava},冻结增多了{una}')

def te_test1(locale='en-US',side='buy',pairCode='ABF_USDT',systemOrderType='limit',price1='1.1',volume='30'):#zh-HK,en-US
    base=(symbolbase(pairCode))['base'];quote=(symbolbase(pairCode))['quote']
    buyprice=(price(pairCode))['bid'][0];sellprice=(price(pairCode))['ask'][0]
    print(buyprice,sellprice)
    baseassets = assets(base);quoteassets = assets(quote)
    base_available = baseassets['available'];base_hold = baseassets['hold']
    quote_available = quoteassets['available'];quote_hold = quoteassets['hold']
    t_fee=exchange_fee(pairCode=pairCode)['tickerFeesRate'];m_fee=exchange_fee(pairCode=pairCode)['makerFeesRate']
    print(12,t_fee,m_fee)
    print(
        f'{base}初始可用资产为{base_available},初始冻结资产为{base_hold},{quote}初始可用资产为{quote_available},初始冻结资产为{quote_hold}')
    if side=='buy':
        order_id = order(pairCode=pairCode, side=side, price=price1, volume=volume, systemOrderType=systemOrderType,
                         source='api',locale=locale)
        time.sleep(4)
        print(order_id)
        sel=f"SELECT CASE WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_orders WHERE id ={order_id}) THEN 1 WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_order_fulfillment WHERE id = {order_id} AND `status`=2) THEN 2 WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_order_fulfillment WHERE id ={order_id} AND `status`=-1) THEN 3 END AS idc"
        order_status=mysql_select(sel)
        print(order_status[0][0])
        baseassets1 = assets(base);quoteassets1 = assets(quote)
        newbase_available = baseassets1['available'];newbase_hold = baseassets1['hold']
        newquote_available = quoteassets1['available'];newquote_hold = quoteassets1['hold']
        if order_status[0][0]==1:#订单未成交
            if d(newquote_available) + d(price1)*d(volume) -d(quote_available) <0.00000001 \
                    and d(newquote_hold) - d(price1)*d(volume) -d(quote_hold) <0.00000001 \
                    and d(newbase_hold) - d(base_hold)==0 \
                    and d(newbase_available) - d(base_available)==0:
                print(f'交易后的{base}和{quote}可用资产和冻结资产检验正确')
            else:
                print(f'资产校验失败,{base}变化后可用资产为{newbase_available},变化后冻结资产为{newbase_hold},{quote}变化后可用资产为{newquote_available},变化后冻结资产为{newquote_hold}')
        elif order_status[0][0]==2:#订单已成交
            c=d(newquote_available)+d(price1)*d(volume)-d(quote_available)
            cc=d(newbase_available)- d(price1) -d(base_available)
            print(1222222,c,cc)

    else:
        assets1 = assets(base)
        available = assets1['available'];hold = assets1['hold']
        print(f'{base}初始可用资产为{available},初始冻结资产为{hold}')
        order_id = order(pairCode=pairCode, side=side, price='0.0803', volume='310', systemOrderType=systemOrderType,
                         source='api', locale=locale)
        time.sleep(2)
        print(order_id)
        data = orders(pairCode=pairCode)
        ids = [item['id'] for item in data]
        sql_select = f"SELECT id,side,entrust_price,amount,entrust_price*amount,source_info,`status` FROM exchange.qk_usdt_orders WHERE id={order_id}"
        cc = mysql_select(sql_select)
        print(ids)
        print('数据库查询订单数据', cc)
        if order_id in ids:
            print("当前委托订单包含当前订单id")
        else:
            print("当前委托订单不包含当前订单id")
        assets2 = assets(base)
        available1 = assets2['available'];
        hold1 = assets2['hold']
        ava = d(available) - d(available1);
        una = d(hold1) - d(hold)
        print(f'{base}变化后可用资产为{available1},变化后冻结资产为{hold1},可用减少了{ava},冻结增多了{una}')

if __name__ == '__main__':
    # 批量下单 （测试通过）
    #print(placeOrder('QK_USDT', 'buy', '0.303', '1', 'limit'))
    # 批量撤单 (测试通过)
    # print(cancelOrders(symbol='QK_USDT'))
    # 查询当前订单列表 （返回空数组[]）
    #print(123,orders(pairCode='QK_USDT'))
    # 查询市场价格(测试通过)
    # print(ticker(pairCode='QK_USDT'))
    # 查盘口数据 （测试通过）
    # print(orderBook(pairCode='QK_USDT',size=2))
    # k线数据  (测试通过)
    # print(kline(pairCode='BTC_USDT', interval='15min'))
    # 查历史成交 （返回空数组[]）
    print(fulfillment(pairCode='ABF_USDT',isHistory=True,systemOrderType=0))
    # 查最新成交 (测试通过)
    # print(fills(pairCode='QK_USDT'))
    # 查所有资产 （测试通过）
    # print(assetsAll())
    # 查单个币种资产 (测试通过)
    # print(assets(symbol='QK'))171613964292160
    #A=(order(pairCode='QK_USDT',side='buy',price='0.0795',volume='300',systemOrderType='limit',source='api'))
    # print(123,orders(pairCode='QK_USDT'))
    # time.sleep(2)
    # print(delete_order(pairCode='QK_USDT',id=171618715009088))
    #print(te_test1())


