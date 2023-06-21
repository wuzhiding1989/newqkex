from common import mysql_san as sql
sql_query = "SELECT user_id, symbol, available_balance, frozen_balance, available_balance + frozen_balance AS total_asset FROM otc.assets ORDER BY user_id DESC"
result = sql.mysql_select(sql_query)
#print(result)
print(len(result))
# for tmp in result:
#     print(tmp)

from datetime import datetime

# 获取当前时间并转换为字符串
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# 创建一个新文件，并命名为当前时间
filename = f"{timestamp}.txt"

with open(filename, 'w') as f:
    # 遍历每个元组，并将元素按照指定格式转换为字符串，然后写入文件中
    for row in result:
        row_str = ', '.join(str(x) for x in row) + '\n'
        f.write(row_str)
        print(row_str)

# 关闭文件
f.close()
