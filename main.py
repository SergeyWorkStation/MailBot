import configparser
from threading import Thread

import telebot
from telebot import types

from create_tables import create_table
from insert_tables import insert_post, insert_user
from fetch_tables import get_all_post, get_post_by_id, get_all_rules
from mail import MailFilter

config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['telegram_api']['token']
mails = dict()
create_table()
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    insert_user(message.from_user.first_name, message.chat.id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Зарегистрировать почтовый ящик", callback_data='register')
    btn2 = types.InlineKeyboardButton("Проверка доступности почтовых ящиков", callback_data='check')
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}, данный бот предназначен для "
                                      f"помощи в отслеживании важных писем вашей электронной почты. Выберите одно из "
                                      f"доступных действий", reply_markup=markup)


@bot.message_handler(commands=['register_post'])
def send_register(message):
    global mails
    mails[f'{message.chat.id}'] = {'email': None, 'password': None}
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Ввести email 📬", callback_data='email')
    btn2 = types.InlineKeyboardButton("Ввести пароль 🔑", callback_data='password')
    btn3 = types.InlineKeyboardButton("Назад", callback_data='start')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, 'Вам необходимо ввести данные для авторизации своего почтового '
                                      'ящика. Для этого нажмите на соответствующую кнопку и введите '
                                      'значение.', reply_markup=markup)


@bot.message_handler(commands=['check_post'])
def check_post(message):
    markup = types.InlineKeyboardMarkup()
    req = get_all_post(message.chat.id)
    for post in req:
        markup.add(types.InlineKeyboardButton(post[0], callback_data=f'posts:{post[0]}:{post[2]}'))
    bot.send_message(message.chat.id, 'Выберите почтовый ящик 📬',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_function(callback):
    global mails
    if callback.data == 'start':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Зарегистрировать почтовый ящик", callback_data='register')
        btn2 = types.InlineKeyboardButton("Проверка доступности почтовых ящиков", callback_data='check')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(callback.message.chat.id, f"{callback.message.from_user.first_name}, выберите одно из "
                                                   f"доступных действий", reply_markup=markup)
    if callback.data == 'register':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
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
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        req = get_all_post(callback.message.chat.id)
        for post in req:
            markup.add(types.InlineKeyboardButton(post[0], callback_data=f'posts:{post[0]}:{post[2]}'))
        bot.send_message(callback.message.chat.id, 'Выберите почтовый ящик 📬',
                         reply_markup=markup)

    elif callback.data == 'email':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.register_next_step_handler(callback.message, register_email)
        bot.send_message(callback.message.chat.id, 'Введите email:')

    elif callback.data == 'password':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.register_next_step_handler(callback.message, register_password)
        bot.send_message(callback.message.chat.id, 'Введите пароль:')

    elif callback.data.split(':')[0] == 'posts':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        post_id = callback.data.split(':')[2]
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Создать правило для получения писем", callback_data='rules:' + post_id)
        btn2 = types.InlineKeyboardButton("Список правил для почты", callback_data='rules_list:' + post_id)
        btn3 = types.InlineKeyboardButton("Проверить соединение с сервером",
                                          callback_data='check_connection:' + post_id)
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(callback.message.chat.id, 'Выберите действие для email 📬: ' + callback.data.split(':')[1],
                         reply_markup=markup)

    elif callback.data.split(':')[0] == 'rules_list':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        req = get_all_rules(callback.data.split(':')[1])
        if req:
            for rule in req:
                markup.add(types.InlineKeyboardButton(f'Получать {rule[1].lower()} от {rule[0]} ',
                                                      callback_data=f'rule:{rule[2]}'))
            bot.send_message(callback.message.chat.id, 'Выберите правило 📬',
                             reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, 'Список пуст 📬',
                             reply_markup=markup)

    elif callback.data.split(':')[0] == 'check_connection':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        post_id = callback.data.split(':')[1]
        req = get_post_by_id(post_id)
        mail = MailFilter(req[0], req[1])
        if mail.is_connect():
            bot.send_message(callback.message.chat.id, 'Подключение к почтовому ящику прошло успешно')
        else:
            bot.send_message(callback.message.chat.id, 'Не удалось подключиться к почтовому ящику. Проверьте логин и '
                                                       'пароль, а также настройки вашего почтового ящика')

    elif callback.data == 'insert_db':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        try:
            insert_post(email=mails[f'{callback.message.chat.id}']['email'],
                        password=mails[f'{callback.message.chat.id}']['password'],
                        chat_id=f'{callback.message.chat.id}')
            bot.register_next_step_handler(callback.message, send_welcome)
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
