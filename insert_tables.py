from postgres_db import database_request
from crypt import encrypt


def insert_user(name_user, chat_id):
    database_request(f"""INSERT INTO users(name_user, chat_id)
                            SELECT '{name_user}', '{chat_id}'
                            WHERE NOT EXISTS (SELECT 1 
                                                FROM users 
                                                WHERE chat_id = '{chat_id}');""")


def insert_post(email, password, chat_id):
    encrypted_password = encrypt(password)
    database_request(f"""INSERT INTO posts(email, password, user_id)
                            SELECT '{email}', '{encrypted_password}', user_id
                            FROM users
                            WHERE chat_id = '{chat_id}';""")


def insert_data_type():
    database_request(f"""INSERT INTO data_type(name_data_type)
                                VALUES ('Всё содержание писем'), ('Файлы из писем'), ('Текст из писем');""")


def insert_rule(post_id, email, data_type_id):
    database_request(f"""INSERT INTO rules(post_id, email, data_type_id)
                            VALUES ({int(post_id)}, '{email}', {int(data_type_id)});""")
