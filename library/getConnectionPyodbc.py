import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


def getConnectionPyodbc(server=os.getenv('server'), user=os.getenv('user'), password=os.getenv('password'),
                        database=os.getenv('database'), *args, **kwargs):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 15 for SQL Server}; SERVER=server; DATABASE=database; UID=user; PWD=password')
        cur = conn.cursor()
    except Exception as e:
        print(f'Ошибка подключения к базе данных {database}: {e}')
        return None
    else:
        print(f'Подключение к базе данных {database} выполнено успешно!')
        return cur, conn
