import sys,datetime, os
from config.urlConfig import orderUrls,defaultUserIdList
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import config.urlConfig as urlConfig
from common.util import request_http as req, printc, countCaseNumber as u
from common.asserts import compare as com
from common.other import httpCheck as e
from param.code_list import code_list as code
from param import dict

class n_order:
    global contract_code_date, contract_code_short,_token
    def __init__(self,server,product=None,user_id=None,token=None):
        global _token
        self.source='web'
        self._server=server;self.server=server;self.user_id=str(user_id)
        if not user_id: user_id=defaultUserIdList[int(server)][0]
        self.Url=orderUrls[str(server)][0]
        self.Url_query = orderUrls[str(server)][1]
        self.success_code = code["success"][0]
        if not token:
            getToken_r = self.getToken(self.user_id)
            if getToken_r == "timeout": printc('获取token超时,程序退出', p_type='green');sys.exit()
            if e(getToken_r)[0]:    self.token = 'Bearer ' + getToken_r['data']['token'];  # print(self._token);#time.sleep(11000)
            else:   self.token = None;printc(user_id, ' token获取异常：', e(getToken_r)[1], e(getToken_r)[2])
        else: self.token=token
        self.instrument={}
        self.instrumentList=[]
        instruments_r = self.instruments(log_level=0)

        if e(instruments_r)[0]:
            for dict in instruments_r['data']:
                self.instrument[dict['symbol'][:-4]]=[dict['tickSize'],dict['ctVal'],dict['takerRate'] ,dict['makerRate']]
                self.instrumentList.append(dict['symbol'])
        else: printc("合约信息接口异常:",instruments_r);#sys.exit()

    def index(self,symbol,log_level=None,beauty=True,com_=None):
        if beauty:
            symbol=symbol.upper()
            if 'USD'  not in symbol : symbol=symbol+'USDTFP'
        path='/index/v1/mark/'+symbol;
        r = req('get', self.Url + path, '', self.token, log_level=log_level)
        sample={'code': '1', 'data': {'symbol': {symbol}, 'tradeType': 'linearPerpetual', 'index': float, 'mark': float, 'market': float, 'time': 1661855204, 'scale': int, 'options': None, 'quotes': None, 'fundingRate': float, 'fundingHours': float, 'fundingRateLimit': float, 'nextFundingTime': 1661875200000}, 'message': 'success', 'timestamp': str}
        if com_:
            com_r=com(sample,r,['index接口 '+symbol,' 返参异常:','',''])
            if not com_r: return com_r
        return r

    # web_api 下单  0.3版本兼容 下单
    def order(self, tradeType=None, symbol=None, source=None, positionSide=None, orderType=None, marginType=None, side=None, price=None, priceType=None, orderQty=None, clOrdId=None, postOnly=None, reduceOnly=None, timeInForce=None, tpTriggerPx=None, slTriggerPx=None, triggerPx=None, tpTriggerPxType=None, slTriggerPxType=None, triggerPxType=None, log_level=None, com_=None, beautiful=None,caseParam=None):
        param={};shema_result=True
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]

        if beautiful:  param['tradeType']='linearPerpetual';param['marginType']='cross';param['marginType']='cross';param['orderType']='limit';param['orderQty']=1
        if tradeType: param['tradeType']=tradeType
        if symbol: param['symbol'] = symbol
        if positionSide: param['positionSide'] = positionSide
        if marginType: param['marginType'] = marginType
        if orderType: param['orderType'] = orderType
        if tradeType: param['tradeType'] = tradeType
        if tradeType: param['tradeType'] = tradeType
        if positionSide: param['positionSide'] = positionSide
        if orderType: param['orderType'] = orderType
        if side: param['side'] = side
        if price: param['price'] = price
        if priceType: param['priceType'] = priceType
        if orderQty: param['orderQty'] = orderQty
        if clOrdId: param['clOrdId'] = clOrdId
        if postOnly: param['postOnly'] = postOnly
        if reduceOnly: param['reduceOnly'] = reduceOnly
        if timeInForce: param['timeInForce'] = timeInForce
        if tpTriggerPx: param['tpTriggerPx'] = tpTriggerPx
        if slTriggerPx: param['slTriggerPx'] = slTriggerPx
        if triggerPx: param['triggerPx'] = triggerPx
        if tpTriggerPxType: param['tpTriggerPxType'] = tpTriggerPxType
        if slTriggerPxType: param['slTriggerPxType'] = slTriggerPxType
        if triggerPxType: param['triggerPxType'] = triggerPxType

        path='/v3/trade/web/orders';
        if source=='API': path='/v3/trade/orders'
        r = req('post', self.Url + path,param, self.token, log_level=log_level,source=source)
        if log_level and log_level>=3: print(f'{self.source}下单结果:',r)
        # r={"message": "success","data": {"orderId": str,"createTime": (int,'len',13)},"code": "1","ts": int}
        if type(r)==list: printc(r[1]);return r[1]
        else:
            sample = {"message": "success","data": {"orderId": (str,'len',19),"createTime": (int,'len',13)},"code": "1","ts": (int,13)}
            shema_result=self.shema(com_, r, sample, ['委托下单response数据类型校验:', symbol, ''],New=1)
            # if shema_result  and com_:
            #     t = ([r['data']['createTime'], 13, 'createTime'], [r['data']['orderId'], 19, 'orderId'], [r['ts'], 13, 'ts'])
            #     compareLengthResult=compareLength(t,'委托下单response字段长度&数据类型校验',log_level=log_level)
            return shema_result

    # web_api 普通委托撤单
    def orderCancel(self,tradeType=None,symbol=None,orderId=None,log_level=None,com_=None, **keypar):
        param = {}
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        if orderId: param['orderId'] = orderId
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/web/orders/cancel'
        r = req('post', self.Url + path, param, self.token, log_level=log_level)
        if log_level and log_level == 3: print(f'{self.source}单笔撤单 结果:', r)
        sample = {"message": "success","data": {"orderId": str},"code": self.success_code,"ts": (int,13)}
        return self.shema(com_, r, sample, ['单笔撤单response数据类型校验:', '', ''])

    # web_api 一键平仓
    def oneClickClose(self,tradeType=None,symbol=None,log_level=None,com_=None,**keypar):
        param = {}
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/web/oneClickClose'
        r = req('post', self.Url + path, param, self.token, log_level=log_level)
        if log_level and log_level == 3: print(f'{self.source}一键平仓 结果:', r)
        sample = {"message": "success","code": self.success_code,"ts": (int,13),"data":list}
        return self.shema(com_, r, sample, ['一键平仓response数据类型校验:', '', ''],New=1)

    # web_api 一键撤单(普通单)
    def oneClickCancel(self,tradeType=None,symbol=None,log_level=None,com_=None, **keypar):
        param = {}
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/web/orders/oneClickCancel'
        r = req('post', self.Url + path, param, self.token, log_level=log_level)
        if log_level and log_level == 3: print(f'{self.source}一键撤单(普通单) 结果:', r)
        sample = {"message": "success","code": self.success_code,"ts": (int,13)}
        return self.shema(com_, r, sample, ['一键撤单(普通单)response数据类型校验:', '', ''],New=1)

    # web_api 一键撤单(条件单)
    def oneClickCancelTriggerOrders(self,tradeType=None,symbol=None,stopOrderId=None,log_level=None,com_=None, **keypar):
        param = {}
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        if stopOrderId: param['stopOrderId'] = stopOrderId
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/web/stopOrders/cancel'
        r = req('post', self.Url + path, param, self.token, log_level=log_level)
        if log_level and log_level == 3: print(f'{self.source}一键撤单(条件单) 结果:', r)
        sample = {"message": "success","code": self.success_code,"ts": (int,13)}
        return self.shema(com_, r, sample, ['一键撤单(条件单)response数据类型校验:', '', ''],New=1)

    # web_api 增加、减少逐仓保证金
    def adjustmentMargin(self,tradeType=None,symbol=None,positionSide=None,amount=None,type=None,log_level=None,com_=None,**keypar):
        param = {}
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        if positionSide: param['positionSide'] = positionSide
        if amount: param['amount'] = amount
        if type: param['type'] = type # 调整方向 1: 增加逐仓保证金，2: 减少逐仓保证金
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/web/position/margin'
        r = req('post', self.Url + path, param, self.token, log_level=log_level)
        if log_level and log_level == 3: print(f'{self.source}保证金调整 结果:', r)
        sample = {"message": "success","code": self.success_code,"ts": (int,13),"data":
            {"symbol": str, "tradeType": str, "amount": str, "type": int, "currency": str}}
        return self.shema(com_, r, sample, ['保证金调整response数据类型校验:', '', ''],New=1)

    # web_api 查询当前委托
    def openOrders(self,tradeType=None,symbol=None,log_level=None,com_=None,source=None, **keypar):
        path='/v3/trade/web/openOrders'
        if source == 'API': path='/v3/trade/openOrders';
        param = {}
        if tradeType: param['tradeType']=tradeType
        if symbol: param['symbol'] = symbol
        for i in keypar:
            if not keypar[i] == None:   param[i]=keypar[i]
        self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path,param, self.token, log_level=log_level,source=source);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询当前委托 结果:',r)
        sample = {"message": "success","data": {"pageNum": int,"pageSize": int,"totalSize": int,"totalPage": int,"list": [{"tradeType": str,"symbol":symbol,"positionSide": str,"side": str,
                "marginType": str,"clOrdId": str,"createTime": (int,'len',13),"orderQty": str,"cumQty": str,"avgPrice": str,"lastPrice": str,"leavesQty": str,"leverage":str,"commission": str,"commissionAsset": str,
                "orderId": str,"orderType": str,"priceType": (str,None),"price": str,"reduceOnly": False,"updateTime": int,"postOnly": False,"orderStatus": str,"timeInForce": str}]},"code": self.success_code,"ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['查询当前委托', '', ''],New=1)

    # web_api 查询历史订单
    def hisOrders(self,log_level=None,com_=None,**keypar):
        param = {}
        for i in keypar:
            if not keypar[i]==None: param[i]=keypar[i]
        path = '/v3/trade/record/web/orders/history';self.path = self.Url_query + path;self.param = param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3 : print(f'{self.source}查询历史订单 结果:',r)
        sample = {"code": self.success_code,"message": "success","ts": (int,'len',13),"data": {"pageNum": int, "pageSize": int, "totalSize": int, "totalPage": int,"list": [{"tradeType": str,"symbol": str,"side": str,"positionSide": str,"marginType":str,
                    "clOrdId":str,"orderId": str,"createTime": (int,'len',13),"avgPrice": str,"lastPrice": str,"leverage": str,"orderQty": str,"filledQty": str,"cumQty": str,"realProfit": str,
                    "orderType": str,"priceType": (str,None),"price": str,"reduceOnly": True,"updateTime": (int,'len',13),"postOnly": True,"orderStatus": str,"timeInForce": str}]}}
        return self.shema(com_, r, sample, ['查询历史委托response数据类型校验:', '', ''],New=1)

    # web_api 查询历史成交
    def hisTrades(self,log_level=None,com_=None,**keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None:param[i]=keypar[i]
        path = '/v3/trade/record/web/orders/fills'
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level)
        sample={"code": self.success_code,"message": "success","ts": (int,'len',13),"data": {"list": [{"tradeType": str,"positionSide": str,"side": str,"symbol": str,"marginType": str,"commissionAsset": str,"filledQty": str,"commission": str,"orderId": str,"clOrdId": str,"createTime": (int,'len',13),
                "tradeId": str,"realProfit": str,"taker": True,"updateTime": (int,'len',13)}],"pageNum": int,"pageSize": int,"totalPage": int,"totalSize": int}}
        if log_level and log_level == 3:print(f'{self.source}查询历史成交 结果:',r)
        return self.shema(com_, r, sample, ['查询成交response数据类型校验:', '', ''],New=1)

    # web_api 计划委托下单
    def triggerOrder(self,symbol=None,log_level=None,com_=None,caseParam=None,**keypar):
        param = {}
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        if symbol: param['symbol']=symbol
        path = '/v3/trade/web/stopOrders'
        self.path=self.Url_query + path;self.param=param;
        r = req('post', self.Url_query + path, param, self.token, log_level=log_level)
        # r={"code": '1',"data": {"clOrdId": "aax_trade","stopOrderId": "1234567890123456789","createTime":1573541338074},"message": "success","ts": 1573541338074}
        self.result = r
        if log_level and log_level == 3: print(f'{self.source}计划委托下单 结果',r)
        sample = {"message": "success", "data": {"stopOrderId": (str, 'len', 19), "createTime": (int, 'len', 13)},"code": "1", "ts": (int, 13)}
        return self.shema(com_, r, sample, ['计划委托下单response数据类型校验:', symbol, ''], New=1)

    # web_api 查询未触发的计划委托
    def OpenTriggerOrder(self,symbol=None,log_level=None,com_=None,caseParam=None,**keypar):
        param = {}
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        if symbol: param['symbol']=symbol
        path = '/v3/trade/web/stopOrders/search'
        self.path=self.Url_query + path;self.param=param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level)
        # r = {"code":'1',"data":{"list":[{"symbol":"str","tradeType":"str","positionSide":"str","side":"str","marginType":"str","stopOrderId":"str","clOrdId":"str","createTime":1234567890123,"leverage":"str","orderType":"str","stopOrderType":"str","priceType":"str","price":"str","orderQty":"str","reduceOnly":"str","postOnly":"str","triggerPxType":"str","tpTriggerPx":"str","tpTriggerPxType":"str","tpOrdPx":"str","slTriggerPx":"str","slTriggerPxType":"str","slOrdPx":"str","triggerPx":"str","triggerPxType":"str","ordPx":"str"}],"pageNum":1,"pageSize":1,"totalPage":1,"totalSize":1},"message":'success',"ts":1234567890123}
        self.result = r
        if log_level and log_level == 3: print(f'{self.source}查询未触发的计划委托 结果',r)
        sample = {"code":'1',"data":{"list":[{"symbol":str,"tradeType":str,"positionSide":str,"side":str,"marginType":str,"stopOrderId":str,"clOrdId":str,"createTime":int,"leverage":str,"orderType":str,"stopOrderType":str,"priceType":str,"price":str,"orderQty":str,"reduceOnly":str,"postOnly":str,"triggerPxType":str,"tpTriggerPx":str,"tpTriggerPxType":str,"tpOrdPx":str,"slTriggerPx":str,"slTriggerPxType":str,"slOrdPx":str,"triggerPx":str,"triggerPxType":str,"ordPx":str}],"pageNum":int,"pageSize":int,"totalPage":int,"totalSize":int},"message":'success',"ts":(int, 13)}
        return self.shema(com_, r, sample, ['查询未触发的计划委托response数据类型校验:', symbol, ''], New=1)

    # web_api 撤销-计划委托
    def CancelTriggerOrder(self,symbol=None,log_level=None,com_=None,caseParam=None,**keypar):
        param = {}
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        if symbol: param['symbol']=symbol
        path = '/v3/trade/web/stopOrders/cancel'
        self.path=self.Url_query + path;self.param=param;
        r = req('post', self.Url_query + path, param, self.token, log_level=log_level)
        # r={"code":"1","message":"success","ts":1234567890123,"data":[{"clOrdId":"str","stopOrderId":"str","sMsg":"str"}]}
        self.result = r
        if log_level and log_level == 3: print(f'{self.source}撤销计划委托 结果',r)
        sample={"code":"1","message":"success","ts":(int,13),"data":[{"clOrdId":str,"stopOrderId":str,"sMsg":str}]}
        return self.shema(com_, r, sample, ['撤销计划委托response数据类型校验:', symbol, ''], New=1)

    # web_api 历史委托-计划委托 查询
    def TriggerOrdersHistory(self,symbol=None,log_level=None,com_=None,caseParam=None,**keypar):
        param = {}
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        if symbol: param['symbol']=symbol
        path = '/v3/trade/record/web/stopOrdersHistory';self.path=self.Url_query + path;self.param=param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level)
        r = {"code":'1',"data":{"list":[{"symbol":"str","tradeType":"str","positionSide":"str","side":"str","marginType":"str","stopOrderId":"str","clOrdId":"str","createTime":1234567890123,"leverage":"str","orderType":"str","stopOrderType":"str","priceType":"str","price":"str","orderQty":"str","reduceOnly":"str","postOnly":"str","triggerPxType":"str","tpTriggerPx":"str","tpTriggerPxType":"str","tpOrdPx":"str","slTriggerPx":"str","slTriggerPxType":"str","slOrdPx":"str","triggerPx":"str","triggerPxType":"str","ordPx":"str"}],"pageNum":1,"pageSize":1,"totalPage":1,"totalSize":1},"message":'success',"ts":1234567890123}
        self.result = r
        if log_level and log_level ==3: print(f'{self.source}历史计划委托 结果',r)
        sample = {"code":'1',"data":{"list":[{"symbol":str,"tradeType":str,"positionSide":str,"side":str,"marginType":str,"stopOrderId":str,"clOrdId":str,"createTime":int,"leverage":str,"orderType":str,"stopOrderType":str,"priceType":str,"price":str,"orderQty":str,"reduceOnly":str,"postOnly":str,"triggerPxType":str,"tpTriggerPx":str,"tpTriggerPxType":str,"tpOrdPx":str,"slTriggerPx":str,"slTriggerPxType":str,"slOrdPx":str,"triggerPx":str,"triggerPxType":str,"ordPx":str}],"pageNum":int,"pageSize":int,"totalPage":int,"totalSize":int},"message":'success',"ts":(int, 13)}
        return self.shema(com_, r, sample, ['历史计划委托查询response数据类型校验:', symbol, ''], New=1)

    # web_api 查询历史完全平仓记录
    def position_closed(self,log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:    param[i] = keypar[i]
        path = '/v3/trade/record/web/position/closed';self.path = self.Url_query + path;self.param = param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询已平仓记录 结果:', r)
        sample = {"code": self.success_code, "data": {"list": [{"tradeType": str, "symbol": str, "exitType": int, "marginType": str, "avgEntryPrice": str,"avgExitPrice": str,
            "positionStatus": str, "positionQty": str, "leverage": str,"commission": str, "realProfit": str,"updateTime": (int, 'len', 13)}], "pageNum": int, "pageSize": int, "totalSize": int,"totalPage": int, }, "message": "success", "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['历史完全平仓记录查询response数据类型校验:', '', ''])

    # web_api 查询合约流水
    def hisAccounts(self,log_level=None,com_=None,source='',**keypar):
        param = {}
        for i in keypar:    param[i]=keypar[i]
        path = '/v3/trade/record/web/account/income';self.path = self.Url_query + path;self.param = param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level);self.result=r;
        sample={"message": "success","data": {"pageNum": int,"pageSize": int,"totalSize": int,"totalPage": int,"list": [{"tradeType": str,"symbol": str,"incomeType": str,"income": str,"details": (int,None),"currency": str}]},"code": self.success_code,"ts": (int,'len',13)}
        if log_level and log_level == 3: print(f'{self.source}查询流水接口 结果:', r)
        return self.shema(com_, r, sample, ['查询历史流水response数据类型校验:', '', ''],New=1)

    # web_api 查询交易对信息
    def instruments(self, log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None:param[i] = keypar[i]
        path = '/v3/public/web/instruments';self.path = self.Url_query + path;self.param = param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询交易对信息 结果:', r)
        sample = {"code": self.success_code, "message": "success", "ts": (int,'len',13), "data": [{"tradeType": str, "symbol": str, "baseAsset": str, "settleCurrency": str, "base": str, "tickSize": str,"ctVal": str, "status": int, "onboardDate": int, "maxQty": str,
                    "minQty": str, "quote": str,"maxNumOrders": str, "maxNumAlgoOrders": str, "maxRiskLimitation": str, "maxLeverage": str,"maintMarginRatio": str, "takerRate": str, "makerRate": str}]}
        return self.shema(com_, r, sample, ['查询交易对信息response数据类型校验:', '', ''],New=1)

    # web_api 查看风险限额-与仓位挂单对应档位
    def riskLimit(self, log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None:param[i] = keypar[i]
        path = '/v3/trade/web/riskLimit';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询风险限额表 结果:', r)
        sample = {"code": self.success_code, "data": {"symbol": str, "tradeType": str, "marginType": str, "bracket": str, "initialLeverage": str,"notionalCap": str, "notionalFloor": str, "maintMarginRatio": str},"message": "success", "ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['查询风险限额表response数据类型校验:', '', ''],New=1)

    # web_api 查看用户全部风险限额
    def allriskLimit(self, log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None:param[i] = keypar[i]
        path = '/v3/trade/web/allRiskLimit';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查看用户全部风险限额 结果:', r)
        sample = {"code": self.success_code, "data": [{"symbol": str, "tradeType": str, "marginType": str, "bracket": str, "initialLeverage": str,"notionalCap": str, "notionalFloor": str, "maintMarginRatio": str}],"message": "success", "ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['查看用户全部风险限额response数据类型校验:', '', ''],New=1)

    # web_api 划转保证金
    def transfer(self, log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None:param[i] = keypar[i]
        path = '/v3/trade/web/account/transfer';self.path = self.Url + path;self.param = param;
        r = req('post', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}划转保证金 结果:',r)
        sample = {"code": self.success_code, "message": "success", "ts": (int,'len',13),"data": {"transId": int, "fromAccountType": str, "toAccountType": str, "currency": str,"amount": str}}
        return self.shema(com_, r, sample, ['划转保证金response数据类型校验:', '', ''], New=1)

    # web_api 获取用户手续费率
    def commissionRate(self, log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:    param[i] = keypar[i]
        path = '/v3/trade/commissionRate';self.path = self.Url_query + path;self.param = param;
        r = req('get', self.Url_query + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询用户手续费率 结果:', r)
        sample = {"code": self.success_code, "message": "success", "ts": (int,'len',13), "data": [{"tradeType": str, "symbol": str, "makerRate": str,"takerRate": str, }]}
        return self.shema(com_, r, sample, ['查询用户手续费率response数据类型校验:', '', ''],New=1)

    # web_api 交易账户  （币种总的浮动盈亏，OpenAPI是给量化用户做资产管理的。前端账户暂时都不需要）
    def balances(self,log_level=None, com_=None, **keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/trade/web/tradingAccount';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询交易账户 结果:', r)
        sample = {"code": self.success_code, "data": [{"currency": str, "marginEquity": str, "marginFrozen": str, "marginPosition": str,"marginAvailable": str, "maxWithdrawAmount": str}], "message": "success", "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['交易账户response数据类型校验:', '', ''],New=1)

    # web_api 查询持仓
    def position(self, tradeType=None, log_level=None, com_=None, **keypar):
        param = {'tradeType':tradeType}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/trade/web/position';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询持仓 结果:', r)
        sample = {"code": self.success_code, "data": [
            {"tradeType": str, "positionSide": str, "symbol": str, "marginType": str, "avgEntryPrice": str,"positionAmt": str, "posMargin": str,
             "leverage": str, "liquidationPrice": str, "unrealisedPnl": str, "earningRate": str, "markPrice": str, "base": str,"quote": str,'positionId':str,'availPos':str}], "message": "success", "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['持仓查询 数据类型校验:', '', ''],New=1)

    # web_api 查询用户当前杠杆倍数（备注：webapi中 tradeType、symbol为必填字段）
    def leverage_info(self,tradeType = None, symbol = None,log_level=None,com_=None, **keypar):
        param =  {'tradeType':tradeType,'symbol':symbol}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path='/v3/trade/web/leverage/info';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询杠杆信息 结果:',r)
        sample ={"code": self.success_code, "message": "success", "data": [{"tradeType": str, "symbol": str, "leverage": str, "marginType": str}],"ts": (int,'len',13)}
        return self.shema(com_, r, sample, ['查询杠杆response数据类型校验:', '', ''], New=1)

    # web_api 切换杠杆
    def changeleverage(self, tradeType=None, symbol=None, leverage=None, marginType=None, log_level=None, com_=None,**keypar):
        param = {'tradeType': tradeType, 'symbol': symbol, 'leverage': leverage, 'marginType': marginType}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/trade/web/leverage';self.path = self.Url + path;self.param = param;
        r = req('post', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}切换杠杆 结果:', r)
        sample ={ "code": self.success_code, "message": "success", "data": { "tradeType": str, "symbol": str, "leverage": str, "marginType": str }, "ts": (int,'len',13) }
        return self.shema(com_, r, sample, ['切换杠杆response数据类型校验:', '', ''],New=1)

    # web_api 获取用户自选列表
    def GetFavirite(self,tradeType=None, log_level=None, com_=None):
        param={}
        if tradeType: param['tradeType']=tradeType
        path = '/v3/user/web/favorite';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result = r;
        if log_level and log_level == 3: print(f'{self.source}获取自选列表 结果:', r)
        sample = {"code": self.success_code, "message": "success","data": list, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['获取自选列表response数据类型校验:', '', ''], New=1)

    # web_api 新增自选
    def AddFavirite(self,tradeType=None,symbolList=None, log_level=None, com_=None):
        param={}
        if tradeType: param['tradeType']=tradeType
        if symbolList: param['symbolList'] = symbolList
        path = '/v3/user/web/favorite/add';self.path = self.Url + path;self.param = param;
        r = req('post', self.Url + path, param, self.token, log_level=log_level);self.result = r;
        if log_level and log_level == 3: print(f'{self.source}新增自选 结果:', r)
        sample = {"code": self.success_code, "message": "success","data": list, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['新增自选response数据类型校验:', '', ''], New=1)

    # web_api 取消自选
    def CancelFavirite(self,tradeType=None,symbolList=None, log_level=None, com_=None):
        param={}
        if tradeType: param['tradeType']=tradeType
        if symbolList: param['symbolList'] = symbolList
        path = '/v3/user/web/favorite/delete';self.path = self.Url + path;self.param = param;
        r = req('post', self.Url + path, param, self.token, log_level=log_level);self.result = r;
        if log_level and log_level == 3: print(f'{self.source}删除自选 结果:', r)
        sample = {"code": self.success_code, "message": "success","data": list, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['删除自选response数据类型校验:', '', ''], New=1)

    # web_api 获取偏好设置
    def QueryFavoriteSetting(self,log_level=None, com_=None,**keypar):
        param={}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/user/web/favorite/setting/query';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result = r;
        if log_level and log_level == 3: print(f'{self.source}获取偏好设置 结果:', r)
        sample = {"code": self.success_code, "message": "success","data": {"preview":int,"tradeUnit":int}, "ts": (int, 'len', 13)}
        return self.shema(com_, r, sample, ['获取偏好设置response数据类型校验:', '', ''], New=1)

    # web_api 更新偏好设置
    def UpdateFavoriteSetting(self,log_level=None,com_=None,**keypar):
        param={}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/user/web/favorite/setting/update';self.path = self.Url + path;self.param = param;
        r = req('post', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}更新偏好设置 结果:', r)
        sample ={ "code": self.success_code, "message": "success","ts": (int,'len',13), "data": {"preview":int,"tradeUnit":int}}
        return self.shema(com_, r, sample, ['更新偏好设置response数据类型校验:', '', ''],New=1)

    # web_api 查询用户全部币种
    def userallSymbol(self,log_level=None, com_=None,**keypar):
        param = {}
        for i in keypar:
            if not keypar[i] == None: param[i] = keypar[i]
        path = '/v3/trade/web/user/allSymbol';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}查询用户全部币种 结果:', r)
        sample ={ "code": self.success_code, "message": "success","ts": (int,'len',13), "data": list}
        return self.shema(com_, r, sample, ['查询用户全部币种response数据类型校验:', '', ''],New=1)

    # web_api 下单二次确认
    def orderPreview(self, tradeType=None, symbol=None, side=None,positionSide=None, orderType=None, reduceOnly=None, marginType=None,
        price=None, priceType=None, orderQty=None, postOnly=None,timeInForce=None,log_level=None, com_=None, caseParam=None):
        param = {}
        if caseParam:
            for i in caseParam: param[i]=caseParam[i]
        if tradeType: param['tradeType'] = tradeType
        if symbol: param['symbol'] = symbol
        if positionSide: param['positionSide'] = positionSide
        if marginType: param['marginType'] = marginType
        if orderType: param['orderType'] = orderType
        if side: param['side'] = side
        if price: param['price'] = price
        if priceType: param['priceType'] = priceType
        if orderQty: param['orderQty'] = orderQty
        if postOnly: param['postOnly'] = postOnly
        if reduceOnly: param['reduceOnly'] = reduceOnly
        if timeInForce: param['timeInForce'] = timeInForce
        path = '/v3/trade/web/orders/preview';self.path = self.Url + path;self.param = param;
        r = req('get', self.Url + path, param, self.token, log_level=log_level);self.result=r;
        if log_level and log_level == 3: print(f'{self.source}下单二次确认 结果:', r)
        sample ={ "code": self.success_code, "message": "success","ts": (int,'len',13), "data": {'liquidationPrice':str}}
        return self.shema(com_, r, sample, ['下单二次确认response数据类型校验:', '', ''],New=1)

    def getToken(self,user_id):
        orderName = urlConfig.order_url_demo+'/common/v2/user/getToken'; # DEV 用 demo 环境的token
        # if str(self._server)=='6' : orderName = urlConfig.order_url_QA+'/common/v2/user/getToken'; #QA 用 QA 环境的token
        param = 'userId='+str(user_id)
        return req('get', orderName, param)

    def shema(self,com_,r,sample,title,New=None):
        if com_:
            com_r = com(sample, r, [ title[0] + title[1], ' 返参异常:', '', ''],New=New)
            if not com_r: u(0);return False;
            else: u(1);return r
        else: return r

    def muLanOrderBook(self,symbolId,log_level=None):
        param = {'symbolId':symbolId }
        url='https://qamock.cn.atomintl.com/md_mock/orderbook'
        return req('get', url, params=param, log_level=log_level)

    #处理openapi标记价格,从webapi这边获取
    def webposition(self,symbol):
        makrPrice= dict.makrPriceMap
        NTS=n_order(self.server,user_id=self.user_id)
        tradeType = 'linearPerpetual'
        position=NTS.position(tradeType=tradeType)['data']
        if len(position)>0:
            for i in range(0,len(position)):
                makrPrice[position[i]['symbol']]=position[i]['markPrice']
        makrPrice = makrPrice[symbol]
        return makrPrice

def basicResponse_check(o,log_level=None):
    r=o.leverage_info('linearPerpetual','ETH',com_=1);u(r,p='查询杠杆 返参验证',log_level=log_level)
    r=o.leverage_change('linearPerpetual','ETH','isolated',22,com_=1);u(r,p='调整杠杆 返参验证',log_level=log_level)
    r = o.margin_change('linearPerpetual', 'ETH', 'long', 100,type=1, com_=1);u(r,p='调整保证金 返参验证',log_level=log_level)

if __name__ == '__main__':
    NTS_WEB=n_order('5',user_id='99999');
    # NTS_WEB = n_order('6', user_id='97201955') #97121927 \ 97201967 （8885）   HUGO: 118939  ALEX: 97110280
    # NTS_WEB = N_apiOrder('6', user_id='97201967')
    print(NTS_WEB.token)
    currency = 'USDT';amount = 20000 ; fromAccountType = 'funding';toAccountType = 'Futures';tradeType='linearPerpetual'
    # #划转`
    # r = NTS_WEB.transfer(currency=currency, amount=str(amount), fromAccountType=fromAccountType, toAccountType=toAccountType, log_level=3)
    r=NTS_WEB.balances(log_level=3,currency=currency)#
    r=NTS_WEB.position(log_level=3,tradeType=tradeType,symbol='BTCUSDT',marginType='cross')
    from UnitTest.com import CreateOrders
    a = CreateOrders(NTS_WEB, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,
                     MarketFlag=False, OpenFlag=True)
    a['orderType']='triggerLimit';a['triggerPxType']="last";a["ordPx"]=13000;
    NTS_WEB.triggerOrder(caseParam=a,log_level=3)

    # print(a)
    # time.sleep(10000)
    # r=NTS_WEB.leverage_info(tradeType='linearPerpetual',symbol='BTCUSDT',log_level=3)
    # r = NTS_WEB.hisAccounts(log_level=3)
    # r=NTS_WEB.GetFavirite(tradeType=tradeType,log_level=3)
    NTS_WEB.hisOrders(tradeType='linearPerpetual', symbol='BTCUSDT', log_level=3)
    NTS_WEB.hisTrades(tradeType='linearPerpetual', symbol='BTCUSDT', log_level=3)
    # time.sleep(1000)
    #     print(_t(),r['data']['totalSize']);time.sleep(5)
    symbol = 'BTCUSDT';price='12330';orderQty = '5';tradeType = 'LinearPerpetual';side = 'Buy';positionSide = 'Long';marginType = 'cross';orderType = 'market';
    orderBasicParam={'marginType':'isolated','orderType':'limit','tradeType':'linearPerpetual'}
    orderParam={'symbol':symbol,'price':price,'orderQty':orderQty,'side' : 'buy','positionSide':'long'};orderParam.update(orderBasicParam);S=datetime.datetime.now();
    # r = NTS_WEB.order(symbol=symbol, log_level=3, price=price, tradeType=tradeType, side=side,positionSide=positionSide, marginType=marginType, orderType=orderType, orderQty=orderQty);

        ##★⭐️⭐️⭐️~(@^_^@)~ 逐仓下单  ~(@^_^@)~
    # r=NTS_WEB.order(log_level=3,caseParam=orderParam);E=datetime.datetime.now();print('耗时',str((E - S))[:-3]);
    r = NTS_WEB.openOrders(tradeType='linearPerpetual', symbol='BTCUSDT', log_level=3)
    # import case.other.UserDataCheck as UserDataCheck
    # UserDataCheck.UsderDataCheckCase(NTS_WEB, 2, option='123', title='test ')
        # NTS_WEB = n_order('6', user_id='118939') #97121927 \ 97201967 （8885）   HUGO: 118939  ALEX: 97110280
        # NTS_WEB = N_apiOrder('6', user_id='97201967')

# basicResponse_check(1)
# print(NTS.trigger_order(symbol='BTC'))
# print(NTS.orderCancel(1, 0,'63', com_=1,log_level=2, foo=1, bar=2,sh=[1,2]))
# print('【Case】', '总数:', ut._all, '通过:', ut._pass, '失败:', ut._all - ut._pass - ut._block, '阻塞:', ut._block,'通过率: ' + str(truncate(ut._pass / ut._all * 100, 2)) + '%');
