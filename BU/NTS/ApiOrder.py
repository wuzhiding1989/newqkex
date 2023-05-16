from BU.NTS.WebOrder import n_order
from param.dict import DMap
from common.other import httpCheck as e
from config.urlConfig import orderUrls
from common.util import request_http as req, requests
from param import dict
from common.asserts import compare as com
from BU.Auth import Auth
from param.code_list import code_list as code
import os

# API_KEY = 'a0hrVRMhJ5Rpz0KxEeYNSLVXZW'
# API_SECRET = '71aeba08a82b1421ae10bde0b32f6f9b';

class NtsApiOrder:
    # global contract_code_date, contract_code_short, Auth , token

    def __init__(self, server, product=None, user_id=None, token=None):
        global auth
        self._server = server;
        self.user_id = user_id
        # if not user_id: user_id=defaultUserIdList[int(server)][0]

        if str(self.user_id) not in DMap['5'].keys():
            print(user_id+'用户未配置apikey，请到BU.NTS.comm.dict.py文件里的APiKeyQaMap配置')
            os._exit(0)
        else:
            self.source = 'API'
            self.Url1 = orderUrls[str(server)][0]
            self.Url = orderUrls[str(server)][0]
            self.Url_query = orderUrls[str(server)][1]
            self.API_KEY = DMap['5'][str(user_id)][0]
            self.API_SECRET = DMap['5'][str(user_id)][1]
            self.auth = Auth(self.API_KEY, self.API_SECRET)
            self.success_code = code["success"][0]
            # self.markPriceMap=self.webposition()
            self.instrument={}
            self.instrumentList = []
            instruments_r = self.instruments()
            if e(instruments_r)[0]:
                for dict in instruments_r['data']:
                    self.instrument[dict['symbol'][:-4]]=[dict['tickSize'],dict['ctVal'],dict['takerRate'] ,dict['makerRate']]
                    self.instrumentList.append(dict['symbol'])

        # if not token:
        #     getToken_r = self.getToken( )
        #     if getToken_r == "timeout": printc('获取token超时,程序退出', p_type='green');sys.exit()
        #     # print(111,getToken_r)
        #     if e(getToken_r)[0]:    self.token = 'Bearer ' + getToken_r['data']['token'];  # print(self._token);#time.sleep(11000)
        #     else:   self.token = None;printc(user_id, ' token获取异常：', e(getToken_r)[1], e(getToken_r)[2])
        # else: self.token = token

    #处理openapi标记价格,从webapi这边获取
    def webposition(self,symbol):
        makrPrice= dict.makrPriceMap
        NTS=n_order(self._server,user_id=self.user_id)
        tradeType = 'linearPerpetual'
        position=NTS.position(tradeType=tradeType)['data']
        if len(position)>0:
            for i in range(0,len(position)):
                makrPrice[position[i]['symbol']]=position[i]['markPrice']
        makrPrice = makrPrice[symbol]
        return makrPrice

    #老系统线上下单
    def oldOrder(self,orderType,symbol,price,orderQty,side):
        data = { "orderType": orderType, "symbol": symbol, "price": price, "orderQty": orderQty, "side": side, }
        return requests.post('https://api.aax.com/v2/futures/orders', json=data, auth=self.auth).json()

    def palceOrder(self,params,log_level=None, com_=None):
        path = '/v3/trade/orders'
        r = req('post', self.Url + path, params=params, auth=self.auth, source='API', log_level=1)
        sample = {"message": "success", "data": {"orderId": str, "clOrdId": str, "createTime": (int, 'len', 13)},"code": self.success_code, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['单笔下单response数据类型校验:', '', ''])

    #Open Api 下单接口
    def order(self, tradeType=None, symbol=None, side=None, positionSide=None, orderType=None, reduceOnly=None,
              marginType=None, price=None, priceType=None, orderQty=None, clOrdId=None, postOnly=None, timeInForce=None,
              log_level=None, com_=None,caseParam=None):
        params = {}
        if caseParam:
            for i in caseParam: params[i]=caseParam[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if side: params['side'] = side
        if positionSide: params['positionSide'] = positionSide
        if orderType: params['orderType'] = orderType
        if reduceOnly: params['reduceOnly'] = reduceOnly
        if marginType: params['marginType'] = marginType
        if price: params['price'] = price
        if priceType: params['priceType'] = priceType
        if orderQty: params['orderQty'] = orderQty
        if clOrdId: params['clOrdId'] = clOrdId
        if postOnly: params['postOnly'] = postOnly
        if timeInForce: params['timeInForce'] = timeInForce
        path = '/v3/trade/orders'
        r = req('post', self.Url + path, params=params, auth=self.auth,source='API', log_level=log_level)
        if log_level and log_level==3: print(f"{self.source}下单结果:{r}")
        if type(r) == list:
            return r[1]
        else:
            sample = {"message": "success", "data": {"orderId": (str,'len',19), "clOrdId": str, "createTime": (int,'len',13)}, "code": self.success_code, "ts": (int,'len',13)}
            shema_result = self.shema(com_, r, sample, ['委托下单response数据类型校验:', symbol, ''],New=1)
            # if shema_result and com_:
            #     t = (
            #         [r['data']['createTime'], 13, 'createTime'], [r['data']['orderId'], 19, 'orderId'],
            #         [r['ts'], 13, 'ts'])
            #     compareLengthResult = compareLength(t, '委托下单response字段长度&数据类型校验', log_level=log_level)
            return r

    # 撤单接口
    def orderCancel(self, tradeType=None, symbol=None, orderId=None, clOrdId=None, com_=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if orderId: params['orderId'] = orderId
        if clOrdId: params['clOrdId'] = clOrdId
        path = '/v3/trade/orders/cancel'
        r = req('post', self.Url + path, params=params, auth=self.auth, log_level=log_level,source='API')
        sample = {"message": "success", "data": {"orderId": str, "clOrdId": str}, "code": self.success_code, "ts": (int,'len',13)};
        return  self.shema(com_, r, sample, ['单笔撤单response数据类型校验:', '', ''])

    # 查看当前委托接口
    def openOrders(self, tradeType=None, side=None, symbol=None, orderId=None, clOrdId=None, pageNum=None,pageSize=None, log_level=None, com_=None, *pospar, **keypar):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if side: params['side'] = side
        if symbol: params['symbol'] = symbol
        if orderId: params['orderId'] = orderId
        if clOrdId: params['clOrdId'] = clOrdId
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize
        for i in keypar:
            if not keypar[i]== None: params[i] = keypar[i]
        path = '/v3/trade/openOrders'
        self.path = self.Url_query + path;self.param = params;
        r = req('get', self.Url + path, params=params, auth=self.auth,log_level=log_level,source='API')
        self.result=r
        if log_level and log_level>=3: print(self.source+'当前委托查询结果',r)
        sample = {"message": "success", "data": {"pageNum": int, "pageSize": int, "totalSize": int, "totalPage": int,"list": [{"tradeType": str, "symbol": symbol, "positionSide": str,
                  "side": str,"marginType": str, "clOrdId": str,"createTime": (int, 'len', 13), "orderQty": str,"cumQty": str, "avgPrice": str, "lastPrice": str,"leavesQty": str, "leverage": str, "commission": str,
                  "commissionAsset": str,"orderId": str, "orderType": str, "priceType": (str, None),"price": str, "reduceOnly": False, "updateTime": int,"postOnly": False, "orderStatus": str, "timeInForce": str}]},"code": self.success_code, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['查询当前委托', '', ''],New=1)

    # 查看交易对信息
    def instruments(self, tradeType=None, symbol=None,com_=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/public/instruments'
        self.path = self.Url_query + path;self.param = params;
        r = req('get', self.Url_query + path, params,log_level=log_level,source='API')
        self.result=r
        sample = {"code": self.success_code, "message": "success", "ts": (int,'len',13), "data": [{"tradeType": str, "symbol": str, "baseAsset": str,  "base": str, "tickSize": str,"ctVal": str, "status": int,
                "onboardDate": int,"maxQty": str, "minQty": str,"maxNumOrders": str, "maxNumAlgoOrders": str, "maxRiskLimitation": str, "maxLeverage": str,"maintMarginRatio": str, "takerRate": str, "makerRate": str}]}
        return self.shema(com_, r, sample, ['查询交易对信息response数据类型校验:', '', ''])

    # 查看风险限额-与仓位挂单对应档位
    def riskLimit(self, tradeType=None, symbol=None, marginType=None,com_=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if marginType: params['marginType'] = marginType
        path = '/v3/trade/riskLimit'
        r = req('get', self.Url + path, params=params,auth=self.auth, log_level=log_level,source='API')
        sample = {"code": self.success_code, "data": [{"symbol": str, "tradeType": str, "marginType": str, "bracket": str, "initialLeverage": str,"notionalCap": str, "notionalFloor": str, "maintMarginRatio": str}],"message": "success", "ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['查询风险限额表response数据类型校验:', '', ''])

    # 划转接口
    def transfer(self, currency=None, amount=None, fromAccountType=None, toAccountType=None, com_=None,log_level=None ,*keypar):
        params = {}
        if currency: params['currency'] = currency
        if amount: params['amount'] = amount
        if fromAccountType: params['fromAccountType'] = fromAccountType
        if toAccountType: params['toAccountType'] = toAccountType
        path = '/v3/trade/account/transfer'
        r = req('post', self.Url + path, params=params, auth=self.auth, log_level=log_level,source='API')
        sample = {"code": self.success_code, "message": "success", "ts": (int,'len',13),"data": {"transId": int, "fromAccountType": str, "toAccountType": str, "currency": str,"amount": str}}
        return self.shema(com_, r, sample, ['划转保证金response数据类型校验:', '', ''])

    # 合约历史订单查询(历史委托)
    def hisOrders(self, tradeType=None, symbol=None, side=None, orderId=None, clOrdId=None, orderStatus=None,
                  orderType=None, pageNum=None, pageSize=None, startTime=None, endTime=None, log_level=None, com_=None,source=None,marginType=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if side: params['side'] = side
        if marginType: params['marginType'] = marginType
        if orderId: params['orderId'] = orderId
        if clOrdId: params['clOrdId'] = clOrdId
        if orderStatus: params['orderStatus'] = orderStatus
        if orderType: params['orderType'] = orderType
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize
        if startTime: params['startTime'] = startTime
        if endTime: params['endTime'] = endTime

        path = '/v3/trade/record/orders/history';self.path = self.Url_query + path;self.param = params;
        r = req('get', self.Url_query + path, params=params, auth=self.auth, log_level=log_level,source='API');self.result=r;
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13),"data": {"pageNum": int, "pageSize": int, "totalSize": int, "totalPage": int, "list": [
                 {"tradeType": str, "symbol": str, "side": str, "positionSide": str, "marginType": str,"clOrdId": str, "orderId": str, "createTime": (int, 'len', 13), "avgPrice": str,
                 "lastPrice": str, "leverage": str, "orderQty": str, "filledQty": str, "cumQty": str,"realProfit": str,"orderType": str, "priceType": (str, None), "price": str, "reduceOnly": True,
                 "updateTime": (int, 'len', 13), "postOnly": True, "orderStatus": str, "timeInForce": str}]}}
        return self.shema(com_, r, sample, ['查询历史委托response数据类型校验:', '', ''])

    # 查看合约订单成交详情(历史成交记录)
    def hisTrades(self, tradeType=None, symbol=None, side=None, orderId=None, clOrdId=None, tradeId=None,startTime=None, endTime=None, pageNum=None,orderType=None,orderStatus=None, pageSize=None, com_=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if side: params['side'] = side
        if orderId: params['orderId'] = orderId
        if clOrdId: params['clOrdId'] = clOrdId
        if tradeId: params['tradeId'] = tradeId
        if orderType:params['orderType'] = orderType
        if orderStatus: params['orderStatus'] = orderStatus
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize
        if startTime: params['startTime'] = startTime
        if endTime: params['endTime'] = endTime
        if 'orderType' in params.keys():
            del params['orderType']
        source = source
        path = '/v3/trade/record/orders/fills'
        r = req('get', self.Url_query + path, params=params, auth=self.auth, log_level=log_level,source='API')
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13), "data": {"list": [
            {"tradeType": str, "positionSide": str, "side": str, "symbol": str, "marginType": str,"commissionAsset": str, "filledQty": str, "commission": str, "orderId": str, "clOrdId": str,
             "createTime": (int, 'len', 13), "tradeId": str, "realProfit": str, "taker": True,"updateTime": (int, 'len', 13)}], "pageNum": int, "pageSize": int, "totalPage": int, "totalSize": int}}
        return self.shema(com_, r, sample, ['查询成交response数据类型校验:', '', ''])

    # 获取合约账户流水
    def hisAccounts(self, tradeType=None, symbol=None, incomeType=None, startTime=None, endTime=None, pageNum=None,pageSize=None, log_level=None, com_=None, **keypar):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if incomeType: params['incomeType'] = incomeType
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize
        if startTime: params['startTime'] = startTime
        if endTime: params['endTime'] = endTime
        path = '/v3/trade/record/account/income'
        r = req('get', self.Url_query + path, params=params, auth=self.auth,source='API', log_level=log_level)
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13), "data": {"list": [{"tradeType": str, "symbol": str, "incomeType": str, "income": str, "details": (int,None), "currency": str,
             'createTime': (int, 'len', 13), }], "pageNum": int, "pageSize": int, "totalPage": int, "totalSize": int}}
        return self.shema(com_, r, sample, ['查询流水response数据类型校验:', '', ''])

    # 获取用户手续费率
    def commissionRate(self, tradeType=None, symbol=None,log_level=None,com_=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/trade/commissionRate'
        r = req('get', self.Url_query + path, params=params, auth=self.auth,source='API', log_level=log_level)
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13),"data": [{"tradeType": str, "symbol": str, "makerRate": str, "takerRate": str, }]}
        return self.shema(com_, r, sample, ['查询用户手续费率response数据类型校验:', '', ''])

    # Open api批量下单
    def batchOrders(self,data=None,log_level=None,source=None,com_=None,**keypar):
        params = {}
        if data: params['data'] = data
        for i in keypar:
            if not keypar[i] == None:params[i]=keypar[i]
        path = '/v3/trade/batchOrders'
        r = req('post', self.Url + path, params=params, auth=self.auth, source='API', log_level=log_level)
        if log_level and log_level == 3: print('批量下单 结果:', r)
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13),"data": [{"orderId": str, "clOrdId": str,"createTime": int},]}
        return self.shema(com_, r, sample, ['批量下单response数据类型校验:', '', ''])

    # Open api批量撤单
    def batchCancelOrders(self,data=None,log_level=None,source=None,com_=None,**keypar):
        params = {}
        if data: params['data'] = data
        for i in keypar:
            if not keypar[i] == None:params[i]=keypar[i]
        path = '/v3/trade/orders/batchCancelOrders'
        r = req('post', self.Url + path, params=params, auth=self.auth, source='API', log_level=log_level)
        if log_level and log_level == 3: print('批量撤单 结果:', r)
        sample = {"code": self.success_code, "message": "success", "ts": (int, 'len', 13),"data":{"successList":list,"errorList":list}}
        return self.shema(com_, r, sample, ['批量撤单response数据类型校验:', '', ''])

    # 增加、减少逐仓保证金
    def adjustmentMargin(self, tradeType=None, symbol=None, positionSide=None, amount=None, type=None, log_level=None,com_=None, **keypar):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if positionSide: params['positionSide'] = positionSide
        if amount: params['amount'] = amount
        if type: params['type'] = type  # 调整方向 1: 增加逐仓保证金，2: 减少逐仓保证金
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        path = '/v3/trade/position/margin'
        r = req('post', self.Url + path, params=params, auth=self.auth, source='API', log_level=log_level)
        if log_level and log_level == 3: print('保证金调整 结果:', r)
        sample = {"message": "success", "code": self.success_code, "ts": (int, 13), "data":
            {"symbol": str, "tradeType": str, "amount": str, "type": int, "currency": str}}
        return self.shema(com_, r, sample, ['保证金调整response数据类型校验:', '', ''], New=1)

    # 计划委托下单
    def triggerOrder(self, tradeType=None, symbol=None, side=None, positionSide=None, marginType=None, orderType=None,
                     priceType=None, price=None, orderQty=None,
                     reduceOnly=None, postOnly=None, tpTriggerPx=None, slTriggerPx=None, triggerPx=None,
                     tpTriggerPxType=None, slTriggerPxType=None
                     , triggerPxType=None, clOrdId=None, timeInForce=None, log_level=None,com_=None,caseParam=None):
        params = {}
        if caseParam:
            for i in caseParam: params[i]=caseParam[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if positionSide: params['positionSide'] = positionSide
        if side: params['side'] = side
        if marginType: params['marginType'] = marginType
        if orderType: params['orderType'] = orderType
        if priceType: params['priceType'] = priceType
        if price: params['price'] = price
        if orderQty: params['orderQty'] = orderQty
        if reduceOnly: params['reduceOnly'] = reduceOnly
        if postOnly: params['postOnly'] = postOnly
        if tpTriggerPx: params['tpTriggerPx'] = tpTriggerPx
        if slTriggerPx: params['slTriggerPx'] = slTriggerPx
        if triggerPx: params['triggerPx'] = triggerPx
        if tpTriggerPxType: params['tpTriggerPxType'] = tpTriggerPxType
        if slTriggerPxType: params['slTriggerPxType'] = slTriggerPxType
        if triggerPxType: params['triggerPxType'] = triggerPxType
        if clOrdId: params['clOrdId'] = clOrdId
        if timeInForce: params['timeInForce'] = timeInForce

        path = '/v3/trade/stopOrders'
        self.path = self.Url_query + path;self.param = params;
        r = req('post', self.Url + path, params=params, auth=self.auth,source='API', log_level=log_level)
        r={"code": '1',"data": {"clOrdId": "aax_trade","stopOrderId": "1234567890123456789","createTime":1573541338074},"message": "success","ts": 1573541338074}
        self.result=r
        if log_level and log_level>=3: print(f'{self.source}计划委托下单请求结果',r)
        sample = {"message": "success", "data": {"stopOrderId": (str, 'len', 19), "createTime": (int, 'len', 13)},"code": "1", "ts": (int, 13)}
        shema_result = self.shema(com_, r, sample, ['委托下单response数据类型校验:', symbol, ''], New=1)
        return shema_result

    # 撤销计划委托单
    def CancelTriggerOrder(self, tradeType=None, symbol=None, stopOrderId=None, clOrdId=None, log_level=None,com_=None,caseParam=None):
        params = {}
        if caseParam:
            for i in caseParam: params[i]=caseParam[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if stopOrderId: params['stopOrderId'] = stopOrderId
        if clOrdId: params['clOrdId'] = clOrdId
        path = '/v3/trade/stopOrders/cancel'
        self.path = self.Url_query + path;self.param = params;
        r = req('delete', self.Url + path, params=params, auth=self.auth, log_level=log_level)
        r = {"code": "1", "message": "success", "ts": 1234567890123,"data": [{"clOrdId": "str", "stopOrderId": "str", "sMsg": "str"}]}
        self.result = r
        if log_level and log_level >= 3: print(f'{self.source}撤销计划委托 请求结果', r)
        sample = {"code": "1", "message": "success", "ts": (int, 13),"data": [{"clOrdId": str, "stopOrderId": str, "sMsg": str}]}
        shema_result = self.shema(com_, r, sample, ['撤销计划委托response数据类型校验:', symbol, ''], New=1)
        return shema_result

    # 查询计划委托单
    def OpenTriggerOrder(self, tradeType=None, symbol=None, marginType=None, orderType=None, priceType=None,
                         stopOrderId=None, clOrdId=None, pageNum=None, pageSize=None, log_level=None,com_=None,caseParam=None):
        params = {}
        if caseParam:
            for i in caseParam: params[i]=caseParam[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if marginType: params['marginType'] = marginType
        if orderType: params['orderType'] = orderType
        if priceType: params['priceType'] = priceType
        if stopOrderId: params['stopOrderId'] = stopOrderId
        if clOrdId: params['clOrdId'] = clOrdId
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize
        path = '/v3/trade/stopOrders/search'
        self.path=self.Url_query + path;self.param=params;
        r = req('get', self.Url + path, params=params, auth=self.auth,source='API', log_level=log_level)
        r = {"code":'1',"data":{"list":[{"symbol":"str","tradeType":"str","positionSide":"str","side":"str","marginType":"str","stopOrderId":"str","clOrdId":"str","createTime":1234567890123,"leverage":"str","orderType":"str","stopOrderType":"str","priceType":"str","price":"str","orderQty":"str","reduceOnly":"str","postOnly":"str","triggerPxType":"str","tpTriggerPx":"str","tpTriggerPxType":"str","tpOrdPx":"str","slTriggerPx":"str","slTriggerPxType":"str","slOrdPx":"str","triggerPx":"str","triggerPxType":"str","ordPx":"str"}],"pageNum":1,"pageSize":1,"totalPage":1,"totalSize":1},"message":'success',"ts":1234567890123}
        self.result = r
        if log_level and log_level>=3: print(f'{self.source}计划委托下单请求结果',r)
        sample = {"code":'1',"data":{"list":[{"symbol":str,"tradeType":str,"positionSide":str,"side":str,"marginType":str,"stopOrderId":str,"clOrdId":str,"createTime":int,"leverage":str,"orderType":str,"stopOrderType":str,"priceType":str,"price":str,"orderQty":str,"reduceOnly":str,"postOnly":str,"triggerPxType":str,"tpTriggerPx":str,"tpTriggerPxType":str,"tpOrdPx":str,"slTriggerPx":str,"slTriggerPxType":str,"slOrdPx":str,"triggerPx":str,"triggerPxType":str,"ordPx":str}],"pageNum":int,"pageSize":int,"totalPage":int,"totalSize":int},"message":'success',"ts":(int, 13)}
        shema_result = self.shema(com_, r, sample, ['计划委托下单response数据类型校验:', symbol, ''], New=1)
        return shema_result

    # 获取历史计划委托单列表
    def TriggerOrdersHistory(self, tradeType=None, symbol=None, marginType=None, orderType=None, priceType=None,
                          pageNum=None, pageSize=None,
                          stopOrderId=None, clOrdId=None, startTime=None, endTime=None, log_level=None,com_=None,caseParam=None):

        params = {}
        if caseParam:
            for i in caseParam: params[i]=caseParam[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if marginType: params['marginType'] = marginType
        if orderType: params['orderType'] = orderType
        if pageNum: params['pageNum'] = pageNum
        if pageSize: params['pageSize'] = pageSize

        if stopOrderId: params['stopOrderId'] = stopOrderId
        if clOrdId: params['clOrdId'] = clOrdId
        if startTime: params['startTime'] = startTime
        if endTime: params['endTime'] = endTime

        path = '/v3/trade/record/stopOrdersHistory'
        self.path = self.Url_query + path;self.param = params;
        r = req('get', self.Url_query + path, params=params, auth=self.auth, source='API',log_level=log_level)
        r = {"code":'1',"data":{"list":[{"symbol":"str","tradeType":"str","positionSide":"str","side":"str","marginType":"str","stopOrderId":"str","clOrdId":"str","createTime":1234567890123,"leverage":"str","orderType":"str","stopOrderType":"str","priceType":"str","price":"str","orderQty":"str","reduceOnly":"str","postOnly":"str","triggerPxType":"str","tpTriggerPx":"str","tpTriggerPxType":"str","tpOrdPx":"str","slTriggerPx":"str","slTriggerPxType":"str","slOrdPx":"str","triggerPx":"str","triggerPxType":"str","ordPx":"str"}],"pageNum":1,"pageSize":1,"totalPage":1,"totalSize":1},"message":'success',"ts":1234567890123}
        self.result = r
        if log_level and log_level>=3: print(f'{self.source}历史委托-计划委托查询 请求结果',r)
        sample = {"code":'1',"data":{"list":[{"symbol":str,"tradeType":str,"positionSide":str,"side":str,"marginType":str,"stopOrderId":str,"clOrdId":str,"createTime":int,"leverage":str,"orderType":str,"stopOrderType":str,"priceType":str,"price":str,"orderQty":str,"reduceOnly":str,"postOnly":str,"triggerPxType":str,"tpTriggerPx":str,"tpTriggerPxType":str,"tpOrdPx":str,"slTriggerPx":str,"slTriggerPxType":str,"slOrdPx":str,"triggerPx":str,"triggerPxType":str,"ordPx":str}],"pageNum":int,"pageSize":int,"totalPage":int,"totalSize":int},"message":'success',"ts":(int, 13)}
        shema_result = self.shema(com_, r, sample, ['历史委托-计划委托查询response数据类型校验:', symbol, ''], New=1)
        return shema_result

    # 老系统 https://api.aax.com/v2/instruments
    def v2_instruments(self, tradeType=None, symbol=None, log_level=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        Url = 'https://api.aax.com/v2/instruments'
        return req('get', Url, params, self.token, log_level=log_level)

    # 查询当前标记价格
    def markPrice(self, tradeType=None, symbol=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/market/markPrice'
        return req('get', self.Url_query + path, params=params, auth=self.auth,source='API', log_level=log_level)

    # 获取深度数据
    def orderBook(self, tradeType=None, symbol=None, level=None, log_level=None,source=None):
        params = {}
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if level: params['level'] = level
        path = '/v3/market/orderBook'
        return req('get', self.Url + path, params=params, auth=self.auth,source='API', log_level=log_level)

    # 交易账户
    def balances(self, currency=None, log_level=None, com_=None,source=None,**keypar):
        params = {}
        if currency: params['currency'] = currency
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        path = '/v3/trade/tradingAccount'
        r = req('get', self.Url + path, params=params, auth=self.auth,source='API',  log_level=log_level)
        sample = {"code": self.success_code, "data": [{ "currency": str, "marginEquity": str, "profitUnreal": str, "marginFrozen": str, "marginPosition": str, "marginAvailable": str, "maxWithdrawAmount": str }], "message": "success", "ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['交易账户response数据类型校验:', '', ''])

    # openAPI查看持仓信息
    def position(self, log_level=None,com_=None,**keypar):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        path = '/v3/trade/position';self.path = self.Url_query + path;self.params = params;
        r = req('get', self.Url + path, params, auth=self.auth,source='API', log_level=log_level);self.result=r;
        if log_level and log_level>=3: print(self.source+'持仓查询结果:',r)
        sample = { "code": self.success_code, "data": [{ "tradeType": str, "positionSide": str, "symbol": str, "marginType": str, "avgEntryPrice": str, "positionStatus": str, "positionAmt": str, "positionMargin": str,
                "leverage": str,'availPos':str, "liquidationPrice": str, "openTime": (int,'len',13), "realProfit": str, "unrealisedPnl": str,'insuranceLevel':int,'maintMarginRatio':str}], "message": "success", "ts": (int,'len',13) }
        return self.shema(com_, r, sample, ['持仓信息response数据类型校验:', '', ''])

    # openAPI端 查询历史完全平仓记录
    def position_closed(self, log_level=None, com_=None, **keypar):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        path = '/v3/trade/record/position/closed';self.path = self.Url_query + path;self.params = params;
        r = req('get', self.Url_query + path, params, auth=self.auth,source='API', log_level=log_level);self.result=r;
        if log_level and log_level >= 3: print(self.source + '历史完全平仓记录查询结果:', r)
        sample = { "code": self.success_code, "data": { "list": [ { "tradeType": str, "symbol": str, "exitType": int, "marginType": str, "avgEntryPrice": str,
                   "avgExitPrice": str, "positionStatus": str, "positionQty": str, "leverage": str, "commission": str, "realProfit": str,
                   "updateTime": (int,'len',13) } ], "pageNum": int, "pageSize": int, "totalSize": int, "totalPage": int, }, "message": "success", "ts": (int,'len',13) }
        return self.shema(com_, r, sample, ['历史完全平仓记录查询response数据类型校验:', '', ''])

    #查看当前杠杆
    def leverage_info(self,tradeType=None,symbol=None,marginType=None,log_level=None,com_=None,source=None,keypar=None):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        if marginType: params['marginType'] = marginType
        path='/v3/trade/leverage/info';self.path = self.Url + path;self.param = params;
        r = req('get', self.Url + path, params=params, auth=self.auth, source='API', log_level=log_level);self.result=r;
        if log_level and log_level >= 3: print(self.source + '当前杠杆查询结果:', r)
        sample ={"code": self.success_code, "message": "success", "data": [{"tradeType": str, "symbol": str, "leverage": str, "marginType": str}],"ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['当前杠杆response数据类型校验:', '', ''])

    #切换杠杆
    def changeleverage(self,tradeType=None,symbol=None,leverage=None,marginType=None,log_level=None, com_=None, **keypar):
        params = {'tradeType':tradeType,'symbol':symbol,'leverage':leverage,'marginType':marginType}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        path='/v3/trade/leverage';self.path = self.Url_query + path;self.params = params;
        r =  req('post', self.Url + path, params, auth=self.auth, source='API', log_level=log_level);self.result=r;
        if log_level and log_level>=3 : print('切换杠杆请求结果',r)
        sample ={ "code": self.success_code, "message": "success", "data": { "tradeType": str, "symbol": str, "leverage": str, "marginType": str }, "ts": (int,'len',13) }
        return self.shema(com_, r, sample, ['切换杠杆response数据类型校验:', '', ''])

    # 获取上期资金结算记录
    def prevFundingRate(self, tradeType=None, symbol=None, log_level=None, com_=None, **keypar):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/public/trade/funding/prevFundingRate';self.path = self.Url + path;self.params = params;
        r = req('get', self.Url + path, params, auth=self.auth, source='API', log_level=log_level);self.result = r;
        if log_level and log_level >= 3: print('获取上期资金结算记录结果', r)
        sample = {"code": self.success_code, "message": "success","ts": (int, 'len', 13),
                  "data": {"tradeType": str, "symbol": str, "fundingRate":(None,str), "fundingTime":(None,int)}}
        return self.shema(com_, r, sample, ['获取上期资金结算记录response数据类型校验:', '', ''])

    # 获取预期资金费结算数据
    def predictedFunding(self, tradeType=None, symbol=None, log_level=None, com_=None, **keypar):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/public/trade/funding/predictedFunding';self.path = self.Url + path;self.params = params;
        r = req('get', self.Url + path, params, auth=self.auth, source='API', log_level=log_level);self.result = r;
        if log_level and log_level >= 3: print('获取预期资金费结算数据结果', r)
        sample = {"code": self.success_code, "message": "success","ts": (int, 'len', 13),
                  "data": {"tradeType": str, "symbol": str, "predictedFundingRate": str, "nextFundingTime":(0,int)}}
        return self.shema(com_, r, sample, ['获取预期资金费结算数据response数据类型校验:', '', ''])

    # 获取资金费率记录
    def fundingRate(self, tradeType=None, symbol=None, log_level=None, com_=None, **keypar):
        params = {}
        for i in keypar:
            if not keypar[i] == None: params[i] = keypar[i]
        if tradeType: params['tradeType'] = tradeType
        if symbol: params['symbol'] = symbol
        path = '/v3/public/trade/funding/fundingRate';self.path = self.Url + path;self.params = params;
        r = req('get', self.Url + path, params, auth=self.auth, source='API', log_level=log_level);self.result = r;
        if log_level and log_level >= 3: print('获取资金费率记录结果', r)
        sample = {"code": self.success_code, "message": "success","ts": (int, 'len', 13),
                  "data": {"tradeType": str, "symbol": str, "fundingRate": str, "fundingTime":(0,int)}}
        return self.shema(com_, r, sample, ['获取资金费率记录response数据类型校验:', '', ''])

    def getToken(self,user_id):
        orderName = '/comm/v2/user/getToken';
        param = 'userId='+str(user_id)
        return req('get', self.Url + orderName, param);

    def shema(self, com_, r, sample, title,New=None):
        if com_:
            com_r = com(sample, r, [title[0] + title[1], ' 返参异常:', '', ''],New=New);
            if not com_r:
                return False  # u(0);
            else:
                return r  # u(1);
        else:
            return r

    def muLanOrderBook(self,symbolId,log_level=None):
        params = {}
        if symbolId: params['symbolId'] = symbolId
        url='https://qamock.cn.atomintl.com/md_mock/orderbook'
        url='https://qamock.cn.atomintl.com/md_mock/orderbook?symbolId=7'
        r= req('get', url, params='', log_level=log_level)
        print(url,params)
        # r=requests.get(url,params='')
        print(r)
        return r

if __name__ == '__main__':
     b = NtsApiOrder('5', user_id='10070')
     # b = NtsApiOrder('6', user_id='97201974')
     # b = NtsApiOrder('7', user_id='99999')
    ##下单
     # print(b.order(tradeType='linearPerpetual',symbol="ETHUSDT",side="buy",positionSide="long",orderType="limit",marginType='cross',price=1200,priceType="marketPrice",orderQty=88,postOnly=False,timeInForce="GTC"))
    ##查当前委托
     # print(b.openOrders())
    ##划转
     # print(b.transfer(currency='USDT',amount='1.123',fromAccountType='Futures',toAccountType='funding'))
    ##查资金
     # print(b.tradingAccount(currency='usdt'))
    ##撤单
     # print(b.cancelOrder(tradeType='linearPerpetual',symbol='btcusdt',clOrdId='111222'))
    ##查看当前杠杆
    # print(b.leverageInfo(tradeType='linearPerpetual',symbol='btcusdt'))
    ##切换杠杆
    # print(b.changeleverage(tradeType='linearPerpetual',symbol='btcusdt',marginType='cross',leverage='15'))
    ##历史成交
     # print(b.ordersFills(tradeType='linearPerpetual',symbol='btcusdt',side='buy',pageSize=100))
    ##获取合约流水
     # print(b.accountIncome(tradeType='linearPerpetual',symbol='btcusdt',startTime=1664112611,endTime=1664199011))
     ## 查看仓位
     # print(b.position(tradeType='linearPerpetual',symbol='btcusdt'))
     #历史委托
     # print(b.hisOrders(symbol='BTCUSDT',side='buy',orderId='1031976043679875072'))
    #查看风险限额
     # print(b.riskLimit(tradeType='linearPerpetual',symbol='btcusdt',marginType='cross'))

     pass
