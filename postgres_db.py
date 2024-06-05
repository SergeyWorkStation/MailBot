import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def database_request(query):
    dbname, user, password, host, port = config['database'].values()
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        # print('Successfully connection to database')
        with conn.cursor() as cursor:
            cursor.execute(query=query)
    except Exception as e:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')
        print(e)
    finally:
        if conn:
            conn.close()
            # print("Connection closed")


def database_response(query):
    dbname, user, password, host, port = config['database'].values()
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        # print('Successfully connection to database')
        with conn.cursor() as cursor:
            cursor.execute(query=query)
            return cursor.fetchall()
    except Exception as e:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        print('Can`t establish connection to database')
        print(e)
    finally:
        if conn:
            conn.close()
            # print("Connection closed")