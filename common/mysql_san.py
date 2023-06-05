import pymysql
#from common import util as u
host='database-1.cnxpymarugg3.ap-southeast-1.rds.amazonaws.com'
user='admin'
password='6Gp0iz1ZHNceJKwSpNg6'
database='otc'
from decimal import Decimal as d
#sql='SELECT available_balance FROM assets WHERE id=4594227'
sql="SELECT a.fee_rate,b.`status`, b.ratio,b.target_uid AS s_uid ,b.source_uid as f_uid,(SELECT platform_commission_rate FROM config_currency WHERE symbol='btc' AND legal_symbol='usd') AS fee FROM user_info a,rebate_config b WHERE a.user_id=b.source_uid AND a.user_id in (10122165)"
def mysql_select(sql):#根据主库,返回内容,查询表,查询条件进行查询
    db = pymysql.connect(host=host, user=user, password=password, database="")# 打开数据库连接
    cursor = db.cursor()# 使用cursor()方法获取操作游标
    sql = sql# 执行SQL语句
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()# 关闭数据库连接
    return data
def sql_send(sql):
    id=[]
    res = mysql_select(sql)
    for tmp in res:
        id.append(tmp[0])
    return id
def mysql_execute(sql):#修改数据库内容或拆入数据
    db = pymysql.connect(host=host, user=user, password=password, database="")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print("执行成功")
    except:
        db.rollback()
        print("执行失败")
    db.close()
def add_account(uid,currency,balance):#给钱包价钱，加到钱包账户
    sql_select = f"SELECT balance FROM wallet.user_balance WHERE user_id in ({uid}) AND parent_symbol='{currency}' AND currency_id=0"
    install_select = f"INSERT INTO wallet.user_balance ( `currency_id`, `parent_symbol`, `user_id`, `balance`, `create_on`, `update_on`) VALUES ( 0, '{currency}', {uid}, {balance}, '2023-02-22 11:08:19', '2023-02-25 14:30:41')"
    updata_select = f"UPDATE wallet.user_balance SET balance = '{balance}' WHERE parent_symbol ='{currency}' AND currency_id=0 AND user_id in ({uid})"
    abc=mysql_select(sql_select)
    if len(abc)==0:#判断钱包是否有数据
        a=mysql_execute(install_select)
        print(a,install_select)
    else:
        a=mysql_execute(updata_select)
        print(updata_select,a)

if __name__ == '__main__':
    # user_id=10122165; legal_symbol='usd'; symbol='btc'
    # sql = f"SELECT a.fee_rate,b.`status`, b.ratio,b.target_uid AS s_uid ,b.source_uid as f_uid,(SELECT platform_commission_rate FROM OTC.config_currency WHERE symbol='{symbol}' AND legal_symbol='{legal_symbol}') AS fee FROM OTC.user_info a,OTC.rebate_config b WHERE a.user_id=b.source_uid AND a.user_id in ({user_id})"
    # a = mysql_select(sql)
    # print(a)
    print(add_account(uid='10122307',currency="USDT",balance='70090000.98'))