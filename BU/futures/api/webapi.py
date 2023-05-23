import copy
import requests
from BU.admin import web
from config import userdate,serverdate

symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'positionSide'
postOnly = 'false';reduceOnly = 'false';orderType = 'limit';priceType = 'optimalN';pageNum = '1';pageSize = '10'
gear='depth0';limit=1000;period='1m'


class webapi():
    def __init__(self,user,server):
        self.headers = {"Content-Type": "application/json", "Accept-Language": "zh-TW", "source": "web"}
        self.account = userdate.weblogin[user]['username']
        self.password = userdate.weblogin[user]['password']
        self.secret = userdate.weblogin[user]['secret']
        self.headers['X-Authorization'] = web.getAccessToken(account=self.account,password=self.password,secret=self.secret)
        self.tradeurl = serverdate.server[server]['tradeapi']
        self.queryurl = serverdate.server[server]['queryapi']
        self.qkurl = serverdate.server[server]['qkurl']

    # 划转
    def web_transfer(self,fromAccountType=None, toAccountType=None, currency=None, amount=None):
        path = '/v1/trade/web/account/transfer'
        params = {
            "fromAccountType": fromAccountType,
            "toAccountType": toAccountType,
            "currency": currency,
            "amount": amount}
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res
    def web_wallet_transfer(self,fromAccountType=None, toAccountType=None, currency=None, amount=None,pairCode=None,symbol=None):
        path = '/wallet/transfer'
        params = {
            "from": fromAccountType,
            "to": toAccountType,
            "currency": currency,
            'pairCode':pairCode,
            'symbol':symbol,
            "amount": amount}
        res = requests.post(url=self.qkurl + path, json=params, headers=self.headers).json()
        return res

    # 单个下单
    def web_order(self,tradeType=None, symbol=None, side=None, positionSide=None, orderType=None, reduceOnly=None,
                      marginType=None, price=None, priceType=None, orderQty=None, postOnly=None, timeInForce=None):
        path = '/v1/trade/web/orders'
        params = {"tradeType": tradeType,
                  "symbol": symbol,
                  "side": side,
                  "positionSide": positionSide,
                  "orderType": orderType,  # market，limit
                  "reduceOnly": reduceOnly,
                  "marginType": marginType,
                  "price": price,
                  "priceType": priceType,
                  "orderQty": orderQty,
                  "postOnly": postOnly,
                  "timeInForce": timeInForce}  # GTC/IOC/FOK
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res

     # 一键平仓
    def web_oneClickClose(self,tradeType=None, symbol=None):
        path = '/v1/trade/web/oneClickClose'
        params = {
            "tradeType": tradeType,
            "symbol": symbol}
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res


     # 查询持仓
    def web_position(self,tradeType=None, symbol=None, marginType=None):
        path = '/v1/trade/web/position'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "marginType": marginType}
        res = requests.get(url=self.tradeurl + path, params=params, headers=self.headers).json()
        return res

     # 撤销单个订单
    def web_orders_cancel(self,tradeType=None, symbol=None, orderId=None):
        path = '/v1/trade/web/orders/cancel'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "orderId": orderId}
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res


    def web_orders_oneClickClose(self,tradeType=None, symbol=None):  # 一键撤销所有订单
        path = '/v1/trade/web/orders/oneClickCancel'
        params = {
            "tradeType": tradeType,
            "symbol": symbol}
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res

    # 当前委托
    def web_openOrders(self,tradeType=None, symbol=None, side=None, clOrdId=None, orderId=None, pageNum=None,
                           pageSize=None):
        path = '/v1/trade/web/openOrders'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "side": side,
            "orderId": orderId,
            "clOrdId": clOrdId,
            "pageNum": pageNum,
            "pageSize": pageSize}
        res = requests.get(url=self.tradeurl + path, params=params, headers=self.headers).json()
        return res


    # 查询历史计划委托 /v1/trade/record/web/stopOrdersHistory
    def web_stopOrdersHistory(self,tradeType=None, symbol=None, startTime=None, endTime=None, pageNum=None, pageSize=None,
                          marginType=None, orderType=None, stopOrderId=None):
        path = '/v1/record/web/stopOrdersHistory'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "marginType": marginType,
            "orderType": orderType,
            "stopOrderId": stopOrderId
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 获取用户自选列表
    def web_favorite(self,tradeType=None):
        path = '/v1/user/web/favorite'
        params = {
            "tradeType": tradeType
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 新增用户自选
    def web_favorite_add(self,tradeType=None, symbolList=None):
        path = '/v1/user/web/favorite/add'
        params = {
            "tradeType": tradeType,
            "symbolList": symbolList
        }
        res = requests.post(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 取消用户自选
    def web_favorite_delete(self, tradeType=None, symbolList=None):
        path = '/v1/user/web/favorite/delete'
        params = {
            "tradeType": tradeType,
            "symbolList": symbolList
        }
        return requests.post(url=self.queryurl + path, params=params, headers=self.headers).json()




    # 查询用户偏好设置/v1/user/web/favorite/setting/query
    def web_favorite_setting_query(self,tradeType=None):
        path = '/v1/user/web/favorite/setting/query'
        params = {
            "tradeType": tradeType
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 更新用户偏好设置 /v1/user/web/favorite/setting/update
    def web_favorite_setting_update(self,tradeType=None, preview=None, tradeUnit=None):
        path = '/v1/user/web/favorite/setting/update'
        params = {
            "tradeType": tradeType,
            "preview": preview,
            "tradeUnit": tradeUnit
        }
        res = requests.post(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 查询交易对列表 /v1/public/web/instruments
    def web_instruments(self,tradeType=None, symbol=None):
        path = '/v1/public/web/instruments'
        params = {
            "tradeType": tradeType,
            "symbol": symbol
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 查询历史订单 /v1/trade/record/web/orders/history
    def web_orders_history(self,tradeType=None, symbol=None, startTime=None, endTime=None, pageNum=None, pageSize=None,
                           side=None, orderType=None, orderId=None, clOrdId=None, orderStatus=None):
        path = '/v1/record/web/orders/history'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "side": side,
            "orderType": orderType,
            "orderId": orderId,
            "clOrdId": clOrdId,
            "orderStatus": orderStatus
        }
        res = requests.get(url=self.queryurl + path, json=params, headers=self.headers).json()
        return res


    # 查询历史成交 /v1/trade/record/web/orders/fills
    def web_orders_fills(self,tradeType=None, symbol=None, startTime=None, endTime=None, pageNum=None, pageSize=None,
                         side=None, orderType=None, orderId=None, clOrdId=None, tradeId=None):
        path = '/v1/record/web/orders/fills'

        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "side": side,
            "orderType": orderType,
            "orderId": orderId,
            "clOrdId": clOrdId,
            "tradeId": tradeId
        }
        res = requests.get(url=self.queryurl + path, json=params, headers=self.headers).json()
        return res


    # 查询历史流水记录 /v1/trade/record/web/account/income
    def web_account_income(self,tradeType=None, symbol=None, startTime=None, endTime=None, pageNum=None, pageSize=None,
                           incomeType=None, currency=None):
        path = '/v1/record/web/account/income'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "incomeType": incomeType,
            "currency": currency
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 查询历史完全平仓记录 /v1/trade/record/web/position/closed
    def web_position_closed(self,tradeType=None, symbol=None, startTime=None, endTime=None, pageNum=None, pageSize=None,
                            marginType=None, pnlType=None):
        path = '/v1/record/web/position/closed'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "marginType": marginType,
            "pnlType": pnlType

        }
        res = requests.get(url=self.queryurl + path, json=params, headers=self.headers).json()
        return res

    # 切换更杠
    def web_change_reverage(self,tradeType=None,symbol=None,leverage=None,marginType=None):
        path = '/v1/trade/web/leverage'
        data = {
                "tradeType": tradeType,
                "symbol": symbol,
                "leverage": leverage,
                "marginType": marginType
                }
        res = requests.post(url=self.queryurl + path, json=data, headers=self.headers).json()
        return res

    # 查询当前用户更杠信息 /v1/trade/web/leverage/info
    def web_leverage_info(self,tradeType=None, symbol=None,marginType=None):
        path = '/v1/trade/web/leverage/info'
        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "marginType": marginType,

        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res


    # 二次确认 /v1/trade/web/orders/preview
    def web_orders_preview(self,tradeType=None, symbol=None,side=None,positionSide=None, orderType=None,
                           reduceOnly=None, marginType=None,price=None,priceType=None,orderQty=None,postOnly=None,timeInForce=None):
        path = '/v1/trade/web/orders/preview'

        params = {
            "tradeType": tradeType,
            "symbol": symbol,
            "side": side,
            "positionSide": positionSide,
            "orderType": orderType,
            "reduceOnly": reduceOnly,
            "marginType": marginType,
            "price": price,
            "priceType": priceType,
            "orderQty": orderQty,
            "postOnly": postOnly,
            "timeInForce":timeInForce
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res

    # 查看用户全部币对 /v1/trade/web/user/allSymbol
    def web_user_allSymbol(self,type=None):
        path = '/v1/trade/web/orders/preview'

        params = {
                "type":type
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res

    # 调整逐仓保证金 /v1/trade/web/position/margin
    def web_position_margin(self,tradeTyp=None, symbol=None, positionSide=None, amount=None,type=None):
        path = '/v1/trade/web/position/margin'
        params ={
          "tradeType": tradeTyp,
          "symbol": symbol,
          "positionSide": positionSide,
          "amount": amount,
          "type": type
        }
        res = requests.post(url=self.tradeurl + path, json=params, headers=self.headers).json()
        return res

    #查看风险限额-与仓位挂单对应档位 /v1/trade/web/riskLimit
    def web_riskLimit(self,tradeType=None,symbol=None,marginType=None):
        path = '/v1/trade/web/riskLimit'

        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "marginType":marginType
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res

    #查看用户全部风险限额 /v1/trade/web/allRiskLimit
    def web_allRiskLimit(self,tradeType=None,symbol=None,marginType=None):
        path = '/v1/trade/web/allRiskLimit'

        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "marginType":marginType
        }
        res = requests.get(url=self.queryurl + path, params=params, headers=self.headers).json()
        return res

    #/v1/trade/web/tradingAccount
    def web_tradingAccount(self,currency=None):#/v1/trade/web/tradingAccount资产接口
        path = '/v1/trade/web/tradingAccount'
        params ={'currency':currency}
        #print(self.tradeurl+path)
        res = requests.get(url=self.tradeurl+path,json=params,headers=self.headers).json()
        return res
    def web_market_depth(self,tradeType=None,symbol=None,limit=None,gear=None):#/v1/market/depth 查询指定档位深度
        path = '/v1/market/depth'
        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "gear": gear,
                "limit":limit
        }
        res = requests.get(url=self.queryurl+path,params=params).json()
        return res
    def web_market_kline(self,tradeType=None,symbol=None,limit=None,period=None):#/v1/market/kline   k线
        path = '/v1/market/kline'
        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "period": period,
                "limit":limit
        }
        res = requests.get(url=self.queryurl+path,params=params).json()
        return res
    def web_market_ticker_24hr(self,tradeType=None,symbol=None,limit=None):#/v1/market/ticker/24hr   行情
        path = '/v1/market/ticker/24hr'
        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "limit":limit
        }
        res = requests.get(url=self.queryurl+path,params=params).json()
        return res
    def web_market_ticker_mini(self,tradeType=None,symbol=None,limit=None):#/v1/market/ticker/mini   查询行情简化信息
        path = '/v1/market/ticker/mini'
        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "limit":limit
        }
        res = requests.get(url=self.queryurl+path,params=params).json()
        return res
    def web_market_trade(self,tradeType=None,symbol=None,limit=None):#/v1/market/trade   查询成交记录
        path = '/v1/market/trade'
        params = {
                "tradeType": tradeType,
                "symbol": symbol,
                "limit":limit
        }
        res = requests.get(url=self.queryurl+path,params=params).json()
        return res

if __name__ == '__main__':
    wb = webapi(2,server='test')
    # print(wb.web_order(tradeType,symbol,side,positionSide,orderType,reduceOnly))
    # print(wb.web_openOrders(tradeType=tradeType, symbol=symbol))
    print(wb.web_market_depth(tradeType=tradeType,gear=gear,symbol=symbol,limit=limit))
    print(wb.web_market_ticker_mini(tradeType=tradeType,symbol=symbol,limit=limit))
    print(wb.web_market_ticker_24hr(tradeType=tradeType, symbol=symbol, limit=limit))
    print(wb.web_market_trade(tradeType=tradeType, symbol=symbol, limit=limit))
    print(wb.web_market_kline(tradeType=tradeType, symbol=symbol, limit=limit,period=period))
