from BU.spot.api import webapi as wb
from common.util import login_email,otc_assets_symbol,d
import ast,random

symbol='BTC'

def otc_public_orders(symbol, legalSymbol, side, page, pageSize,id, amount=None, payType=None):
    res = wb.otc_PublicOrders(amount=amount, payType=payType, symbol=symbol, legalSymbol=legalSymbol, side=side,
                             page=page, pageSize=pageSize)
    orders ={}
    if res['code'] !=0:
        print('获取c2c订单列表失败，原因：',res['msg'])
        return False
    res = res['data']['orders']
    for tmp in res:
        if id == tmp['id']:
            orders['availableAmount'] = tmp['availableAmount']
            orders['exchangeRate'] = tmp['exchangeRate']
            orders['maxPlacePrice'] = tmp['maxPlacePrice']
            orders['minPlacePrice'] = tmp['minPlacePrice']
            orders['payType'] = ast.literal_eval(tmp['paySupport'])[0]['payType']
    return orders

def otc_send_ads():
    avb_1=otc_assets_symbol(symbol=symbol)
    a=(d(avb_1[0]))/d(str(random.randint(4,9)))
    c=("{:.5f}".format(a))
    fabu = wb.otc_orders(amount=c, side='buy', quote='USD', base=symbol)
    print(c)





if __name__ == '__main__':
    #print(otc_public_orders(amount=None,payType=None,symbol='BTC',id=114,legalSymbol='USD',side='sell',page=1,pageSize=1000))
    print(otc_send_ads())