from telebot import types
from threading import Thread
import telebot
from postgres_db import database_request, database_response
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['telegram_api']['token']



res = database_response("""SELECT * FROM users;"""
                )
print(res)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    database_request(f"""INSERT INTO users(name_user, chat_id)
                        SELECT '{message.from_user.first_name}', '{message.chat.id}'
                        WHERE NOT EXISTS (SELECT 1 
                                            FROM users 
                                            WHERE chat_id = '{message.chat.id}');"""
                     )
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


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

def other_function():
    pass
def polling():
    bot.infinity_polling()

polling_thread = Thread(target=polling)

polling_thread.start()