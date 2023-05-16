from common.util import request_http as req,truncate,printc,printl,d,requests,priceSpread,t as _t,countCaseNumber as u,Count
import common.util as ut
import common.mysqlClient as mysql

#开仓maker手续费 验证
def OpenMakerFeeCheck(NTS,log_level=None):
    db = mysql.mysql(NTS.server, 1)
    dbName = 'qa_mulan_btc1.';title='<历史成交 开仓maker 手续费费率 所有用户> 验证'
    sql='select * from (select a.filled_price*a.filled_qty*0.01*0.0002 fee,a.commission,a.uid,a.order_id,a.symbol from '+dbName+'t_trade a left join '+dbName+'t_order b on a.order_id=b.order_id where  a.role="maker" and b.create_date>"2022-09-28" and a.id>0 and a.position_side=a.side) c where c.fee!=c.commission or c.fee is null '
    r = db.mysql(sql,init=True);
    if r.__len__()==0: printl(log_level,title+'成功');u(1);return True;
    else: u(0);printc(title+'失败'+str(r.__len__()),r);return False;
#平仓maker手续费 验证
def CloseMakerFeeCheck(NTS,log_level=None):
    db = mysql.mysql(NTS.server, 1)
    dbName = 'qa_mulan_btc1.';title='<历史成交 平仓maker 手续费费率 所有用户> 验证'
    sql='select * from (select a.filled_price*a.filled_qty*0.01*0.0002 fee,a.commission,a.uid,a.order_id,a.symbol from '+dbName+'t_trade a left join '+dbName+'t_order b on a.order_id=b.order_id where  a.role="maker" and b.create_date>"2022-09-28" and a.id>0 and a.position_side!=a.side) c where c.fee!=c.commission or c.fee is null '
    r = db.mysql(sql,init=True);
    if r.__len__()==0: printl(log_level,title+'成功');u(1);return True;
    else: u(0);printc(title+'失败'+str(r.__len__()),r);return False;

#开仓taker手续费 验证
def OpenTakerFeeCheck(NTS,log_level=None):
    db = mysql.mysql(NTS.server, 1)
    dbName = 'qa_mulan_btc1.';title='<历史成交 开仓taker 手续费费率 所有用户> 验证'
    sql='select * from (select a.filled_price*a.filled_qty*0.01*0.0004 fee,a.commission,a.uid,a.order_id,a.symbol from '+dbName+'t_trade a where  a.role="taker" and create_date>"2022-09-27" and id>0 and position_side=side) c where c.fee!=c.commission or c.fee is null;'
    r = db.mysql(sql,init=True);
    if r.__len__()==0: printl(log_level,title+'成功');u(1);return True;
    else: u(0);printc(title+'失败'+str(r.__len__()),r);return False;

#平仓taker手续费 验证
def CloseTakerFeeCheck(NTS,log_level=None):
    db = mysql.mysql(NTS.server, 1)
    dbName = 'qa_mulan_btc1.';title='<历史成交 平仓taker 手续费费率 所有用户> 验证'
    sql='select * from (select a.filled_price*a.filled_qty*0.01*0.0004 fee,a.commission,a.uid,a.order_id,a.symbol from '+dbName+'t_trade a where  a.role="taker" and create_date>"2022-09-27" and id>0 and position_side!=side) c where c.fee!=c.commission or c.fee is null;'
    r = db.mysql(sql,init=True);
    if r.__len__()==0: printl(log_level,title+'成功');u(1);return True;
    else: u(0);printc(title+'失败'+str(r.__len__()),r);return False;

def FeeCase(NTS,log_level=None):
    r=CloseTakerFeeCheck(NTS,log_level=log_level);
    Count('手续费计算',1,1,0,0) if r else Count('手续费计算',1,0,1,0)
    r=OpenTakerFeeCheck(NTS, log_level=log_level)
    Count('手续费计算', 1, 1, 0, 0) if r else Count('手续费计算', 1, 0, 1, 0)
    r=OpenMakerFeeCheck(NTS, log_level=log_level)
    Count('手续费计算', 1, 1, 0, 0) if r else Count('手续费计算', 1, 0, 1, 0)
    r=CloseMakerFeeCheck(NTS, log_level=log_level)
    Count('手续费计算', 1, 1, 0, 0) if r else Count('手续费计算', 1, 0, 1, 0)
if __name__ == '__main__':
    from BU.NTS.WebOrder import n_order
    NTS = n_order(6, user_id=97201967);
    FeeCase(NTS,0)
    print('【Case】', '总数:', ut._all, '通过:', ut._pass, '失败:', ut._all - ut._pass - ut._block, '阻塞:', ut._block,'通过率: ' + str(truncate(ut._pass / ut._all * 100, 2)) + '%');
