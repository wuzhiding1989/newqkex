# from BU.NTS.ApiOrder import NtsApiOrder
from BU.futures.api import webapi as NTS_WEB
from decimal import *
import random
token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBVE9NSU5UTCIsInVpZCI6OTcxMjE5MjcsImlhdCI6MTY2MzgyODQ4MSwiZXhwIjoxNjYzOTE0ODgxfQ.WBI81QBOJy5DM5ShGKEfmEYyPNAb1fnByGrvAwBbPFcH20oUkXGn9Wn1iesMNoOZb13qgRIkbyYccqWUaHRENaKKelH3sUNjGpwLHDKKzQtl9y21PN36dO2Y06elzr6o2SkKXTCWvxN0dS3e50hOE9Jniqt97KyLKqAfwdcPDiSfItvse-CeKTSLxB8BYouUy5v8kBXaHsmzBzHk9QPzPuwsZB5Dlp7IqgAMPgLdZKoQ_f0Ax8T9UC7XWda7KJNPAsSfQtssj1VtSKCQRy6UUdyCaWTBOAKj2ICnUzOpYxLeANAf4WrNRY2zyPBzsL9zmYbpu35IxZzTy3QPXttSIg'
# NTS_WEB = NTS_WEB(5,token=token)
# NTS = NtsApiOrder(5)

class BasicData:
    # def __init__(self, server=None, product=None, user_id=None, token=None):
    #
    #     # self.NTS=NtsApiOrder(6, user_id='99999')
    #

    #获取合约信息
    def contractCode(self, NTS,tradeType=None, symbol=None):
        if tradeType == None:
            tradeType = 'linearPerpetual'
        # r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)['data']
        r = NTS.instruments(tradeType=tradeType, symbol=symbol)['data']
        dict = {
            "symbol":'',
            "tickSize":'',
            "ctVal":'0',
            "takerRate":'0',
            "makerRate":'0',
            'maintMarginRatio':'0'
        }
        for tmp in r :
            if symbol == tmp['symbol']:
                dict['symbol']=tmp['symbol']
                dict['tickSize'] = tmp['tickSize']
                dict['ctVal'] = tmp['ctVal']
                dict['takerRate'] = tmp['takerRate']
                dict['makerRate'] = tmp['makerRate']
                dict['maintMarginRatio'] = tmp['maintMarginRatio']
        return dict

    #获取交易所上了哪些symbol
    def contract(self, tradeType=None, symbol=None):

        r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
        a = r['data']
        symbol = []
        for tmp in a:
            symbol.append(tmp['symbol'])
        return symbol

    # 获取币种tickSize
    def tickSize(self, tradeType=None,symbol=None):
        r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
        a = r['data']
        for tmp in a:
            return tmp['tickSize']


    #获取maker手续费
    def makerRate(self,tradeType=None,symbol=None,source='API'):
        if source=='API':s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if source=='web': s=NTS_WEB.instruments(tradeType=tradeType, symbol=symbol)
        if symbol in s:
            r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
            a = r['data']
            for tmp in a:
                return tmp['makerRate']
        else:
            return 0

    # 获取taker手续费
    def takerRate(self, NTS,tradeType=None, symbol=None,source='API'):
        s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if source=='API': s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if source=='web': s = NTS_WEB.instruments(tradeType=tradeType, symbol=symbol)
        if symbol in s:
            # r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
            r = NTS.instruments(tradeType=tradeType, symbol=symbol)

            a = r['data']
            for tmp in a:
                return tmp['takerRate']
        else:
            return 0

    #处理精度
    def size(self, num):
        if num >= 1:
            size=0
        else:
            size = abs(Decimal(str(num)).as_tuple()[2])

        return size
        # 处理价格精度
    def pricesize(self,NTS, tradeType=None, symbol=None):
        dictSize = BasicData().contractCode(NTS,tradeType=tradeType,symbol=symbol)
        size = dictSize['tickSize']
        size=float(size)
        pricesize=BasicData().size(size)
        return pricesize

    #获取最大数量上限
    def maxQty(self,NTS,tradeType=None, symbol=None):
        s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if symbol in s:
            r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
            a = r['data']
            for tmp in a:
                return tmp['maxQty']
        else:
            return 0

    #获取最小数量上限 minQty
    def minQty(self,tradeType=None, symbol=None):
        s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if symbol in s:
            r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
            a = r['data']
            for tmp in a:
                return tmp['minQty']
        else:
            return 0
    #最多可挂多少个单(笔数)
    def maxNumOrders(self,tradeType=None, symbol=None):
        s = BasicData().contract(tradeType=tradeType, symbol=symbol)
        if symbol in s:
            r = self.NTS.instruments(tradeType=tradeType, symbol=symbol)
            a = r['data']
            for tmp in a:
                return tmp['maxNumOrders']
        else:
            return 0

    #获取标记价格
    def markPrice(self,tradeType=None, symbol=None):
        r = self.NTS.markPrice(tradeType=None, symbol=None)['data']

        for tmp in r:
            return tmp['markPrice']



    #划转数量随机处理
    def transferAmount(self,x,y,z,type=None):

        if type == 1 or type == None: #随机生成x-y之间的小数，保留z位小数
            amount = round(random.uniform(x,y),z)
        if type == 2: #随机生成x-y之间的正整数（包含x、y）
            amount = round(random.randint(x, y), z)
        if type == 3: #随机生成x-y之间的正整数（不包含x、y）
            amount = round(random.randrange(x, y), z)

        return amount







if __name__ == '__main__':
    # token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBVE9NSU5UTCIsInVpZCI6OTcxMjE5MjcsImlhdCI6MTY2MzgyODQ4MSwiZXhwIjoxNjYzOTE0ODgxfQ.WBI81QBOJy5DM5ShGKEfmEYyPNAb1fnByGrvAwBbPFcH20oUkXGn9Wn1iesMNoOZb13qgRIkbyYccqWUaHRENaKKelH3sUNjGpwLHDKKzQtl9y21PN36dO2Y06elzr6o2SkKXTCWvxN0dS3e50hOE9Jniqt97KyLKqAfwdcPDiSfItvse-CeKTSLxB8BYouUy5v8kBXaHsmzBzHk9QPzPuwsZB5Dlp7IqgAMPgLdZKoQ_f0Ax8T9UC7XWda7KJNPAsSfQtssj1VtSKCQRy6UUdyCaWTBOAKj2ICnUzOpYxLeANAf4WrNRY2zyPBzsL9zmYbpu35IxZzTy3QPXttSIg'
    # # NTS_WEB = NTS_WEB(5,token=token
    # NTS = NtsApiOrder(6, user_id='99999')
    # print(BasicData().contractCode(tradeType='linearPerpetual',symbol='BTCUSDT'))
    #获取币种价格精度
    # print(BasicData().pricesize(tradeType='linearPerpetual', symbol='BTCUSDT'))
    #   # print(BasicData.contractCode(self=None,tradeType='linearPerpetual', symbol='BTC-USDT'))
    print(BasicData().size(0.0001))
    #   #   print(BasicData().randomAmount(x=1,y=131,z=8))

    pass
