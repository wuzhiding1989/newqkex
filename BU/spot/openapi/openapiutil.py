import time
from common.mysql_san import mysql_select
from common import util as u
from BU.spot.openapi import api
def sql_order_id(pairCode,order_id): ####判断订单是否成交,1挂单未成交2已完成3已撤销4挂单部分成交5已撤单部分成交
    sql_id = f"SELECT CASE WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_orders WHERE id ={order_id} AND deal_amount=0) THEN 1 " \
         f"WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_order_fulfillment WHERE id = {order_id} AND `status`=2) THEN 2 " \
         f"WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_order_fulfillment WHERE id ={order_id} AND `status`=-1 AND deal_quote_amount=0) THEN 3 " \
         f"WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_orders WHERE id = {order_id} AND deal_amount!=0) THEN 4 " \
         f"WHEN EXISTS (SELECT 1 FROM exchange.{pairCode}_order_fulfillment WHERE id = {order_id} AND `status`=-1 AND deal_quote_amount!=0) THEN 5 " \
         f"END AS idc"
    order_status = mysql_select(sql_id)
    return order_status

#状态4的调试
# c=u.d(newquote_available) + u.d(averagePrice) * u.d(amount) - u.d(quote_available)#usdt可用
# x=u.d(newbase_hold)-u.d(base_hold)#ada不可用
# s=u.d(newbase_available) - u.d(dealAmount)- u.d(dealAmount) * u.d(m_fee) -u.d(base_available)#ada可用
# sd=u.d(newquote_hold)- u.d(openAmount)*u.d(price1)-u.d(quote_hold)#usdt不可用
# print(c,s,sd,x)



def te_test1(locale='en-US',side='buy',pairCode='ADA_USDT',systemOrderType='limit',price1='0.3109',volume='58'):#zh-HK,en-US
    base=(u.symbolbase(pairCode))['base'];quote=(u.symbolbase(pairCode))['quote']
    buyprice=(u.price(pairCode))['bid'][0];sellprice=(u.price(pairCode))['ask'][0]
    print(buyprice,sellprice)
    baseassets = api.assets(base);quoteassets = api.assets(quote)
    base_available = baseassets['available'];base_hold = baseassets['hold']
    quote_available = quoteassets['available'];quote_hold = quoteassets['hold']
    t_fee=u.exchange_fee(pairCode=pairCode)['tickerFeesRate'];m_fee=u.exchange_fee(pairCode=pairCode)['makerFeesRate']
    print(12,t_fee,m_fee)
    print(f'{base}初始可用资产为{base_available},初始冻结资产为{base_hold},{quote}初始可用资产为{quote_available},初始冻结资产为{quote_hold}')
    if side=='buy':
        order_id = api.order(pairCode=pairCode, side=side, price=price1, volume=volume, systemOrderType=systemOrderType,
                         source='api',locale=locale)
        time.sleep(4)
        print(order_id)
        order_status=sql_order_id(pairCode,order_id)
        print(f'当前订单状态为{order_status[0][0]}')
        baseassets1 = api.assets(base);quoteassets1 = api.assets(quote)
        newbase_available = baseassets1['available'];newbase_hold = baseassets1['hold']
        newquote_available = quoteassets1['available'];newquote_hold = quoteassets1['hold']
        if order_status[0][0]==1:#订单未成交
            if u.d(newquote_available) + u.d(price1)*u.d(volume) -u.d(quote_available) ==0 \
                    and u.d(newquote_hold) - u.d(price1)*u.d(volume) -u.d(quote_hold) ==0 \
                    and u.d(newbase_hold) - u.d(base_hold)==0 \
                    and u.d(newbase_available) - u.d(base_available)==0:
                print(f'挂单后的{base}和{quote}可用资产和冻结资产检验正确')
            else:
                print(f'资产1校验失败,{base}变化后可用资产为{newbase_available},变化后冻结资产为{newbase_hold},{quote}变化后可用资产为{newquote_available},变化后冻结资产为{newquote_hold}')
        elif order_status[0][0]==2:#订单已成交
            his=u.openapi_order_History(pairCode=pairCode,id=order_id)
            averagePrice=his['averagePrice']
            if  u.d(newquote_available) + u.d(averagePrice) * u.d(volume) - u.d(quote_available) == 0\
                    and u.d(newbase_available) - u.d(volume)- u.d(volume) * u.d(m_fee) -u.d(base_available) == 0 \
                    and u.d(newbase_hold)-u.d(base_hold)==0 \
                    and u.d(newquote_hold)-u.d(newquote_hold)==0:
                print(f'交易完成后的{base}和{quote}可用资产和冻结资产检验正确')
            else:
                print(f'资产2校验失败,{base}变化后可用资产为{newbase_available},变化后冻结资产为{newbase_hold},{quote}变化后可用资产为{newquote_available},变化后冻结资产为{newquote_hold}')
        elif order_status[0][0]==3:
            print('待补充3')
        elif order_status[0][0]==4:#挂单部分成交
            op=u.openapi_order(pairCode=pairCode,id=order_id)
            amount=op['amount'];averagePrice=op['averagePrice'];dealAmount=op['dealAmount'];openAmount=op['openAmount']
            if u.d(newquote_available) + u.d(averagePrice) * u.d(amount) - u.d(quote_available) == 0 \
                and u.d(newbase_available) - u.d(dealAmount)- u.d(dealAmount) * u.d(m_fee) -u.d(base_available)== 0 \
                and u.d(newquote_hold)- u.d(openAmount)*u.d(price1)-u.d(quote_hold)== 0 \
                and u.d(newbase_hold)-u.d(base_hold)==0:
                print(f'交易完成后的{base}和{quote}可用资产和冻结资产检验正确')
            else:
                print(f'资产4校验失败,{base}变化后可用资产为{newbase_available},变化后冻结资产为{newbase_hold},{quote}变化后可用资产为{newquote_available},变化后冻结资产为{newquote_hold}')
        elif order_status[0][0]==5:
            print('待补充5')
        #print(f',{base}变化后可用资产为{newbase_available},变化后冻结资产为{newbase_hold},{quote}变化后可用资产为{newquote_available},变化后冻结资产为{newquote_hold}')

    else:
        assets1 = api.assets(base)
        available = assets1['available'];hold = assets1['hold']
        print(f'{base}初始可用资产为{available},初始冻结资产为{hold}')
        order_id = api.order(pairCode=pairCode, side=side, price='0.0803', volume='310', systemOrderType=systemOrderType,
                         source='api', locale=locale)
        time.sleep(2)
        print(order_id)
        data = api.orders(pairCode=pairCode)
        ids = [item['id'] for item in data]
        sql_select = f"SELECT id,side,entrust_price,amount,entrust_price*amount,source_info,`status` FROM exchange.qk_usdt_orders WHERE id={order_id}"
        cc = mysql_select(sql_select)
        print(ids)
        print('数据库查询订单数据', cc)
        if order_id in ids:
            print("当前委托订单包含当前订单id")
        else:
            print("当前委托订单不包含当前订单id")
        assets2 = api.assets(base)
        available1 = assets2['available'];
        hold1 = assets2['hold']
        ava = u.d(available) - u.d(available1);
        una = u.d(hold1) - u.d(hold)
        print(f'{base}变化后可用资产为{available1},变化后冻结资产为{hold1},可用减少了{ava},冻结增多了{una}')

if __name__ == '__main__':
    print(te_test1())
    #print(sql_order_id('ADA_USDT','171960320359488'))