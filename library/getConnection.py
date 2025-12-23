import pymssql
import os
from dotenv import load_dotenv



load_dotenv()

def getConnection(server=os.getenv('server'), user=os.getenv('user'), password=os.getenv('password'), database=os.getenv('database'), *args, **kwargs):
    try:
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        cur = conn.cursor()
    except Exception as e:
        print(f'Ошибка подключения к базе данных {database}: {e}')
        return None
    else:
        print(f'Подключение к базе данных {database} выполнено успешно!')
        return cur, conn


