from telebot import types
from threading import Thread
import telebot
import psycopg2
#API_TOKEN = '7154170243:AAGdWMvdTrwSt_L2UBzsW4dvpn9ixv6-uDM'
API_TOKEN = '7154170243:AAGdWMvdTrwSt_L2UBzsW4dvpn9ixv6-uDM'

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='mydb', user='user', password='mypassword', host='192.168.0.107', port='5432')
    print('Successfully connection to database')
except Exception as e:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')
    print(e)
bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Зарегистрировать почтовый ящик", callback_data='register')
    btn2 = types.InlineKeyboardButton("Проверка доступности почтовых ящиков", callback_data='check')
    markup.add(btn1)
    markup.add(btn2)
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