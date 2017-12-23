import config
import time
import telebot
from telebot import types
import pprint
import pdb
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from telebot.types import LabeledPrice
from telebot.types import ShippingOption
silver_price = [LabeledPrice(label='Silver', amount=2000 )]
gold_price = [LabeledPrice(label='Gold', amount=3000 )]
platinum_price = [LabeledPrice(label='Platinum', amount=5000 )]


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 
bot = telebot.TeleBot(config.token)
product_dict = {}
search_menu = ['Главное меню']        
client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

coin_names = ['Bitcoin','Ethereum','Litecoin','NEO','NEM','Stratis','BitShares','Stellar','Ripple','Dash','Lisk','Waves','Ethereum Classic','Monero','ZCash'] 

cities = ['Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Кызылорда','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган']

exchanges =['COINMARKETCAP', 'BLOCKCHAIN', 'CEX.IO', 'ALONIX', 'BITTREX', 'EXMO.ME', 'BITFINEX', 'POLONIEX']

main_buttons = ['Купить','Продать','Найти по названию валюты','Найти по цене валюты','Мои объявления','Пакеты']

packages = ['Silver', 'Gold', 'Platinum','Главное меню']

premium = ['Получить премиум', 'Главное меню']
delete_buttons = ['Удалить', 'Мои объявления','Главное меню']
class Product:
    def __init__(self, name):
        self.name = name
        self.exchange = None
        self.price = None        
        self.percent = None
        self.city = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Здравствуйте, {0}. Что вы хотите сделать?".format(message.chat.first_name)
    bot.send_message(message.chat.id, welcome_msg,reply_markup=create_keyboard(main_buttons, 1))
    username = message.chat.username
    if traders.find({ 'username': username}).count()<1:
        traders.insert_one({
            'username': username,
            'is_paid':None
        })

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
    elif message.text=='Удалить':
        remove(message)
    elif message.text=='Главное меню':
        a = 'Что вы хотите сделать?'
        bot.send_message(message.chat.id, a, reply_markup=create_keyboard(main_buttons, 1))
    elif message.text=='Пакеты':
        list_packages(message)      

@bot.message_handler(commands=['find'])
def find_coins(message):
    msg = bot.send_message(message.chat.id, "Выберите криптовалюту", reply_markup=create_keyboard(coin_names,1))
    bot.register_next_step_handler(msg, process_find)

@bot.message_handler(commands=['find_price'])
def find_price_coins(message):
    msg = bot.send_message(message.chat.id, "Введите ценовой диапозон, разделенный пробелом, от меньшего к большому. Например: 2000 5000",reply_markup=create_keyboard(search_menu,1))
    bot.register_next_step_handler(msg, process_find_price)

def list_packages(message):
    msg = bot.send_message(message.chat.id, "Выберите пакет", reply_markup=create_keyboard(packages,1))
    bot.register_next_step_handler(msg, process_package_step)

def process_package_step(message):
    if message.text == "Silver":
        msg = silver_invoice(message)
        bot.register_next_step_handler(msg, process_package_step)
    elif message.text == "Gold":
        msg = gold_invoice(message)
        bot.register_next_step_handler(msg, process_package_step)
    elif message.text == "Platinum":
        msg = platinum_invoice(message)
        bot.register_next_step_handler(msg, process_package_step)
    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(main_buttons,1))

def silver_invoice(message):
    msg = bot.send_invoice(message.chat.id, 
        title='Пакет Silver',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Silver пакет даёт возможность размещения 10 объявлений''',
        provider_token=config.provider_token,
        currency='USD',
        photo_url='http://livingalegacyinc.com/wp-content/uploads/2016/09/silver.png',
        photo_height=300,  # !=0/None or picture won't be shown
        photo_width=300,
        photo_size=300,
        is_flexible=False,  # True If you need to set up Shipping Fee
        prices=silver_price,
        start_parameter='coinkz-silver',
        invoice_payload='HAPPY FRIDAYS 1')
    return msg
    
def gold_invoice(message):
    msg = bot.send_invoice(message.chat.id, 
        title='Пакет Gold',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Gold пакет даёт возможность размещения 30 объявлений''',
        provider_token=config.provider_token,
        currency='USD',
        photo_url='http://angeltd.com/wp-content/uploads/2016/06/gold-package.png',
        photo_height=300,  # !=0/None or picture won't be shown
        photo_width=280,
        photo_size=300,
        is_flexible=False,  # True If you need to set up Shipping Fee
        prices=gold_price,
        start_parameter='coinkz-gold',
        invoice_payload='HAPPY FRIDAYS 2')
    return msg
    

