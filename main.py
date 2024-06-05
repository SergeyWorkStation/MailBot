from telebot import types
from threading import Thread
import telebot
from postgres_db import database_request, database_response
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['telegram_api']['token']

database_request("""CREATE TABLE IF NOT EXISTS users( 
                       user_id serial PRIMARY KEY,
                       name_user varchar(30),
                       chat_id int);"""
                )
database_request("""INSERT INTO users(name_user, chat_id)
                    VALUES ('Mari', 646452);"""
                )
res = database_response("""SELECT * FROM users;"""
                )
print(res)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Зарегистрировать почтовый ящик", callback_data='register')
    btn2 = types.InlineKeyboardButton("Проверка доступности почтовых ящиков", callback_data='check')
    markup.add(btn1)
    markup.add(btn2)
    print(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, f"""\
Привет {message.from_user.first_name}\
""", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'register':
        bot.send_message(callback.message.chat.id, 'Функция регистрации почты будет тут')

    elif callback.data == 'check':
        bot.send_message(callback.message.chat.id, 'Функция регистрации проверки доступности почтовых ящиков будет тут')

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

def other_function():
    pass
def polling():
    bot.infinity_polling()

polling_thread = Thread(target=polling)

polling_thread.start()