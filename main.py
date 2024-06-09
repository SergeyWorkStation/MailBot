from telebot import types
from threading import Thread
import telebot
import insert_tables, create_tables
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['telegram_api']['token']
mails = dict()
create_tables.create_table()
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    insert_tables.insert_user(message.from_user.first_name, message.chat.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Зарегистрировать почтовый ящик", callback_data='register')
    btn2 = types.InlineKeyboardButton("Проверка доступности почтовых ящиков", callback_data='check')
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}, данный бот предназначен для "
                                      f"помощи в отслеживании важных писем вашей электронной почты. Выберите одно из "
                                      f"доступных действий", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_function(callback):
    global mails
    if callback.data == 'register':

        mails[f'{callback.message.chat.id}'] = {'email': None, 'password': None}
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Ввести email 📬", callback_data='email')
        btn2 = types.InlineKeyboardButton("Ввести пароль 🔑", callback_data='password')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(callback.message.chat.id, 'Вам необходимо ввести данные для авторизации своего почтового '
                                                   'ящика. Для этого нажмите на соответствующую кнопку и введите '
                                                   'значение.', reply_markup=markup)

    elif callback.data == 'check':
        bot.send_message(callback.message.chat.id, 'Функция регистрации проверки доступности почтовых ящиков будет тут')

    elif callback.data == 'email':
        bot.register_next_step_handler(callback.message, register_email)
        bot.send_message(callback.message.chat.id, 'Введите email:')

    elif callback.data == 'password':
        bot.register_next_step_handler(callback.message, register_password)
        bot.send_message(callback.message.chat.id, 'Введите пароль:')

    elif callback.data == 'insert_db':

        try:
            insert_tables.insert_post(email=mails[f'{callback.message.chat.id}']['email'],
                                      password=mails[f'{callback.message.chat.id}']['password'],
                                      chat_id=f'{callback.message.chat.id}')
            bot.send_message(callback.message.chat.id,
                             f'Вы успешно зарегистрировали email: {mails[f'{callback.message.chat.id}']['email']}🎉')

        except:
            bot.send_message(callback.message.chat.id, 'Произошла ошибка😖😖😖\nЯ её исправляю😅🤥😏')

        finally:
            del mails[f'{callback.message.chat.id}']


def register_email(message):
    global mails
    mails[f'{message.chat.id}']['email'] = message.text.strip()
    markup = types.InlineKeyboardMarkup()
    if mails[f'{message.chat.id}']['password'] and mails[f'{message.chat.id}']['email']:
        btn1 = types.InlineKeyboardButton("Подтвердить данные", callback_data='insert_db')
        btn2 = types.InlineKeyboardButton("Повторить ввод", callback_data='register')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, f"""Ваш email: {mails[f'{message.chat.id}']['email']}
    Ваш пароль: {mails[f'{message.chat.id}']['password']}""", reply_markup=markup)
    else:
        btn = types.InlineKeyboardButton("Ввести пароль 🔑", callback_data='password')
        markup.add(btn)
        bot.send_message(message.chat.id, f"Ваш email: {mails[f'{message.chat.id}']['email']}", reply_markup=markup)


def register_password(message):
    global mails
    mails[f'{message.chat.id}']['password'] = message.text.strip()
    markup = types.InlineKeyboardMarkup()
    if mails[f'{message.chat.id}']['password'] and mails[f'{message.chat.id}']['email']:
        btn1 = types.InlineKeyboardButton("Подтвердить данные", callback_data='insert_db')
        btn2 = types.InlineKeyboardButton("Повторить ввод", callback_data='register')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, f"""Ваш email: {mails[f'{message.chat.id}']['email']}
Ваш пароль: {mails[f'{message.chat.id}']['password']}""", reply_markup=markup)
    else:
        btn = types.InlineKeyboardButton("Ввести email 📬", callback_data='email')
        markup.add(btn)
        bot.send_message(message.chat.id, f"Ваш пароль: {mails[f'{message.chat.id}']['password']}", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


def other_function():
    pass


def polling():
    bot.infinity_polling()


polling_thread = Thread(target=polling)

polling_thread.start()
