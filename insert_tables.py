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
