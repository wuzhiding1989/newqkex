from common import mysql_san as sql1
data = [
    [96.07843137, None],
    [100, None]
]
def mysql_fee_selec(user_id,legal_symbol,symbol):#通过数据库获取用户数据计算广告费率
    sql = f"SELECT a.fee_rate,b.`status`, b.ratio,b.target_uid AS s_uid ,b.source_uid as f_uid,(SELECT platform_commission_rate FROM OTC.config_currency WHERE symbol='{symbol}' AND legal_symbol='{legal_symbol}') AS fee FROM OTC.user_info a,OTC.rebate_config b WHERE a.user_id=b.source_uid AND a.user_id in ({user_id})"
    wss = sql1.mysql_select(sql)
    fee_rate = wss[0][0];status = wss[0][1];ratio = wss[0][2];target_uid = wss[0][3];source_uid = wss[0][4];fee = wss[0][5]
    print('基于数据库''uid=', target_uid, f'法币为{legal_symbol}的币种{symbol}费率=', fee, '折扣=', fee_rate, '溢价率=',
          ratio, 'uid=', target_uid, '返佣关系(1正常0暂停)=', status)
    # print(fee_rate,status,ratio,source_uid,fee)
    if status==0:
        print('返佣关系暂停，不存在返佣')
    else:
        if fee_rate==0:
            fee_2 = fee * (1+ ratio)#币种费率*(1+溢价率)# cc="{:.2f}%".format(fee_1*100) #转换成功百分比
            return fee_2
        else:
            fee_1 = (fee * fee_rate + fee * ratio)#币种费率*手续折扣+手续费溢价率*币种费率,
            return fee_1
def otc_ratiofee(fee_rate,status,ratio,fee,account,cc):#计算费率返佣的
    print('基于币种费率=',fee,'折扣=',fee_rate,'溢价率=',ratio,'数量=',account,'返佣关系(1正常0暂停)=',status)
    if status==0:
        print('返佣关系暂停，不存在返佣关系')
        fee_1=fee * fee_rate
        print('手续费率为', "{:.2f}%".format(fee_1 * 100))
        cee = account * fee_1
        print('订单收取手续费为', cee)
    else:
        if fee_rate==0:
            fee_2 = fee * (1+ ratio)#币种费率*(1+溢价率)
            print('手续费率为',"{:.2f}%".format(fee_2*100))
            cee=account * fee_2
            print('订单收取手续费为',cee)
            f_fee=  fee_2 - fee
            feea = account * f_fee
            print(cc,'返佣手续费为',feea)
            order_account=account/(1+fee_2)
            print('若数量为发布广告数量，则可售数量为',order_account)
        else:
            fee_1 = (fee * fee_rate + fee * ratio)#币种费率*手续折扣+手续费溢价率*币种费率,
            print('手续费率为',"{:.8f}%".format(fee_1*100))
            cee = account * fee_1
            print('订单收取手续费为', "{:.8f}".format(cee))
            f_fee = fee_1 - (fee * fee_rate)
            feea = (account) * (f_fee)
            print('返佣手续费为' "{:.8f}".format(feea))
            order_account = account / (1 + fee_1)
            print('若数量为发布广告数量，则可售数量为', order_account)





if __name__ == '__main__':
    for tmp in data:
        c=otc_ratiofee(fee_rate=0,status=1,ratio=1,fee=0.01,account=tmp[0],cc=tmp[1])
        print(c)
    # a=mysql_fee_selec(user_id=10122165,legal_symbol='usd',symbol='ETH')
    # print(a)