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

coin_names = ['NEO','NEM','Stratis','BitShares','Ethereum','Stellar','Ripple','Dash','Lisk','Litecoin','Waves','Ethereum Classic','Monero','Bitcoin','ZCash'] 

cities = ['Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Кызылорда','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган']
main_buttons = [
            'Купить',
            'Продать',
            'Найти по названию валюты',
            'Найти по цене валюты',
            'Мои объявления'
            ]
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
    bot.send_message(message.chat.id, welcome_msg,reply_markup=create_keyboard(main_buttons, 1))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'Продать':
        sell_coin(message)
    elif message.text=='Купить':
        buy(message)
    elif message.text=='Найти по названию валюты':
        find_coins(message)
    elif message.text=='Найти по цене валюты':
        find_price_coins(message)
    elif message.text=='Мои объявления':
        my_ads(message)

@bot.message_handler(commands=['find'])
def find_coins(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('NEO','NEM','Stratis','BitShares','Ethereum','Stellar','Ripple','Dash','Lisk','Litecoin','Waves','Ethereum Classic','Monero','Bitcoin','ZCash')
    msg = bot.send_message(message.chat.id, "Выберите криптовалюту", reply_markup=markup)
    bot.register_next_step_handler(msg, process_find)

@bot.message_handler(commands=['find_price'])
def find_price_coins(message):
    msg = bot.send_message(message.chat.id, "Введите ценовой диапозон, разделенный пробелом. Например: 2000 5000")
    bot.register_next_step_handler(msg, process_find_price)

def process_find(message):
    try:
        coin_name = message.text  
        b = 1
        a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"name": coin_name}).count())
        for i in sell.find({"name": coin_name}).limit(10):
            a += '{0}. Название валюты: {1}\n'.format(b, i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n\n'.format(i['username'])
            b+=1
        bot.send_message(message.chat.id, a, reply_markup=create_keyboard(main_buttons, 1))
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_find_price(message):
    try:
        price = message.text  
        p = price.split(" ")
        n1 = int(p[0])
        n2 = int(p[1])
        b = 1
        a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"price": {"$gte": n1, "$lte": n2}}).count())
        for i in sell.find({"price": {"$gte": n1, "$lte": n2}}).limit(10):
            a += '{0}. Название валюты: {1}\n'.format(b, i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n\n'.format(i['username'])   
            b+=1  
        bot.send_message(message.chat.id, a)
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['sell'])
def sell_coin(message):
    if message.text == 'Продать':
        if (message.chat.username == None):
            bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Bitcoin','Ethereum','Litecoin','NEO','NEM','Stratis','BitShares','Stellar','Ripple','Dash','Lisk','Waves','Ethereum Classic','Monero','ZCash')
            msg = bot.reply_to(message, 'Хорошо. Cперва, выберите криптовалюту.', reply_markup=markup)
            bot.register_next_step_handler(msg, process_name_step)

@bot.message_handler(commands=['buy'])
def buy(message):  
    try:   
        a = "Свежие объявления\n\n"
        b = 1
        for i in sell.find().sort('_id',-1).limit(10):
            a += '{0}. Название валюты: {1}\n'.format(b,i['name'])
            a += 'Цена: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n\n'.format(i['username'])     
            b+=1
        bot.send_message(message.chat.id, a)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def my_ads(message):
    try:   
        username = message.chat.username
        a = "Ваши объявления\n\n"
        b = 1
        if sell.find({'username':username}).count()==0:
            bot.send_message(message.chat.id, 'У вас пока нету объявлений')
        else:
            for i in sell.find({'username':username}):
                a += '{0}. Название валюты: {1}\n'.format(b,i['name'])
                a += 'Цена: $'+'{}\n'.format(i['price'])
                a += 'Процент: {}\n'.format(i['percent'])
                a += 'Город: {}\n'.format(i['city'])
                a += 'Владелец: @{}\n\n'.format(i['username'])     
                b+=1
            bot.send_message(message.chat.id, a)
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Введите команду /start для начала торговли")

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        product = Product(name)
        product_dict[chat_id] = product
        if (name in coin_names):
            product.name = name
        else:
            raise Exception()
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
        markup.add('Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Кызылорда','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган')
        msg = bot.reply_to(message, 'Из какого вы города?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
def process_city_step(message):
    try:
        chat_id = message.chat.id
        city = message.text
        product = product_dict[chat_id]
        if (city in cities):
            product.city = city
        else:
            raise Exception()    
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Нет', 'Да')
        msg = bot.reply_to(message, 'Подтвердите объявление о продаже', reply_markup=markup)
        bot.register_next_step_handler(msg, process_confirmation_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_confirmation_step(message):
    try:
        chat_id = message.chat.id
        confirm_answer = message.text
        product = product_dict[chat_id]        
        if confirm_answer == 'Да':
            bot.send_message(chat_id, 'Вы успешно опубликовали!\n\nВалюта: ' + product.name + '\nЦена: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent + '\nГород: ' + product.city, reply_markup = create_keyboard(main_buttons,1))
            sell.insert_one({
                'name': product.name,
                'price': int(product.price),
                'percent': int(product.percent),
                'city': product.city,
                'username': message.chat.username
            }).inserted_id
        else:
            bot.send_message(chat_id, 'Вы отменили объявление о продаже', reply_markup = create_keyboard(main_buttons,1))
    except Exception as e:
        bot.reply_to(message, 'oooops')
def create_keyboard(words=None, width=None):
        keyboard = types.ReplyKeyboardMarkup(row_width=width, resize_keyboard = True)
        for word in words:
            keyboard.add(types.KeyboardButton(text=word))
        return keyboard
if __name__ == '__main__':
    db = client.fuckingtelegrambot
    # db.sell.delete_many({})
    sell = db.sell
    bot.polling(none_stop=True)