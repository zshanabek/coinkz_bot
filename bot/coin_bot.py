import config
import time
import telebot
from telebot import types
import pprint
import pdb
bot = telebot.TeleBot(config.token)
product_dict = {}

from pymongo import MongoClient
client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

db = client.fuckingtelegrambot
sell = db.sell
# db.sell.delete_many({})

class Product:
    def __init__(self, name):
        self.name = name
        self.price = None        
        self.amount = None
        self.percent = None
        self.city = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Здравствуйте, {0}. Что вы хотите сделать?".format(message.chat.first_name)
    buttons = [
            'Купить',
            'Продать',
            'Найти по названию валюты',
            'Найти по цене валюты'
            ]
    bot.send_message(message.chat.id, welcome_msg,reply_markup=create_keyboard(buttons, 1))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'Продать':
        if (message.chat.username == None):
            bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
        else:
            msg = bot.send_message(message.chat.id, """\
                    Хорошо. Cперва, введите имя валюты.
                    """)
            bot.register_next_step_handler(msg, process_name_step)
    elif message.text=='Купить':
        a = ""
        for i in sell.find():
            a += 'Название валюты: {}\n'.format(i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            if(i['username']!=None):
                a += 'Владелец: @{}\n\n'.format(i['username'])     
            else:
                a += 'Владелец: Не указан'  
        bot.send_message(message.chat.id, a)
    elif message.text=='Найти по названию валюты':
        msg = bot.send_message(message.chat.id, "Введите название валюты")
        bot.register_next_step_handler(msg, process_find)
    elif message.text=='Найти по цене валюты':
        msg = bot.send_message(message.chat.id, "Введите ценовой диапозон, разделенный пробелом. Например: 2000 5000")
        bot.register_next_step_handler(msg, process_find_price)

@bot.message_handler(commands=['find'])
def find_coins(message):
    msg = bot.send_message(message.chat.id, "Введите название валюты")
    bot.register_next_step_handler(msg, process_find)

@bot.message_handler(commands=['find_price'])
def find_price_coins(message):
    msg = bot.send_message(message.chat.id, "Введите ценовой диапозон, разделенный пробелом. Например: 2000 5000")
    bot.register_next_step_handler(msg, process_find_price)

def process_find(message):
    # try:
        coin_name = message.text  
        a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"name": coin_name}).count())
        for i in sell.find({"name": coin_name}):
            a += 'Название валюты: {}\n'.format(i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            if(i['username']!=None):
                a += 'Владелец: @{}\n\n'.format(i['username'])     
            else:
                a += 'Владелец: Не указан'  
        bot.send_message(message.chat.id, a)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

def process_find_price(message):
    # try:
        price = message.text  
        p = price.split(" ")
        n1 = int(p[0])
        n2 = int(p[1])
        a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"price": {"$gt": n1, "$lt": n2}}).count())
        for i in sell.find({"price": {"$gt": n1, "$lt": n2}}):
            a += 'Название валюты: {}\n'.format(i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            if(i['username']!=None):
                a += 'Владелец: @{}\n\n'.format(i['username'])     
            else:
                a += 'Владелец: Не указан'  
        bot.send_message(message.chat.id, a)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['sell'])
def sell(message):
    if (message.chat.username == None):
        bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
    else:
        msg = bot.send_message(message.chat.id, """\
                Хорошо. Cперва, введите имя валюты.
                """)
        bot.register_next_step_handler(msg, process_name_step)

@bot.message_handler(commands=['buy'])
def bye(message):     
    a = ""
    for i in sell.find():
        a += 'Название валюты: {}\n'.format(i['name'])
        a += 'Цена: $'+'{}\n'.format(i['price'])
        a += 'Процент: {}\n'.format(i['percent'])
        a += 'Город: {}\n'.format(i['city'])
        if(i['username']!=None):
            a += 'Владелец: @{}\n\n'.format(i['username'])     
        else:
            a += 'Владелец: Не указан'  
    bot.send_message(message.chat.id, a)


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Введите команду /start для начала торговли")

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        product = Product(name)
        product_dict[chat_id] = product
        msg = bot.reply_to(message, 'Какая цена?')
        bot.register_next_step_handler(msg, process_price_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_price_step(message):
    try:
        chat_id = message.chat.id
        price = message.text
        if not price.isdigit():
            msg = bot.reply_to(message, 'Цена должна быть числом')
            bot.register_next_step_handler(msg, process_price_step)
            return
        product = product_dict[chat_id]
        product.price = price
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        msg = bot.reply_to(message, 'Под какой процент?')
        bot.register_next_step_handler(msg, process_percent_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_percent_step(message):
    try:
        chat_id = message.chat.id
        percent = message.text
        if not percent.isdigit():
            msg = bot.reply_to(message, 'Процент должен быть числом')
            bot.register_next_step_handler(msg, process_percent_step)
            return
        product = product_dict[chat_id]
        product.percent = percent
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        msg = bot.reply_to(message, 'Из какого города?')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
def process_city_step(message):
    # try:
        chat_id = message.chat.id
        city = message.text
        product = product_dict[chat_id]
        product.city = city        
        bot.send_message(chat_id, 'Вы хотите продать ' + product.name + '\nЦена: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent + '\nГород: ' + product.city)
        sell.insert_one({
            'name': product.name,
            'price': int(product.price),
            'percent': int(product.percent),
            'city': product.city,
            'username': message.chat.username
        }).inserted_id
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

def create_keyboard(words=None, width=None):
        keyboard = types.ReplyKeyboardMarkup(row_width=width, resize_keyboard = True)
        for word in words:
            keyboard.add(types.KeyboardButton(text=word))
        return keyboard
if __name__ == '__main__':
     bot.polling(none_stop=True)