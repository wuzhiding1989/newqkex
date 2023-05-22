import base64
import hashlib
import hmac
import json
import threading
import time
import uuid
import xlwt
import xlrd

import requests as requests

#dev
# api_key = "6364c7041be6ef0007a5fa8a"
# api_secret = "9bcdf0b2-182f-49ae-b89b-1d78c6edb2b4"
# api_passphrase = "12345678"
# base_url = 'https://futures-api.dev-polo-fts.com'


# stage
api_key = "63579202c4cf9100062197e7"
api_secret = "b69ff537-fdf3-4856-9571-a76047333b61"
api_passphrase = "12345678"
base_url = 'https://stg-futures-api.poloniex.com'

#prod
# api_key = "635a537c6c17300007941464"
# api_secret = "3b577913-3bab-4635-82bf-813dc79bf357"
# api_passphrase = "12345678"
# base_url = 'https://futures-api.poloniex.com'

def withdrawMargin(symbol,bizNo,margin):
    url = base_url+'/api/v1/position/margin/withdraw-margin';
    now = int(time.time() * 1000);
    data = {"symbol": symbol, "bizNo": bizNo, "margin": margin};
    data_json = json.dumps(data);
    str_to_sign = str(now) + 'POST' + '/api/v1/position/margin/withdraw-margin' + data_json;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('post', url, headers=headers, data=data_json);
    print(response.json());
    return

def depositMargin(symbol,bizNo,margin):
    url = base_url+'/api/v1/position/margin/deposit-margin';
    now = int(time.time() * 1000);
    data = {"symbol": symbol, "bizNo": bizNo, "margin": margin};
    data_json = json.dumps(data);
    str_to_sign = str(now) + 'POST' + '/api/v1/position/margin/deposit-margin' + data_json;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('post', url, headers=headers, data=data_json);
    print(response.json());
    return

def autoDepositStatus(symbol,status):
    url = base_url+'/api/v1/position/margin/auto-deposit-status';
    now = int(time.time() * 1000);
    data = {"symbol": symbol, "status": status};
    data_json = json.dumps(data);
    str_to_sign = str(now) + 'POST' + '/api/v1/position/margin/auto-deposit-status' + data_json;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('post', url, headers=headers, data=data_json);
    print(response.json());
    return

def positions():
    url = base_url+'/api/v1/positions';
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'GET' + '/api/v1/positions';
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('get', url, headers=headers);
    print(response.json());
    return

def positionDetail(symbol):
    url = base_url+'/api/v1/position?symbol='+symbol;
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'GET' + '/api/v1/position?symbol='+symbol;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('get', url, headers=headers);
    print(str(response.json()));
    return


def placeOrder(symbol,price,size,side,clientId):
    url = base_url+'/api/v1/orders';
    now = int(time.time() * 1000);
    data = {
        "clientOid": clientId,
        "reduceOnly": False,
        "closeOrder": False,
        "forceHold": False,
        "hidden": False,
        "iceberg": False,
        "leverage": 20,
        "postOnly": False,
        "price": price,
        "remark": "remark",
        "side": side,
        "size": size,
        "stop": "",
        "stopPrice": "1",
        "stopPriceType": "",
        "symbol": symbol,
        "timeInForce": "",
        "type": "limit",
        "visibleSize": 0
    };
    data_json = json.dumps(data);
    str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('post', url, headers=headers, data=data_json);
    print(response.json());
    return


def cancelOrder(orderId):
    url = base_url+'/api/v1/orders/'+orderId;
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'DELETE' + '/api/v1/orders/'+orderId;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('DELETE', url, headers=headers);
    print(response.json());
    return

def cancelOrders(symbol):
    url = base_url+'/api/v1/orders?symbol='+symbol;
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'DELETE' + '/api/v1/orders?symbol='+symbol;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('DELETE', url, headers=headers);
    print(response.json());
    return

def orderDetail(orderId):
    url = base_url+'/api/v1/orders/'+orderId;
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'GET' + '/api/v1/orders/'+orderId;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('GET', url, headers=headers);
    print(response.json());
    return

