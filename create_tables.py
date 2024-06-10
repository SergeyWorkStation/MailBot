from postgres_db import database_request


def create_table():
    database_request("""CREATE TABLE IF NOT EXISTS users( 
                           user_id serial PRIMARY KEY,
                           name_user varchar(30),
                           chat_id varchar(30) NOT NULL);
                        CREATE TABLE IF NOT EXISTS data_type( 
                           data_type_id serial PRIMARY KEY,
                           name_data_type varchar(30) NOT NULL);
                        CREATE TABLE IF NOT EXISTS posts( 
                           post_id serial PRIMARY KEY,
                           email varchar(45) NOT NULL,
                           password varchar(45) NOT NULL,
                           user_id int NOT NULL,
                           FOREIGN KEY (user_id)  
                           REFERENCES users (user_id) ON DELETE CASCADE);
                        CREATE TABLE IF NOT EXISTS rules( 
                           rule_id serial PRIMARY KEY,
                           post_id int NOT NULL,
                           email varchar(45) NOT NULL,
                           data_type_id int NOT NULL,
                           FOREIGN KEY (post_id)  
                           REFERENCES posts (post_id) ON DELETE CASCADE,
                           FOREIGN KEY (data_type_id)  
                           REFERENCES data_type (data_type_id) ON DELETE CASCADE);
                        """
                     )