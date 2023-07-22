import time,random,ast
from common.mysqlq import jis
from BU.spot.api import webapi as wp
from case import google_code as wd
from common import util as ut
from common.data import account,user,amount1,side_buy,side_sell,verifyCode,secret_key,headers,secret_key1
from common.data1 import headers4,s_key,s_user,y_key,y_user,password
from BU.spot.api.webapi import headers3
aa=str(random.randint(4,9))
#发布买卖的广告
def otcbuy_order(symbol=None):
    gol = wd.read_google_authenticator_code(secret_key=s_key)
    res = wp.login(account=s_user,password=password,verifyCode=gol)
    if res['code'] !=0:
        print('登录报错为',res['msg'])
        return
    token = res['data']['accessToken']
    headers['X-Authorization'] = token
    avb_1=wp.otc_assets_symbol(headers1=headers,symbol=symbol)
    a=(ut.d(avb_1[0]))/ut.d(aa)
    c=("{:.5f}".format(a))
    fabu = wp.otc_orders(headers1=headers,amount=c,side='buy',quote='USD',base=symbol)
    if fabu['code'] !=0:
        print('shll发布广告报错为',fabu['msg'])
    time.sleep(1)
    rid=wp.user(headers)
    userid=rid['data']['userId']
    fabu1 = wp.otc_orders(headers1=headers, amount=c, side='sell',quote='USD',base=symbol)
    if fabu1['code'] != 0:
        print('buy发布广告报错为', fabu1['msg'])
        return
    avb_2 = wp.otc_assets_symbol(headers1=headers, symbol=symbol)
    if (ut.d(avb_1[0])+ut.d(avb_1[1]))-(ut.d(avb_2[0])+ut.d(avb_2[1])) == 0:
        print('总余额检验正确')
    else:
        print('总余额检验失败，分别为',avb_1[0],avb_1[1],avb_2[0],avb_2[1])
    sql = f"SELECT a.fee_rate,b.`status`, b.ratio,b.target_uid AS s_uid ,b.source_uid as f_uid,(SELECT platform_commission_rate FROM config_currency WHERE symbol='btc' AND legal_symbol='usd') AS fee FROM user_info a,rebate_config b WHERE a.user_id=b.source_uid AND a.user_id in ({userid})"
    fee= jis(sql)
    ad=ut.d(c) / (1+fee)
    if avb_2[1] ==c:
        print('广告单冻结数量正确')
    cw = wp.orders_select(headers1=headers)  # 获取广告id
    for tmp in cw['data']:
        if tmp['side']=='sell':
            availableAmount=tmp['availableAmount']
            print(availableAmount)
    if ut.d(ad)-ut.d(availableAmount)<0.00000001:
        print('发布广告可售数量正确')
    print(aa)
def buy_otc_order():
    cw = wp.orders_select(headers1=headers3)#获取广告id
    id = cw['data'][0]['id']
    exchangeRate = cw['data'][0]['exchangeRate']
    print(cw)
    cd = ast.literal_eval(cw['data'][0]['paySupport'])
    for tmp in cd:
        if tmp['name']=='wechatpay':
            bankcard=tmp['id']
    print(cd)
    gol = wd.read_google_authenticator_code(secret_key=secret_key1)#获取用户谷歌验证码
    print('c',cw)
    qw = wp.otc_pendings(headers3=headers4,id=id,exchangeRate=exchangeRate,amount=0.01,googleVerifyCode=gol)#根据广告id下单
    if qw['code']!=0:
        print('下单失败，报错为',qw['msg'])
    orid = qw['data']['id']
    print(qw)
    cw = wp.otc_pendings_paid(orderid=orid,headers3=headers4,payment=bankcard)#用户点击已付款
    print(cw)
    gol = wd.read_google_authenticator_code(secret_key=secret_key)#获取商家谷歌验证码
    print(gol)
    aw = wp.otc_pendings_complete(headers3=headers3,orderid=orid,googleVerifyCode=gol,tradePassword=password)#确认放币
    print(aw)

if __name__ == '__main__':
    #print(buy_otc_order())
    print(otcbuy_order(symbol='BTC'))