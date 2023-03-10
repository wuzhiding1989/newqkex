import time

import pymysql
from config.mysqlConfig import mysqlHost

class mysql():
    def __init__(self,server,product=None):
        mysql_server=mysqlHost[server]
        if product : mysql_server=mysqlHost[server][product-1]
        self.serverIP=mysql_server[0];self.serverPort=mysql_server[1];self.serverUserName=mysql_server[2];self.serverPassword=mysql_server[3]
        # print(mysql_server);#time.sleep(100)
    def dbExcute(self,db, sql):
        try:
            cursor = db.cursor();cursor.execute(sql);db.commit();data = cursor.fetchall()
            return data    #连接mysql，执行sql语句
        except Exception as e:  print(e)
    def _init(self,ret):
        result = str(ret).replace('(', '').replace(',)', '').replace(' ', '')
        return result#[0:-1]
    def mysql(self,sql,init=None):
        # env_mysql(server,product=product)
        defaultdb = 'mysql'
        # if str(server)[-1:]==conf.contract_flag:
        #     if product=='order_seq': defaultdb='mysql'
        #     else: defaultdb='mysql'
        # if str(server)[-1:]==conf.swap_flag:    defaultdb='contract_trade'
        # if str(server)[-1:] == conf.linear_flag:    defaultdb = 'linear_contract_trade'
        db = pymysql.connect(host=self.serverIP, port=self.serverPort, user=self.serverUserName, passwd=self.serverPassword, db=defaultdb,charset='utf8')
        ret=self.dbExcute(db, sql)
        if not init: return self._init(ret)
        else: return ret


# t=mysql('3').mysql('select * from mulan_btc1.t_trade')
# print(t)