from postgres_db import database_response


def get_all_post(chat_id):
    return database_response(f"""SELECT email
                                FROM posts
                                WHERE user_id=(SELECT user_id
                                                FROM users
                                                WHERE chat_id='{chat_id}'
                                                LIMIT 1)
                                ORDER BY email;""")