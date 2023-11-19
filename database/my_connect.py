from pymysql.cursors import DictCursor
from pymysql import connect


def create_connection(con_host, con_user_name, con_password, con_db_name):
    connection = None
    try:
        connection = connect(
            host=con_host,
            port=3306,
            user=con_user_name,
            password=con_password,
            database=con_db_name,
            cursorclass=DictCursor
        )
        print('Соединение с базой данных установлено...')
        print('#' * 20)

    except Exception as ex:
        print('Ошибка соединения с базой данных...')
        print(ex)

    return connection
