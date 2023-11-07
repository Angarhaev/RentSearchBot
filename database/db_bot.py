import pymysql
from config_db import host, user_name, password, db_name

try:
    connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user_name,
        password = password,
        database = db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('successfully connected...')
    print('#' * 20)
    try:
        with connection.cursor() as cursor:
            create_table_query = ("CREATE TABLE IF NOT EXISTS `users` (id int AUTO_INCREMENT,"
                                  " name varchar(32),"
                                  " password varchar(32),"
                                  " email varchar(32), PRIMARY KEY (id));")
            cursor.execute(create_table_query)
            print('get ready to work...')
    finally:
        connection.close()

except Exception as ex:
    print('connection refused...')
    print(ex)
# https://www.youtube.com/watch?v=LS42t1VMwuM&ab_channel=PythonToday
