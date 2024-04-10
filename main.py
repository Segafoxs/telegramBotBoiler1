import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('TOKEN')
login = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('segafox.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, '
                'name varchar(50), pass varchar(50))')

    conn.commit()
    cur.close()
    conn.close()

    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    # bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

    bot.send_message(message.chat.id, 'Давайте пройдем авторизацию! Введите ваше имя: ')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('segafox.sql')
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM users WHERE name = ? and pass = ?", (login, password)).fetchone()


    if result is None:
        bot.send_message(message.chat.id, 'Неправильный логин или пароль!')
        conn.close()
        start(message)
    else:
        boiler(message)

def boiler(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Параметры котла 7')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Параметры котла 9')
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Привет, чем могу помочь?', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Параметры котла 7':
        doc = open('report.csv', 'r')
        bot.send_document(message.chat.id, doc)
    elif message.text == 'Параметры котла 9':
        bot.send_message(message.chat.id, 'yes 9')

bot.polling(none_stop=True)


#Вывести список пользователей
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('segafox.sql')
#
#     cur = conn.cursor()
#
#
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     info = ''
#     for el in users:
#         info += f'id: {el[0]} Имя: {el[1]}, пароль: {el[2]}\n'
#
#     cur.close()
#     conn.close()
#
#
#     bot.send_message(call.message.chat.id, info)
#     bot.register_next_step_handler(message, user_pass)
#     bot.polling(none_stop=True)