def platinum_invoice(message):
    msg = bot.send_invoice(message.chat.id, 
        title='Пакет Platinum',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Platinum пакет даёт возможность размеще до 50 объявлений''',
        provider_token=config.provider_token,
        currency='USD',
        photo_url='https://i2.wp.com/www.buildyoursocialgame.com/wp-content/uploads/2016/11/platinum-pkg.png',
        photo_height=300,  # !=0/None or picture won't be shown
        photo_width=280,
        photo_size=300,
        is_flexible=False,  
        prices=platinum_price,
        start_parameter='coinkz-platinum',
        invoice_payload='HAPPY FRIDAYS 3')
    return msg    
    
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Мошенники хотели украсть CVV вашей карточки, но я успешно защитил ваши данные. Попробуйте еще раз оплатить через несколько минут")
                                                
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, 'Ура! Спасибо за покупку пакета! Оставайтесь с нами')
    traders.update_one({'username':message.chat.username},{'$set':{'is_paid':True}})

def process_find(message):
    try:
        coin_name = message.text  
        b = 1
        a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"name": coin_name}).count())
        for i in sell.find({"name": coin_name}).limit(10):
            a += '{0}. Название валюты: {1}\n'.format(b, i['name'])
            a += 'Cумма покупки: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}%\n'.format(i['percent'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n\n'.format(i['username'])
            b+=1
        bot.send_message(message.chat.id, a, reply_markup=create_keyboard(main_buttons, 1))
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_find_price(message):
    try:
        price = message.text

        if price == 'Главное меню':
            bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(main_buttons,1))
        else:
            p = price.split(" ")
            if(not (p[0].isdigit() and p[1].isdigit())):
                msg = bot.reply_to(message, 'Введите ценовой диапозон')
                bot.register_next_step_handler(msg, process_find_price)
                return
            n1 = int(p[0])
            n2 = int(p[1])
            b = 1
            a = 'Найдено продавцoв: {0}\n\n'.format(sell.find({"price": {"$gte": n1, "$lte": n2}}).count())
            for i in sell.find({"price": {"$gte": n1, "$lte": n2}}).limit(10):
                a += '{0}. Название валюты: {1}\n'.format(b, i['name'])
                a += 'Сумма покупки: $'+'{}\n'.format(i['price'])
                a += 'Процент: {}%\n'.format(i['percent'])
                a += 'Биржа: {}\n'.format(i['exchange'])                       
                a += 'Город: {}\n'.format(i['city'])
                a += 'Владелец: @{}\n\n'.format(i['username'])   
                b+=1  
            msg = bot.send_message(message.chat.id, a, reply_markup=create_keyboard(search_menu,1))
            bot.register_next_step_handler(msg, process_find_price)
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['sell'])
def sell_coin(message):
    current_username = message.chat.username
    t = traders.find_one({'username':current_username})
    if (sell.find({'username':current_username}).count()==3 and t['is_paid']==None):
        bot.send_message(message.chat.id, "Вы достигли лимит объявлений (3 объявления). Купите премиум пакет чтобы публиковать больше объявлений. Хотите получить премиум?", reply_markup=create_keyboard(premium,1))
    else: 
        if (current_username == None):
            bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
        else:
            msg = bot.reply_to(message, 'Хорошо. Cперва, выберите криптовалюту.', reply_markup=create_keyboard(coin_names,1,True))
            bot.register_next_step_handler(msg, process_name_step)

@bot.message_handler(commands=['buy'])
def buy(message):  
    try:   
        a = "Свежие объявления\n\n"
        b = 1
        for i in sell.find().sort('_id',-1).limit(10):
            a += '{0}. Название валюты: {1}\n'.format(b,i['name'])
            a += 'Сумма покупки: $'+'{}\n'.format(i['price'])
            a += 'Процент: {}%\n'.format(i['percent'])
            a += 'Биржа: {}\n'.format(i['exchange'])            
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
                a += 'Сумма покупки: $'+'{}\n'.format(i['price'])
                a += 'Процент: {}%\n'.format(i['percent'])
                a += 'Биржа: {}\n'.format(i['exchange'])                            
                a += 'Город: {}\n'.format(i['city'])
                a += 'Владелец: @{}\n\n'.format(i['username'])     
                b+=1
            bot.send_message(message.chat.id, a, reply_markup=create_keyboard(delete_buttons,1))                
    except Exception as e:
        bot.reply_to(message, 'oooops')

def remove(message):
    try:
        username = message.chat.username
        ads_number = sell.find({'username':username}).count()
        if ads_number==0:
            bot.send_message(message.chat.id, "У вас пока нету объявлений", reply_markup=create_keyboard(delete_buttons,1)) 
        else:
            numbers = range(1,ads_number+1)
            str_numbers = [str(i) for i in numbers]
            str_numbers.append('Назад')
            msg = bot.send_message(message.chat.id, "Какое по счету объявление вы хотите удалить?", reply_markup=create_keyboard(str_numbers,1))       
            bot.register_next_step_handler(msg, process_remove_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
def process_remove_step(message):
    try:
        if message.text == 'Назад':
            my_ads(message)
        else:
            username = message.chat.username    
            chat_id = message.chat.id
            seq_num = int(message.text)
            seq_num-=1
            target = ObjectId()
            docs = sell.find({'username':username})
            docs_count = docs.count()

            for i in range(docs_count):
                if i==seq_num:
                    target = docs[i]['_id']
                print(str(i)+'fds'+str(seq_num))

            sell.delete_one({'_id': target})
            bot.send_message(chat_id, "Ok, я удалил {0} объявление".format(seq_num+1), reply_markup=create_keyboard(delete_buttons,1))
    except Exception as e:
        bot.reply_to(message, 'oooops')   
def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if not (name in coin_names):
            msg = bot.reply_to(message, 'Выберите криптовалюту из списка')
            bot.register_next_step_handler(msg, process_name_step)
            return
        
        product = Product(name)
        product_dict[chat_id] = product        
        product.name = name
        msg = bot.reply_to(message, 'На сколько долларов вы хотите продать?')
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
        msg = bot.reply_to(message, 'По какому курсу?', reply_markup = create_keyboard(exchanges,2))
        bot.register_next_step_handler(msg, process_exchange_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_exchange_step(message):
    try:
        chat_id = message.chat.id
        exchange = message.text
        product = product_dict[chat_id]
        if not (exchange in exchanges):
            msg = bot.reply_to(message, 'Выберите биржу из списка')
            bot.register_next_step_handler(msg, process_exchange_step)
            return
        product.exchange = exchange
        msg = bot.reply_to(message, 'Из какого города?', reply_markup=create_keyboard(cities,3))
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oooops') 
        
def process_city_step(message):
    try:
        chat_id = message.chat.id
        city = message.text
        product = product_dict[chat_id]

        if not (city in cities):
            msg = bot.reply_to(message, 'Выберите город из списка')
            bot.register_next_step_handler(msg, process_city_step)
            return
        product.city = city
        
        buttons = ['Нет', 'Да']
        msg = bot.reply_to(message, 'Подтвердите объявление о продаже', reply_markup=create_keyboard(buttons,2))
        bot.register_next_step_handler(msg, process_confirmation_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_confirmation_step(message):
    try:
        chat_id = message.chat.id
        confirm_answer = message.text
        product = product_dict[chat_id]   
        username = message.chat.username     
        if confirm_answer == 'Да':
            bot.send_message(chat_id, 'Вы успешно опубликовали!\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange +'\nГород: ' + product.city+'\nUsername: @'+username, reply_markup = create_keyboard(main_buttons,1))
            sell.insert_one({
                'name': product.name,
                'price': int(product.price),
                'percent': int(product.percent),
                'exchange': product.exchange,                
                'city': product.city,
                'username': username
            })
        else:
            bot.send_message(chat_id, 'Вы отменили объявление о продаже', reply_markup = create_keyboard(main_buttons,1))
    except Exception as e:
        bot.reply_to(message, 'oooops')
def create_keyboard(words=None, width=None, isOneTime=None):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=isOneTime, row_width=width, resize_keyboard = True)
        for word in words:
            keyboard.add(types.KeyboardButton(text=word))
        return keyboard

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Введите команду /start для начала торговли")

@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Thank you for shopping with our demo bot. We hope you like your new time machine!\n'
                     '1. If your time machine was not delivered on time, please rethink your concept of time and try again.\n'
                     '2. If you find that your time machine is not working, kindly contact our future service workshops on Trappist-1e.'
                     ' They will be accessible anywhere between May 2075 and November 4000 C.E.\n'
                     '3. If you would like a refund, kindly apply for one yesterday and we will have sent it to you immediately.')
if __name__ == '__main__':
    db = client.fuckingtelegrambot
    sell = db.sell
    traders = db.traders
    bot.skip_pending = True
    bot.polling(none_stop=True, interval=0)