import config
import time
import telebot
from telebot import types
bot = telebot.TeleBot(config.token)
product_dict = {}

from pymongo import MongoClient
client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

db = client.fuckingtelegrambot

sell = db.sell



class Product:
    def __init__(self, name):
        self.name = name
        self.price = None        
        self.amount = None
        self.percent = None
        self.city = None
        

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Здравствуйте {0}. Что вы хотите? Купить или продать?".format(message.chat.first_name)
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    callback_bt1 = types.InlineKeyboardButton(text="Купить", callback_data="1")
    callback_bt2 = types.InlineKeyboardButton(text="Продать", callback_data="2")
    keyboard.add(callback_bt1, callback_bt2)
    bot.send_message(message.chat.id, welcome_msg,reply_markup=keyboard)



@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    print(c)
    if c.data=='2':
        msg = bot.reply_to(c.message, """\
                    Хорошо. Расскажите мне, что вы хотите продать. Cперва, введите ваше имя для продажи.
                    """)
        bot.register_next_step_handler(msg, process_name_step)
    elif c.data=='1':
        a = ""
        for i in sell.find():
            a += 'Name: {}\n'.format(i['name'])
            a += 'price: {}\n'.format(i['price'])
            a += '%: {}\n'.format(i['percent'])
            a += 'City: {}\n\n'.format(i['city'])
        bot.send_message(c.message.chat.id, a)


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

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
    try:
        chat_id = message.chat.id
        city = message.text
        product = product_dict[chat_id]
        product.city = city        
        bot.send_message(chat_id, 'Хорошо. Ваш зовут ' + product.name + '\n Цена товара: ' + str(product.price) + '\n Процент: ' + product.percent + '\n Город: ' + product.city)
        print(sell.insert_one({
            'name': product.name,
            'price': product.price,
            'percent': product.percent,
            'city': product.city

        }).inserted_id)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')
if __name__ == '__main__':
     bot.polling(none_stop=True)