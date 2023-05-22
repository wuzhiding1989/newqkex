import copy
from common.util import printc,printl, LogOut
import BU.NTS.dataCheck.Formula as Formula
from BU.NTS.WebOrder import n_order as WebOrder
from UnitTest.com import GetAllUsers
import datetime
from UnitTest.com import LogName
from param.dict import SuccessMessage
import common.mysqlClient as mysql
from common.util import Count
import UnitTest.AOP as AOP
symbol='BTCUSDT'
def PlatFrozenAmoutCheck(log_level=None):
    # AllUsers=GetAllUsers()
    ForNumber=0
    for user_id in GetAllUsers():

    # if 1==1:

        if user_id not in ["97121927"]: #临时排除一些 异常用户的数据
            ForNumber+=1
            NTS = WebOrder(6, user_id=user_id) #user_id
            S=datetime.datetime.now();
            F=Formula.Formula(NTS,symbol)  #
            F.FrozenPositionAssert(log_level=log_level)  #4 - 冻结仓位数量验证
            F.FrozenMarginAssert(log_level=log_level)  # 1- 挂单冻结金额结果 验证
            # F.PositionAssert(log_level= 0) #2-持仓验证
            # F.AccountAssert(log_level= 0) #3-资金
                ###🀆🀆🀆🀆🀆★★★★★Assert 平台仓位数量对账 ★★★★★🀆🀆🀆🀆🀆
            Aop=AOP.AOP(NTS, symbol=symbol, _type=3)
            if ForNumber==1:
                PlatPositonDict={};BasicPositionDict={"long":0,"short":0}
                for i in Aop.instrumentList:
                    PlatPositonDict[i]=copy.deepcopy(BasicPositionDict)
                #将每个用户的持仓数据放到平台的持仓数据中
            for Symbol in Aop.Positions:
                for MarginType in Aop.Positions[Symbol]:
                    for PositionSide in Aop.Positions[Symbol][MarginType]:
                        Temp_Position=Aop.Positions[Symbol][MarginType][PositionSide]
                        if float(Temp_Position['PositionAmt'])>0:
                            PlatPositonDict[Symbol][PositionSide]+=float(Temp_Position['PositionAmt'])
            # print(NTS.user_id,PlatPositonDict)
            # 将每个用户的汇总持仓数据 加到日志中
            LogOut(f'{NTS.user_id}{PlatPositonDict}',LogName)
    #开始仓位对账
    for Symbol in PlatPositonDict:
        if not PlatPositonDict[Symbol]['long']==PlatPositonDict[Symbol]['short']:
            ErrorMessage=f'{Symbol} 平台仓位对账不平: {PlatPositonDict[Symbol]}';
            printc(ErrorMessage);LogOut(ErrorMessage,LogName);CaseResult=False
        else:
            printl(log_level,f'{Symbol} 平台仓位对账{SuccessMessage}');CaseResult=True;
    temp=Count('平台仓位对账',1,1,0,0) if CaseResult else Count('平台仓位对账',1,0,1,0)
    E = datetime.datetime.now();
    print('耗时', str((E - S))[:-3]);
def Db_Check():
    db = mysql.mysql(6, 1)
    dbName = 'qa_mulan_btc1.'
    sql=f'select * from (SELECT a.uid,a.side,a.event_type, (case a.event_type when 13 then a.order_qty when 14 then a.order_qty*-1 end) as order_qty,concat("",a.create_date) create_date,concat("",b.income) income,b.income_type,b.details,concat("",b.create_date) as create_date2 from {dbName}t_order a,{dbName}t_account_action b where a.order_id=b.order_id and a.leverage=0 and b.income_type=1 ) a where create_date!=create_date2 or income_type!=1 or details not in (1,2) or event_type not in (13,14) or order_qty!=income'
    r = db.mysql(sql,init=True)
    if r.__len__()>0:
        printc('平台划转订单和流水不一致')
        for i in r : printc(r)

    sql=f'select * from {dbName}t_trade where  order_id not in ( SELECT order_id from {dbName}t_account_action);'
    r = db.mysql(sql, init=True)
    if r.__len__() > 0:
        printc('成交表数据在流水表不存在')
        for i in r: printc(r)

    sql=f'select * from {dbName}t_order where  leverage>0  and order_status not in (4) and order_id not in ( SELECT order_id from {dbName}t_account_action )'
    r = db.mysql(sql, init=True)
    if r.__len__() > 0:
        printc('订单表成交数据在流水表不存在')
        for i in r: printc(r)

    sql=f'select * from {dbName}t_account_action where income_type!=1  and order_id not in ( SELECT order_id from {dbName}t_trade)'
    r = db.mysql(sql, init=True)
    if r.__len__() > 0:
        printc('流水表成交数据在成交表不存在')
        for i in r: printc(r)

    sql=f'select * from {dbName}t_order where leverage=0 and order_id not in (SELECT order_id from {dbName}t_account_action)'
    r = db.mysql(sql, init=True)
    if r.__len__() > 0:
        printc('划转流水数据在订单表不存在')
        for i in r: printc(r)

    sql = f'select * from {dbName}t_account_action where income_type=1 and order_id not in (SELECT order_id from {dbName}t_order)'
    r = db.mysql(sql, init=True)
    if r.__len__() > 0:
        printc('划转订单表在流水表不存在')
        for i in r: printc(r)
    # for i in r: print(r)
if __name__ == '__main__':
    PlatFrozenAmoutCheck(0)
    Db_Check()
# Count(summary=1, log_level=2, SendSlack=False, title=f' 111 ')