def liqdAndRuptPrice(symbol,price,size,leverage,posComm):
    url = base_url+'/app/v1/kumex-position/liqdAndRuptPrice';
    now = int(time.time() * 1000);
    data = {
        "leverage": leverage,
        "price": price,
        "currentQty": size,
        "symbol": symbol,
        "posComm": posComm
    };
    data_json = json.dumps(data);
    str_to_sign = str(now) + 'GET' + '/app/v1/kumex-position/liqdAndRuptPrice' + data_json;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('get', url, headers=headers, data=data_json);
    print(response.json());
    return


def queryMarginType(symbol):
    url = base_url+'/api/v1/marginType/query?symbol='+symbol;
    now = int(time.time() * 1000);
    str_to_sign = str(now) + 'GET' + '/api/v1/marginType/query?symbol='+symbol;
    print(str_to_sign);
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('GET', url, headers=headers);
    print(response.json());
    return


def test(symbol, mode):
    url = base_url + '/api/v1/test?symbol=' + symbol + "&mode=" + mode;
    now = int(time.time() * 1000);
    str_to_sign = str(
        now) + 'GET' + '/api/v1/test?symbol=' + symbol + "&mode=" + mode;
    print(str_to_sign);
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'),
                 hashlib.sha256).digest());
    headers = {
        "PF-API-SIGN": signature,
        "PF-API-TIMESTAMP": str(now),
        "PF-API-KEY": api_key,
        "PF-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    };
    response = requests.request('GET', url, headers=headers);
    print(response.json());
    return

def test1(mode):
    for _ in range(100):
        test("BTCUSDTPERP",mode)
        time.sleep(5)
    return

def many_thread():
    threading.Thread(target=test1,args=("route-set",)).start()
    threading.Thread(target=test1,args=("route-noset",)).start()
    # threads = []
    # for _ in range(1):  # 循环创建10个线程
    #     t = threading.Thread(target=test1,args=("route-set",))
    #     threads.append(t)
    # for t in threads:  # 循环启动10个线程
    #     t.start()
    return

def getBNPrice(symbol):
    url = 'https://www.binance.com/api/v3/uiKlines?limit=1000&symbol='+symbol+'&interval=1d';
    response = requests.request('GET', url);
    list=response.json();
    wb = xlwt.Workbook()
    ws = wb.add_sheet(symbol)
    for i,v in enumerate(list):
        timeArray = time.localtime(v[0]/1000)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        open=v[1];
        close=v[4];
        print (formatTime+','+open+','+close)
        ws.write(i, 0, formatTime)
        ws.write(i, 1, open)
        ws.write(i, 2, close)
    wb.save(symbol+'.xls')
    return

def getIXICPrice(symbol):
    url = 'https://finance.pae.baidu.com/selfselect/getstockquotation?code='+symbol+'&all=0&count=1000&ktype=1&isIndex=true&isBk=false&isBlock=false&isFutures=false&stockType=us&end_time=1671439027&market_type=us&group=quotation_index_kline&finClientType=pc';
    response = requests.request('GET', url);
    list=response.json()['Result'];
    wb = xlwt.Workbook()
    ws = wb.add_sheet(symbol)
    for i,v in enumerate(list):
        timeArray = time.localtime(int(v['time']))
        formatTime = time.strftime("%Y-%m-%d", timeArray)
        open=v['kline']['open'];
        close=v['kline']['close'];
        ws.write(i, 0, formatTime)
        ws.write(i, 1, open)
        ws.write(i, 2, close)
    wb.save(symbol+'.xls')
    return

# positionDetail('BTCUSDTPERP');
placeOrder('HNTUSDTPERP',1,3,"buy","8");
# depositMargin('ETHUSDTPERP',"586AEBD7529685240810",0.01);
# withdrawMargin('ETHUSDTPERP',"586AEBD7529685240811",0.9)
# autoDepositStatus('ETHUSDTPERP',True)
# placeOrder('ALGOUSDTPERP',0.403,1);
# placeOrder('HNTUSDTPERP',2,1,str(uuid.uuid1()));
# cancelOrder('6364d848c531fb0007e9cd9a');
# orderDetail('6364d848c531fb0007e9cd9a');
# cancelOrders('BTCUSDTPERP');
# many_thread();
# test("BTCUSDTPERP","route-set");
# queryMarginType('HNTUSDTPERP');
# getBNPrice("BTCUSDT");
# getIXICPrice('DJI');