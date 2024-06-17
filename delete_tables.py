from postgres_db import database_request


def delete_post(post_id):
    database_request(f"""DELETE FROM posts
                            WHERE post_id={int(post_id)};""")
