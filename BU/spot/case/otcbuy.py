import time
from BU.spot.api import webapi as wp
from case import google_code as wd ;
from case import ccte as wq
from common import util as u
from common import data1 as da
import ast,random
amount='0.0' + str(random.randint(1000, 9999))
user_secret_key=da.y_key;mer_secret_key=da.s_key;password=da.password;mer_email=da.s_user
user_email=da.y_user;
#c2c下单接口校验
def otc_buy():
    user_headers=wq.login_email(user_email,password,user_secret_key)#用户登录
    mer_header=wq.login_email(mer_email,password,mer_secret_key)#商家登录
    wal = wp.otc_assets(headers1=user_headers)#获取otc的资产
    wq.code_msg_api(wal)#判断接口是否报错
    cw = wp.orders_select(headers1=mer_header)  # 获取广告id
    id = cw['data'][0]['id']
    minPlacePrice=cw['data'][0]['minPlacePrice']
    exchangeRate = cw['data'][0]['exchangeRate']
    amount = (minPlacePrice / exchangeRate * 1.02)
    cd = ast.literal_eval(cw['data'][0]['paySupport'])
    for tmp in cd:
        if tmp['name'] == '支付宝':
            bankcard = tmp['id']
            print(bankcard)
    gol = wd.read_google_authenticator_code(secret_key=user_secret_key)  # 获取用户谷歌验证码
    qw = wp.otc_pendings(headers3=user_headers, id=id, exchangeRate=exchangeRate, amount="%.8f" % amount,googleVerifyCode=gol) # 根据广告id下单
    print(amount)
    wq.code_msg_api(qw)
    orid = qw['data']['id']
    cw = wp.otc_pendings_paid(orderid=orid, headers3=da.headers4, payment=bankcard)  # 用户点击已付款
    wq.code_msg_api(cw)
    gol = wd.read_google_authenticator_code(secret_key=mer_secret_key)  # 获取商家谷歌验证码
    aw = wp.otc_pendings_complete(headers3=mer_header, orderid=orid, googleVerifyCode=gol, tradePassword=password)  # 确认放币
    wq.code_msg_api(aw)
    ca = wp.otc_pendings_send(orid=orid,headers=mer_header)
    buyerInAmount = ca['data']['buyerInAmount']#交易数量
    platformCommission = ca['data']['platformCommission']#手续费
    orderTotal = ca['data']['orderTotal']#订单总额
    exchangeRate = ca['data']['exchangeRate']#价格
    print(buyerInAmount,platformCommission,orderTotal,exchangeRate)
def otc_called():#撤消用户所有进行中订单
    user_headers = wq.login_email(user_email, password, user_secret_key)  # 用户登录
    ca = wp.otc_pendings_status(98,user_headers)
    orderId=[]
    for tmp in ca['data']['items']:
        orderId.append(tmp['id'])
    print(orderId)
    for i in range(0,len(orderId)):
        sa=wp.otc_cancel(orderId[i],user_headers)
        time.sleep(1)
        print(sa)



if __name__ == '__main__':
    print(otc_buy())
    #print(otc_called())

