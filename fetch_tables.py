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


def get_all_users():
    return database_response(f"""SELECT *
                                FROM users;""")


def get_post_by_id(post_id):
    result = database_response(f"""SELECT email, password, post_id
                                FROM posts
                                WHERE post_id={post_id};""")[0]
    result = (result[0], decrypt(result[1]), result[2])
    return result


def get_all_rules(post_id):
    return database_response(f"""SELECT email, name_data_type, rule_id
                                FROM rules INNER JOIN data_type USING(data_type_id)
                                WHERE post_id='{post_id}'
                                ORDER BY email;""")


def get_all_data_type():
    return database_response(f"""SELECT *
                                FROM data_type;""")


def get_name_data_type(data_type_id):
    return database_response(f"""SELECT name_data_type
                                FROM data_type
                                WHERE data_type_id={int(data_type_id)};""")[0][0]


def get_data_massage():
    result = database_response(f"""SELECT chat_id, posts.email, password, rules.email, data_type_id
                                    FROM users
                                        INNER JOIN posts USING(user_id)
                                        INNER JOIN rules USING(post_id);""")
    return [(i[0], i[1], decrypt(i[2]), i[3], i[4]) for i in result]
