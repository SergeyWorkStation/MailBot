from postgres_db import database_response
from crypt import decrypt


def get_all_post(chat_id):
    result = database_response(f"""SELECT email, password, post_id
                                FROM posts
                                WHERE user_id=(SELECT user_id
                                                FROM users
                                                WHERE chat_id='{chat_id}'
                                                LIMIT 1)
                                ORDER BY email;""")
    return [(i[0], decrypt(i[1]), i[2]) for i in result]


def get_post_by_id(post_id):
    result = database_response(f"""SELECT email, password, post_id
                                FROM posts
                                WHERE post_id={post_id};""")[0]
    result = (result[0], decrypt(result[1]), result[2])
    return result
