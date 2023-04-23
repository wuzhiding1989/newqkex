qa_mysql_server=['database-1.cnxpymarugg3.ap-southeast-1.rds.amazonaws.com',3306,'admin','6Gp0iz1ZHNceJKwSpNg6']
# NTS_tidb_server=['52.196.5.46',4000,'qa_mulan','eZZBNymY_RbWHy8q']
# NTS_mysql_server=['future-uat-manager-mysql.clmrvlqzouao.ap-northeast-1.rds.amazonaws.com',3306,'qa_mulan','eZZBNymY_RbWHy8q']
# mysql_ip = '172.18.6.71';mysql_port = 3306;mysql_user='linear_contract';mysql_password = 'linear_contract@123'
mysqlHost={
     3 :qa_mysql_server
    # ,6:[NTS_tidb_server],7:NTS_mysql_server
}
#123456789
dbList={
    "20l":{"ex1":"linear_order_seq1","btc1":"linear_btc","btc2":"linear_eos"},
    "20hl":{"ex1":"linear_order_seq","btc1":"linear_btc","btc2":"linear_eos"}}