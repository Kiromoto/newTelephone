import pyodbc

def getConnectionPyodbc(server='10.10.12.150', user='sa', password='3086993GKSE', database='PhoneBookGKSE', *args, **kwargs):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 15 for SQL Server}; SERVER=server; DATABASE=database; UID=user; PWD=password')
        cur = conn.cursor()
    except Exception as e:
        print(f'Ошибка подключения к базе данных {database}: {e}')
        return None
    else:
        print(f'Подключение к базе данных {database} выполнено успешно!')
        return cur, conn


