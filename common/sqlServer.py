import pyodbc

def query_sql_server(query):
    try:
        # 修改为实际的服务器名、数据库名、用户名和密码
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=121.37.233.153;'
                              'Database=MuOnline;'
                              'uid=sa;'
                              'pwd=Wu23314902;')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    query = 'select * from dbo.AccountCharacter'
    print(query_sql_server(query))