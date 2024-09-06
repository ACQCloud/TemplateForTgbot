import telebot
import sqlite3
from telebot import types

print('Injecting token.')
bot = telebot.TeleBot('')
link = 'https://discord.gg/'
name= None

print('Injected token!')

@bot.message_handler(commands=['start'])
def start(message):

    # sqlconnect
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increament primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Введите свой имья:')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль: ')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    # sqlconnect
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()


    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()


    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup= markup)
    print(f'New user: {name}. Password: {password}. Telegram:', message.from_user.first_name, message.from_user.last_name, '[',  message.from_user.username, ':', message.from_user.id, ']')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # sqlconnect
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    a = 0
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'ID: {a}. Имья: {el[1]}. Пароль: {el[2]}.\n'
        a = a + 1
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

print('Telegram Bot is working...')

bot.polling(none_stop=True)
