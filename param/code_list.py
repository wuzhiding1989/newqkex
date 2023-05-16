
# 定义所有的code码

code_list={
    "success": ['1',"返回正常"],
    "system": ["1001","系统异常，请稍后再试"],
    "visitsnumber": ["1002","超过访问次数，请稍后再试"],
    "symbolstatus": ["1003","当前交易对处于非交易状态，请稍后再试"],
    "maxorderqty": ["1004","超过单笔下单委托数量，请修改委托数量"],
    "tradetype": ["1005","业务类型不合法，请修改"],
    "symbol": ["1006","交易对不存在，请修改"],
    "side": ["1007","交易方向不合法，请修改"],
    "positionside": ["1008","持仓方向不合法，请修改"],
    "ordertype": ["1009","订单类型不合法，请修改"],
    "margintype": ["1010","保证金模式不合法，请修改"],
    "timeinforce": ["1011","订单策略不合法，请修改"],
    "orderid": ["1012","订单号不合法，请修改"],
    "lever": ["1013","超过最大杠杆，请修改"],
    "clordid": ["1014","客户订单号不合法，请修改"],
    "orderqty": ["1015","委托数量不合法，请修改"],
    "available": ["1016","可用保证金不足"],
    "risklimit": ["1017","风险限额超出限制"],
    "closeqty": ["1018","可平量不足"],
    "mustparam": ["1019","必要参数为空:{%s}"],
    "param": ["1020","参数错误:{%s}"],
    "odernone": ["1021","订单不存在"],
    "leverparam": ["1028","杠杆倍数有误"],
    "price": ["1033","价格不合法"],
    "transfercurrency": ["1035","币种不合法"],
    "transferqty": ["1044","可转不足"],
    "paramwrong": ["1046","{0}字段不合法,请重新输入"],
    "orderprice": ["1045","	订单价格超过限制"],
    "paramnull": ["1047","{0}字段不能为空,请重新输入"],
    "transferaccounttype": ["1048","账户类型错误"],
    "transferamount": ["1049", "划转数量不合法"],
    "type": ["1050", "保证金类型错误"],
    "orderstatus": ["1020","参数错误:{%s}"],  # 目前还没定义orderStatus错误码，传参".@#$%^&^&*",返回1020，产品已确认接1020
}

# pageNum、pageSize、startTime、endTime #目前还没定义单独错误码，传参".@#$%^&^&*",返回["1046","{0}字段不合法,请重新输入"]