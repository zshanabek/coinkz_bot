import config
import time
import telebot
from telebot import types
import pdb
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from telebot.types import LabeledPrice
from telebot.types import ShippingOption
import datetime
import math
import pprint
silver_price = [LabeledPrice(label='Silver', amount=200000)]
gold_price = [LabeledPrice(label='Gold', amount=500000)]
platinum_price = [LabeledPrice(label='Platinum', amount=800000)]

silver = "Silver"
gold = "Gold"
platinum = "Platinum"
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(config.token)
product_dict = {}
search_filter_dict = {}
user_dict = {}
search_menu = ['Все', 'Назад']
back_btn = ['Назад']
client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')
date_buttons = ['1 день', '3 дня', 'Неделя', 'За все время','Назад']
coin_names = ['Bitcoin', 'Ethereum', 'Litecoin', 'NEO', 'NEM', 'Stratis', 'BitShares', 'Stellar', 'Ripple', 'Dash', 'Lisk', 'Waves', 'Ethereum Classic', 'Monero', 'ZCash']

cities = ['Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган']

rus_cities = ['Москва','Санкт-Петербург','Новосибирск','Екатеринбург','Нижний Новгород','Казань','Челябинск','Омск','Самара','Ростов-на-Дону','Уфа','Красноярск','Пермь','Воронеж','Другое']

countries = ['Казахстан','Россия']
exchanges =['COINMARKETCAP', 'BLOCKCHAIN', 'CEX.IO', 'ALONIX', 'BITTREX', 'EXMO.ME', 'BITFINEX', 'POLONIEX']

main_buttons = ['Базар', 'Настройки', 'Инструкции по использованию', 'Обратная связь']
packages = ['Silver', 'Gold', 'Platinum', 'Узнать свой пакет', 'Отменить подписку', 'Назад к настройкам']
delete_buttons = ['Удалить', 'Мои объявления', 'Главное меню']
bazaar_buttons = ['Купить', 'Продать', 'Мои объявления', 'Главное меню']
settings_buttons = ['Пакеты']

class Product:
    def __init__(self, country):
        self.country = country
        self.name = None
        self.exchange = None
        self.price = None
        self.percent = None
        self.city = None
        self.comment = None
        self.contact = None
        self.text = None

class SearchFilter:
    def __init__(self, country):
    	self.current_page = None
    	self.price = None
    	self.sort_type = None
    	self.country = country
    	self.city = None
    	self.currency = None
    	self.commission = None


class User:
    def __init__(self, name):
        self.name = name
        self.text = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "Здравствуйте, *{0}*. Что вы хотите сделать?".format(message.chat.first_name)
    bot.send_message(message.chat.id, welcome_msg,reply_markup=create_keyboard(words=main_buttons,width=1),parse_mode='markdown')
    username = message.chat.username
    if traders.find({ 'username': username}).count()<1:
        traders.insert_one({
            'username': username,
            'is_paid':None,
            "created_at": datetime.datetime.utcnow()
        })
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({'username': message.chat.username,'chat_id':message.chat.id,"created_at": datetime.datetime.utcnow()})


#def handle_message(message):
 #  elif message.text=='Настройки':
  #      settings(message)
   # elif message.text=='Инструкции по использованию':
    #    command_terms(message)
 #   elif message.text == "Silver":
  #      silver_invoice(message)
   # elif message.text == "Gold":
    #    gold_invoice(message)
#    elif message.text == "Platinum":
 #       platinum_invoice(message)
  #  elif message.text == "Отменить подписку":
   #     cancel_subscription(message)
    #elif message.text == "Узнать свой пакет":
#        determine_package(message)
 #   elif message.text == "Главное меню":
  #      handle_main_menu_btn(message)
   # elif message.text =='Назад к настройкам':
    #    settings(message)

@bot.message_handler(func=lambda mess: mess.text == "Базар" or mess.text == "Назад", 
                     content_types=["text"])
def bazaar(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    msg = bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(bazaar_buttons,1,False,False))
    
@bot.message_handler(func=lambda mess: mess.text == "Обратная связь", 
                     content_types=["text"])
def obratnaya_sv(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    msg = bot.send_message(message.chat.id, 'Мы ценим мнение каждого из вас и нам очень важно знать о том, чего именно вам не хватает в работе с нашей программой.\nЕсли вы хотите видеть еще какие-либо дополнительные функции, просим вас написать об этом 👇👇👇\n\nС уважением @hancapital', reply_markup=create_keyboard(words=back_btn,width=1))
    bot.register_next_step_handler(msg, obratnaya_sv2)
    
def obratnaya_sv2(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Что вы хотите сделать?',reply_markup=create_keyboard(words=main_buttons,width=1),parse_mode='markdown')
    else:
        buttons = ['Нет', 'Да']
        user_name = str(message.from_user.first_name) 
        user = User(user_name)
        user_dict[message.chat.id] = user
        user = user_dict[message.chat.id]
        user.text = message.text
        msg = bot.reply_to(message, 'Вы уверены, что хотите отправить?', reply_markup=create_keyboard(words=buttons,width=1))
        bot.register_next_step_handler(msg, confirm_temp)

def confirm_temp(message):
    if message.text == "Да":
        username = message.chat.username
        user = user_dict[message.chat.id]
        feedbacks.insert_one({
            'username': username,
            "created_at": datetime.datetime.utcnow(),
            'text': user.text
        })
        bot.send_message(message.chat.id, 'Спасибо вам за обратную связь!',reply_markup=create_keyboard(words=main_buttons,width=1),parse_mode='markdown')
    elif message.text == "Нет":
        obratnaya_sv(message)

@bot.message_handler(func=lambda mess: mess.text == "Купить",
                     content_types=["text"])
def buy(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    msg = bot.send_message(message.chat.id, 'Отлично! Сейчас я задам несколько вопросов. Ответы на них будут составлять параметры поиска в моей базе объявлений. Таким образом я найду для вас нужные объявления. Поехали!\n'
    'Для начала выберите страну из списка.', reply_markup=create_keyboard(countries+['Назад'],1,False,False))
    bot.register_next_step_handler(msg, choose_country_buy)

def choose_country_buy(message):
    try:
        chat_id = message.chat.id
        country = message.text
        if message.text == 'Назад':
            bazaar(message)
        elif iequal(country, 'Казахстан'):
            search_filter = SearchFilter(country)
            search_filter_dict[chat_id] = search_filter
            msg = bot.reply_to(message, 'Выберите город из списка.', reply_markup=create_keyboard(["Все"]+cities+['Назад'],1,True,False))
            bot.register_next_step_handler(msg, choose_city_buy)
        elif iequal(country, 'Россия'):
            search_filter = SearchFilter(country)
            search_filter_dict[chat_id] = search_filter
            msg = bot.reply_to(message, 'Выберите город из списка.', reply_markup=create_keyboard(["Все"]+rus_cities+['Назад'],1,True,False))
            bot.register_next_step_handler(msg, choose_city_buy_rus) 
        else:
            msg = bot.reply_to(message, 'Выберите страну из списка.')
            bot.register_next_step_handler(msg, choose_country_buy)
            return
            
    except Exception as e:
        bot.reply_to(message, 'oooops')


def choose_city_buy(message):
    try:
        chat_id = message.chat.id
        city = message.text
        if message.text == 'Назад':
            bazaar(message)
        elif city == 'Другое':
        	msg = bot.reply_to(message, 'Введите название города.')
        	bot.register_next_step_handler(msg, process_enter_city)
        else:
            count = 0
            for i in cities+['Все']:
                if iequal(city, i):
                    count+=1
            if count==1:
                search_filter = search_filter_dict[chat_id]
                search_filter.city = city
                msg = bot.reply_to(message, 'Выберите криптовалюту из списка.', reply_markup=create_keyboard(["Все"]+coin_names+['Назад'],1,False,False))
                bot.register_next_step_handler(msg, process_name_step_buy)
            else:
                msg = bot.reply_to(message, 'Выберите город из списка.')
                bot.register_next_step_handler(msg, choose_city_buy)
                return
            
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_enter_city(message):
	try:
		chat_id = message.chat.id
		city = message.text
		search_filter = search_filter_dict[chat_id]
		search_filter.city = city
		msg = bot.reply_to(message, 'Выберите криптовалюту из списка.', reply_markup=create_keyboard(["Все"]+coin_names+['Назад'],1,False,False))
		bot.register_next_step_handler(msg, process_name_step_buy)
	except Exception as e:
		bot.reply_to(message, 'oooops')

def choose_city_buy_rus(message):
    try:
        chat_id = message.chat.id
        city = message.text
        if message.text == 'Назад':
            bazaar(message)
        elif city == 'Другое':
        	msg = bot.reply_to(message, 'Введите название города.')
        	bot.register_next_step_handler(msg, process_enter_city)
        else:
            count = 0
            for i in rus_cities+['Все']:
                if iequal(city, i):
                    count+=1
            if count==1:
                search_filter = search_filter_dict[chat_id]
                search_filter.city = city
                msg = bot.reply_to(message, 'Выберите криптовалюту из списка.', reply_markup=create_keyboard(["Все"]+coin_names+['Назад'],1,False,False))
                bot.register_next_step_handler(msg, process_name_step_buy)
            else:
                msg = bot.reply_to(message, 'Выберите город из списка.')
                bot.register_next_step_handler(msg, choose_city_buy_rus)
                return
            
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(func=lambda mess: mess.text == "Пакеты",
                     content_types=["text"])
def list_packages(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    msg = bot.send_message(message.chat.id, "Выберите пакет.", reply_markup=create_keyboard(words=packages,width=1))
    bot.register_next_step_handler(msg, process_package_step)

def process_package_step(message):
    if message.text == "Silver":
        silver_invoice(message)
    elif message.text == "Gold":
        gold_invoice(message)
    elif message.text == "Platinum":
        platinum_invoice(message)
    elif message.text == "Отменить подписку":
        cancel_subscription(message)
    elif message.text == "Узнать свой пакет":
        determine_package(message)
    elif message.text == "Назад к настройкам":
        settings(message)

def cancel_subscription(message):
    buttons = ['Нет', 'Да']
    msg = bot.reply_to(message, 'Вы уверены, что хотите отменить подписку?', reply_markup=create_keyboard(words=buttons,width=1))
    bot.register_next_step_handler(msg, process_package_delete_confirmation_step)

def determine_package(message):
    a = traders.find_one({'username':message.chat.username})
    package_id = a['is_paid']
    if (package_id == False or package_id==None):
        msg = bot.send_message(message.chat.id, "Вы не активировали ни один пакет.")
    else:
        if package_id == 1:
            package_name = silver
        elif package_id == 2:
            package_name = gold
        elif package_id == 3:
            package_name = platinum
        msg = bot.send_message(message.chat.id, "У вас пакет {0}".format(package_name))
    bot.register_next_step_handler(msg, process_package_step)
def process_package_delete_confirmation_step(message):
    if message.text == "Да":
        traders.update_one({'username':message.chat.username},{'$set':{'is_paid':False}})
        msg = bot.send_message(message.chat.id, "Я отменил подписку.")
        list_packages(message)
    elif message.text == "Нет":
        list_packages(message)

def silver_invoice(message):
    bot.send_invoice(message.chat.id,
        title='Пакет Silver',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Silver пакет даёт возможность размещения 10 объявлений.''',
        provider_token=config.provider_token,
        currency='KZT',
        photo_url='http://livingalegacyinc.com/wp-content/uploads/2016/09/silver.png',
        photo_height=300,
        photo_width=300,
        photo_size=300,
        is_flexible=False,
        prices=silver_price,
        start_parameter='coinkz-silver',
        invoice_payload='Silver')

def gold_invoice(message):
    bot.send_invoice(message.chat.id,
        title='Пакет Gold',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Gold пакет даёт возможность размещения 30 объявлений.''',
        provider_token=config.provider_token,
        currency='KZT',
        photo_url='http://angeltd.com/wp-content/uploads/2016/06/gold-package.png',
        photo_height=300,  # !=0/None or picture won't be shown
        photo_width=280,
        photo_size=300,
        is_flexible=False,  # True If you need to set up Shipping Fee
        prices=gold_price,
        start_parameter='coinkz-gold',
        invoice_payload='Gold')

def platinum_invoice(message):
    bot.send_invoice(message.chat.id,
        title='Пакет Platinum',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Platinum пакет даёт возможность размеще до 50 объявлений.''',
        provider_token=config.provider_token,
        currency='KZT',
        photo_url='https://i2.wp.com/www.buildyoursocialgame.com/wp-content/uploads/2016/11/platinum-pkg.png',
        photo_height=300,  # !=0/None or picture won't be shown
        photo_width=280,
        photo_size=300,
        is_flexible=False,
        prices=platinum_price,
        start_parameter='coinkz-platinum',
        invoice_payload='Platinum')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Мошенники хотели украсть CVV вашей карточки, но я успешно защитил ваши данные,"
                                                " Попробуйте оплатить через несколько минут еще раз. Мне нужен отдых.")
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    msg = bot.send_message(message.chat.id,
                     'Спасибо за покупку {0} пакета! '
                     'Оставайтесь с нами.'.format(message.successful_payment.invoice_payload), parse_mode='Markdown')

    invoice_payload = message.successful_payment.invoice_payload

    if invoice_payload == "Silver":
        traders.update_one({'username':message.chat.username},{'$set':{'is_paid':1}})
    elif invoice_payload == "Gold":
        traders.update_one({'username':message.chat.username},{'$set':{'is_paid':2}})
    elif invoice_payload == "Platinum":
        traders.update_one({'username':message.chat.username},{'$set':{'is_paid':3}})

    bot.register_next_step_handler(msg, process_package_step)

def process_find_price(message):
    try:
        chat_id = message.chat.id
        price = message.text
        search_filter = search_filter_dict[chat_id]
        if price == 'Назад':
            bazaar(message)
        else:
            if price=='Все':
               search_filter.price = {"$gte":0}
            else:
                p = price.split("-")
                if len(p)==1:
                    msg = bot.reply_to(message, 'Введите два числа разделенными тире.')
                    bot.register_next_step_handler(msg, process_find_price)
                    return
                elif(p[0].isdigit() and p[1].isdigit()):
                    n1 = int(p[0])
                    n2 = int(p[1])
                    if n1>n2:
                        msg = bot.reply_to(message, 'Введите цену от меньшего к большему.')
                        bot.register_next_step_handler(msg, process_find_price)
                        return
                    else:
                        search_filter.price = {"$gte": n1, "$lte": n2}
                else:
                    msg = bot.reply_to(message, 'Введите ценовой диапозон.')
                    bot.register_next_step_handler(msg, process_find_price)
                    return

            msg = bot.reply_to(message, '''Какую комиссию вы хотите найти? Введите диапозон, разделенный тире, от меньшего к большому. Например: 5-10. Если для вас это не важно нажмите 'Все'.''', reply_markup=create_keyboard(words=search_menu,width=1))
            bot.register_next_step_handler(msg, process_commission_filter_step)
    except Exception as e:
        msg = bot.reply_to(message, "Введите ценовой диапозон.",reply_markup=create_keyboard(words=search_menu,width=1))
        bot.register_next_step_handler(msg, process_find_price)


def process_commission_filter_step(message):
    try:
        chat_id = message.chat.id
        commission = message.text
        search_filter = search_filter_dict[chat_id]
        if commission == 'Назад':
            bazaar(message)
        else:
            if commission=='Все':
               search_filter.commission = {"$gte":0}
            else:
                c = commission.split("-")
                if len(c)==1:
                    msg = bot.reply_to(message, 'Введите два числа разделенными тире.')
                    bot.register_next_step_handler(msg, process_commission_filter_step)
                    return
                elif(c[0].isdigit() and c[1].isdigit()):
                    n1 = int(c[0])
                    n2 = int(c[1])
                    if n1>n2:
                        msg = bot.reply_to(message, 'Введите комиссию от меньшего к большему.')
                        bot.register_next_step_handler(msg, process_commission_filter_step)
                        return
                    else:
                        search_filter.commission = {"$gte": n1, "$lte": n2}
                else:
                    msg = bot.reply_to(message, 'Введите числовой диапозон.')
                    bot.register_next_step_handler(msg, process_commission_filter_step)
                    return
            msg = bot.reply_to(message, 'Выберите промежуток времени со дня публикаций.', reply_markup=create_keyboard(words=date_buttons, width=1))
            bot.register_next_step_handler(msg, process_sort_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Введите числовой диапозон.')
        bot.register_next_step_handler(msg, process_commission_filter_step)

def process_sort_step(message):
    try:
        chat_id = message.chat.id
        sort_type = message.text
        search_filter = search_filter_dict[chat_id]
        if sort_type == 'Назад':
            bazaar(message)
        else:
            if sort_type == '1 день' or sort_type == '3 дня' or sort_type == 'Неделя' or sort_type =='За все время':
                if sort_type == '1 день':
                    N = 1
                elif sort_type == '3 дня':
                    N = 3
                elif sort_type == 'Неделя':
                    N = 7
                elif sort_type == 'За все время':
                    N = 100000
                date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=N)
                search_filter.sort_type = ({'$gte':date_N_days_ago})
                filter_params = get_filter_params(chat_id)
                # bot.send_message(chat_id, str(filter_params))
                pages = get_pages_num(filter_params)
                a = skiplimit(5,1,filter_params, chat_id,pages)
                search_filter.current_page = 1
                keyboard = types.InlineKeyboardMarkup(row_width = 2)
                if sell.find(filter_params).count()>5:
                    callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="forward")
                    keyboard.add(callback_bt2)
                if pages != 1:            
                    msg = bot.send_message(chat_id,a, reply_markup=keyboard, parse_mode='HTML')
                else:
                    msg = bot.send_message(chat_id,a, parse_mode='HTML')                
                bot.register_next_step_handler(msg, process_sort_step)
            else:
                msg = bot.reply_to(message, 'Выберите промежуток времени со дня публикаций.', reply_markup=create_keyboard(words=date_buttons, width=1))
                bot.register_next_step_handler(msg, process_sort_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Выберите промежуток времени со дня публикаций.', reply_markup=create_keyboard(words=date_buttons, width=1))
        bot.register_next_step_handler(msg, process_sort_step)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            chat_id = call.message.chat.id
            search_filter = search_filter_dict[chat_id]
            if call.data == 'back' or call.data == 'forward':
                if call.data=='back':
                    search_filter.current_page-=1
                elif call.data == 'forward':
                    search_filter.current_page+=1
                filter_params = get_filter_params(chat_id)
                pages = get_pages_num(filter_params)                
                a = skiplimit(5,search_filter.current_page,filter_params,chat_id,pages)
                keyboard = types.InlineKeyboardMarkup(row_width = 2)
                callback_bt1= types.InlineKeyboardButton(text="Назад", callback_data="back")
                callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="forward")

                if search_filter.current_page == 1:
                    keyboard.add(callback_bt2)
                elif search_filter.current_page == pages:
                    keyboard.add(callback_bt1)
                else:
                    keyboard.add(callback_bt1, callback_bt2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=a, reply_markup=keyboard,parse_mode="HTML")
            else:
                pages = get_pages_num({'username': call.message.chat.username})                
                if call.data =='-1':
                    search_filter.current_page-=1
                elif call.data == '1':
                    search_filter.current_page+=1
                a = skiplimit(5,search_filter.current_page,{'username': call.message.chat.username},chat_id,pages)
                keyboard = types.InlineKeyboardMarkup(row_width = 2)
                callback_bt1= types.InlineKeyboardButton(text="Назад", callback_data="-1")
                callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="1")


                if search_filter.current_page == 1:
                    keyboard.add(callback_bt2)
                elif search_filter.current_page == pages:
                    keyboard.add(callback_bt1)
                else:
                    keyboard.add(callback_bt1, callback_bt2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=a, reply_markup=keyboard,parse_mode="HTML")
    except Exception as e:
        bot.reply_to(call.message, 'oooops')

def get_filter_params(chat_id):
    search_filter = search_filter_dict[chat_id]
    filter_params = {}

    filter_params["price"]=search_filter.price
    filter_params["percent"]=search_filter.commission
    filter_params["created_at"] = search_filter.sort_type
    filter_params["country"] = search_filter.country
    if search_filter.city != "Все":
        filter_params["city"]=search_filter.city
    if search_filter.currency != "Все":
        filter_params["name"]=search_filter.currency

    return filter_params

def get_pages_num(filter_params):
    ads_count = sell.find(filter_params).count()
    pages = math.ceil(ads_count/5.0)

    return pages

def skiplimit(page_size, page_num, filter_params, chat_id, total_pages):
    skips = page_size * (page_num - 1)
    cursor = sell.find(filter_params).skip(skips).limit(page_size)
   
    ads_count = sell.find(filter_params).count()
    b = page_size * page_num - page_size +1
    a = 'Найдено {0} объявлений:\n\n'.format(ads_count)
    for i in cursor:
        if b==page_size * page_num +1:
            break
        else:
            a += '{0}. Криптовалюта: {1}\n'.format(b, i['name'])
            a += 'Сумма покупки: $'+'{}\n'.format(i['price'])
            a += 'Комиссия: {}%\n'.format(i['percent'])
            a += 'Биржа: {}\n'.format(i['exchange'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n'.format(i['username'])
            a += 'Номер телефона: {}\n'.format(i['phone_number'] if i['phone_number'] else '')  
            a += 'Комментарий: <i>{}</i>\n'.format(i['comment'])
            a += 'Дата создания (UTC): {}\n\n'.format(i['created_at'].strftime("%d/%m/%Y"))
            b+=1
    return a

@bot.message_handler(func=lambda mess: mess.text == "Продать",
                     content_types=["text"])
def sell_coin(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    current_username = message.chat.username
    t = traders.find_one({'username':current_username})

    if (current_username == None):
        bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
    else:
        # if (sell.find({'username':current_username}).count()==3 and (t['is_paid']==None or t['is_paid']==False)):
        #     msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (3 объявления). Купите один из пакетов чтобы публиковать больше объявлений")
        #     list_packages(message)
        # elif (sell.find({'username':current_username}).count()==10 and t['is_paid']==1):
        #     msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (10 объявлений). Купите один из пакетов чтобы публиковать больше объявлений")
        #     list_packages(message)
        # elif (sell.find({'username':current_username}).count()==30 and t['is_paid']==2):
        #     msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (10 объявлений). Купите один из пакетов чтобы публиковать больше объявлений")
        #     list_packages(message)
        # elif (sell.find({'username':current_username}).count()==50 and t['is_paid']==3):
        #     msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (50 объявлений)")
        # else:
            ct = countries+["Назад"]
            msg = bot.send_message(message.chat.id, 'Отлично! Сейчас я задам несколько вопросов, касающиеся вашего нового объявления. Ответьте на них пожалуйста. Если все хорошо, я опубликую его. Это позволит другим пользователям найти ваше объявление. Если оно им понравится, то вам позвонят, либо напишут. Поехали!\nСперва, выберите вашу страну из списка', reply_markup=create_keyboard(ct,3,True,False))
            bot.register_next_step_handler(msg, process_country_step)

@bot.message_handler(func=lambda mess: mess.text == "Мои объявления",
                     content_types=["text"])
def my_ads(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    chat_id = message.chat.id
    username = message.chat.username
    a = "Ваши объявления\n\n"
    b = 1
    if sell.find({'username':username}).count()==0:
        msg = bot.send_message(message.chat.id, 'У вас пока нету объявлений.', reply_markup=create_keyboard(bazaar_buttons,1,False,False))
    else:
        search_filter = SearchFilter('')
        search_filter_dict[chat_id] = search_filter            
        search_filter.current_page = 1
        pages = get_pages_num({'username':username})
        a = skiplimit(5,1,{'username':username}, chat_id,pages)
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        if sell.find({'username':username}).count()>5:
            callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="1")
            keyboard.add(callback_bt2)
        msg = bot.send_message(chat_id, 'Ваши объявления', reply_markup=create_keyboard(delete_buttons,1,False,False))
        msg1 = bot.send_message(chat_id, a, parse_mode='HTML', reply_markup=keyboard)
        bot.register_next_step_handler(msg1, process_my_ads_step)


def process_my_ads_step(message):
    if message.text == 'Мои объявления':
        my_ads(message)
    elif message.text == 'Удалить':
        remove(message)
    elif message.text == 'Главное меню':
        handle_main_menu_btn(message)

def remove(message):
    try:
        username = message.chat.username
        chat_id = message.chat.id
        ads_number = sell.find({'username':username}).count()
        if ads_number==0:
            bot.send_message(message.chat.id, "У вас пока нету объявлений.", reply_markup=create_keyboard(delete_buttons,1,False,False))
        else:
            numbers = range(1,ads_number+1)
            str_numbers = [str(i) for i in numbers]
            str_numbers.append('Назад')

            msg = bot.send_message(message.chat.id, "Какое по счету объявление вы хотите удалить?", reply_markup=create_keyboard(str_numbers,1,False,False))
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
            ads_number = sell.find({'username':username}).count()
            if ads_number==0:
                bot.send_message(message.chat.id, "У вас пока нету объявлений.", reply_markup=create_keyboard(delete_buttons,1,False,False))
            else:
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
                msg =bot.send_message(chat_id, "Ok, я удалил {0} объявление".format(seq_num+1))

                my_ads(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_country_step(message):
    try:
        chat_id = message.chat.id
        country = message.text
        if message.text == 'Назад':
            bazaar(message)
        elif iequal(country, 'Казахстан'):
            product = Product(country)
            product_dict[chat_id] = product
            msg = bot.send_message(message.chat.id, 'Выберите город из списка.', reply_markup=create_keyboard(cities+['Назад'],3,True,False))
            bot.register_next_step_handler(msg, process_city_step)
        elif iequal(country, 'Россия'):
            product = Product(country)
            product_dict[chat_id] = product
            msg = bot.send_message(message.chat.id, 'Выберите город из списка.', reply_markup=create_keyboard(rus_cities+['Назад'],3,True,False))
            bot.register_next_step_handler(msg, process_city_step2)
        else:
            msg = bot.reply_to(message, 'Выберите город из списка.')
            bot.register_next_step_handler(msg, process_country_step)
            return
            
    except Exception as e:
        msg = bot.reply_to(message, 'Выберите город из списка.')
        bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        chat_id = message.chat.id
        city = message.text.capitalize()
        if message.text == 'Назад':
            bazaar(message)
        elif city == 'Другое':
        	msg = bot.reply_to(message, 'Введите название города.')
        	bot.register_next_step_handler(msg, process_enter_city2)
        else:
            count = 0
            for i in cities:
                if iequal(city, i):
                    count+=1
            if count == 1:
                product = product_dict[chat_id]
                product.city = city
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Нет')
                itembtn2 = types.KeyboardButton('Отправить контакт',request_contact=True)
                markup.add(itembtn1, itembtn2)
                msg = bot.reply_to(message, 'Хотите поделиться своим телефонным номером? Если нет, то с вами свяжутся через ваш username в Телеграме.', reply_markup=markup)
                bot.register_next_step_handler(msg, process_phone_step)
            else:
                msg = bot.reply_to(message, 'Выберите город из списка.')
                bot.register_next_step_handler(msg, process_city_step)
                return
            
    except Exception as e:
        msg = bot.reply_to(message, 'Выберите город из списка.')
        bot.register_next_step_handler(msg, process_city_step)

def process_enter_city2(message):
	try:
		chat_id = message.chat.id
		city = message.text
		product = product_dict[chat_id]
		product.city = city
		markup = types.ReplyKeyboardMarkup(row_width=1)
		itembtn1 = types.KeyboardButton('Нет')
		itembtn2 = types.KeyboardButton('Отправить контакт',request_contact=True)
		markup.add(itembtn1, itembtn2)
		msg = bot.reply_to(message, 'Хотите поделиться своим телефонным номером? Если нет, то с вами свяжутся через ваш username в Телеграме.', reply_markup=markup)
		bot.register_next_step_handler(msg, process_phone_step)
	except Exception as e:
		bot.reply_to(message, 'oooops')

def process_city_step2(message):
    try:
        chat_id = message.chat.id
        city = message.text.capitalize()
        if message.text == 'Назад':
            bazaar(message)
        elif city == 'Другое':
        	msg = bot.reply_to(message, 'Введите название города.')
        	bot.register_next_step_handler(msg, process_enter_city2)
        else:
            count = 0
            for i in rus_cities:
                if iequal(city, i):
                    count+=1
            if count == 1:
                product = product_dict[chat_id]
                product.city = city
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Нет')
                itembtn2 = types.KeyboardButton('Отправить контакт',request_contact=True)
                markup.add(itembtn1, itembtn2)
                msg = bot.reply_to(message, 'Хотите поделиться своим телефонным номером? Если нет, то с вами свяжутся через ваш username в Телеграме.', reply_markup=markup)
                bot.register_next_step_handler(msg, process_phone_step)
            else:
                msg = bot.reply_to(message, 'Выберите город из списка.')
                bot.register_next_step_handler(msg, process_city_step)
                return
            
    except Exception as e:
        msg = bot.reply_to(message, 'Выберите город из списка.')
        bot.register_next_step_handler(msg, process_city_step)


def process_phone_step(message):
    try:
        chat_id = message.chat.id
        product = product_dict[chat_id]
        if message.contact:
            product.contact = message.contact.phone_number
        else:
            product.contact = ''

        msg = bot.reply_to(message, 'Теперь выберите криптовалюту.', reply_markup=create_keyboard(coin_names,1,True,False))
        bot.register_next_step_handler(msg, process_name_step)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Нет')
        itembtn2 = types.KeyboardButton('Отправить контакт',request_contact=True)
        markup.add(itembtn1, itembtn2)
        msg = bot.reply_to(message, 'Хотите поделиться своим телефонным номером?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_phone_step)

def process_name_step_buy(message):
    try:
        chat_id = message.chat.id
        currency = message.text
        if message.text == 'Назад':
            bazaar(message)
        else:
        	count = 0            
	        for i in ['Все']+coin_names:
	            if iequal(currency, i):
	                count+=1
	        
	        if count == 1:
	            search_filter = search_filter_dict[chat_id]
	            search_filter.currency = currency
	            msg = bot.reply_to(message, "Введите ценовой диапозон, разделенный тире, от меньшего к большому. Например: 2000-5000. Чтобы искать все цены нажмите на кнопку 'Все'.",reply_markup=create_keyboard(words=search_menu,width=1))
	            bot.register_next_step_handler(msg, process_find_price)
	        else:
	            msg = bot.reply_to(message, 'Выберите криптовалюту из списка.')
	            bot.register_next_step_handler(msg, process_name_step_buy)
	            return
       
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text.title()
        count = 0
        for i in coin_names:
            if iequal(name, i):
                count+=1
    
        if count == 1:
            product = product_dict[chat_id]
            product.name = name

            msg = bot.reply_to(message, 'На сколько долларов вы хотите продать?')
            bot.register_next_step_handler(msg, process_price_step)
        else:
            msg = bot.reply_to(message, 'Выберите криптовалюту из списка.')
            bot.register_next_step_handler(msg, process_name_step)
            return

    except Exception as e:
        msg = bot.reply_to(message, 'Выберите криптовалюту из списка.')
        bot.register_next_step_handler(msg, process_name_step)

def process_price_step(message):
    try:
        chat_id = message.chat.id
        price = message.text
        if not price.isdigit():
            msg = bot.reply_to(message, 'Цена должна быть числом.')
            bot.register_next_step_handler(msg, process_price_step)
            return
        product = product_dict[chat_id]
        product.price = price
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        msg = bot.reply_to(message, 'Какую комиссию вы берете? От 0 до 100.')
        bot.register_next_step_handler(msg, process_percent_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Цена должна быть числом.')
        bot.register_next_step_handler(msg, process_price_step)

def process_percent_step(message):
    try:
        chat_id = message.chat.id
        percent = message.text
        rng = range(0,101)
        if not percent.isdigit():
            msg = bot.reply_to(message, 'Процент комиссии должен быть числом.')
            bot.register_next_step_handler(msg, process_percent_step)
            return
        if int(percent) not in rng:
            msg = bot.reply_to(message, 'Процент комиссии должен быть между 0 и 100.')
            bot.register_next_step_handler(msg, process_percent_step)
            return
        product = product_dict[chat_id]
        product.percent = percent
        msg = bot.reply_to(message, 'По какому курсу?', reply_markup = create_keyboard(exchanges,2,False,False))
        bot.register_next_step_handler(msg, process_exchange_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Процент комиссии должен быть числом.')
        bot.register_next_step_handler(msg, process_percent_step)

def process_exchange_step(message):
    try:
        chat_id = message.chat.id
        exchange = message.text.upper()
        product = product_dict[chat_id]
        if not (exchange in exchanges):
            msg = bot.reply_to(message, 'Выберите биржу из списка.')
            bot.register_next_step_handler(msg, process_exchange_step)
            return
        product.exchange = exchange
        msg = bot.reply_to(message, 'Есть ли у вас комментарии? Если нет, то можете оставить пустым.', reply_markup=create_keyboard(['Нет'],1,False,False))
        bot.register_next_step_handler(msg, process_comment_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Выберите биржу из списка.')
        bot.register_next_step_handler(msg, process_exchange_step)


def process_comment_step(message):
    try:
        chat_id = message.chat.id
        comment = message.text
        product = product_dict[chat_id]
        username = message.chat.username
        if comment=='Нет':
             product.comment=''
        else:
            product.comment = comment
        buttons = ['Нет', 'Да']
        a = 'Подтвердите объявление о продаже\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange + '\nСтрана: ' + product.country +'\nГород: ' + product.city+'\nUsername: @'+username+'\nТелефон: '+product.contact+'\nКомментарий: <i>'+product.comment+'</i>'
        msg = bot.send_message(chat_id, a, reply_markup=create_keyboard(buttons,2,False,False),parse_mode='HTML')
        bot.register_next_step_handler(msg, process_confirmation_step)
    except Exception as e:
        msg = bot.reply_to(message, 'Есть ли у вас комментарии?', reply_markup=create_keyboard(['Нет'],1,False,False))
        bot.register_next_step_handler(msg, process_comment_step)

def process_confirmation_step(message):
    try:
        chat_id = message.chat.id
        confirm_answer = message.text
        product = product_dict[chat_id]
        username = message.chat.username
        if confirm_answer == 'Да':
            sell.insert_one({
                'name': product.name,
                'price': int(product.price),
                'percent': int(product.percent),
                'exchange': product.exchange,
                'country': product.country,
                'city': product.city,
                'username': username,
                'comment': product.comment,
                'phone_number': product.contact,
                "created_at": datetime.datetime.utcnow()
            })
            a = 'Вы успешно опубликовали!\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange + '\nСтрана: ' + product.country +'\nГород: ' + product.city+'\nUsername: @'+username+'\nТелефон: '+product.contact+'\nКомментарий: <i>'+product.comment+'</i>'
            bot.send_message(chat_id, a, reply_markup = create_keyboard(main_buttons,1,False,False), parse_mode='HTML')
        else:
            bot.send_message(chat_id, 'Вы отменили объявление о продаже.', reply_markup=create_keyboard(main_buttons,1,False,False))
    except Exception as e:
        buttons = ['Нет', 'Да']
        a = 'Подтвердите объявление о продаже\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange + '\nСтрана: ' + product.country +'\nГород: ' + product.city+'\nUsername: @'+username+'\nТелефон: '+product.contact+'\nКомментарий: <i>'+product.comment+'</i>'
        msg = bot.send_message(chat_id, a, reply_markup=create_keyboard(buttons,2,False,False),parse_mode='HTML')
        bot.register_next_step_handler(msg, process_confirmation_step)


def create_keyboard(words=None, width=None, isOneTime=False, isPhone=False):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=isOneTime, row_width=width, resize_keyboard = True)
    for word in words:
        keyboard.add(types.KeyboardButton(text=word, request_contact=isPhone))
    return keyboard


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Введите команду /start для начала торговли.")


@bot.message_handler(func=lambda mess: mess.text == "Инструкции по использованию",
                     content_types=["text"])
def command_terms(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    bot.send_message(message.chat.id,
        '''🤔<b>Что это за бот?</b>
Данный бот помогает связать покупателей и продавцов криптовалюты по всему миру.

💡<b>Какую проблему он решает?</b>
В наше время поиск покупателей и продавцов криптовалюты выглядит рутинной задачей (Писать свое объявление в разных группах, искать в сотнях сообщений актуальные предложения. Сверять что предложение находится в вашем городе, с нужной суммой и приемлемой комиссией. 

✅<b>Как работает данный бот?</b>
Бот принимает и фильтрует объявления о продаже криптовалюты по всему миру. И помогает людям находить нужные объявления с помощью фильтров.
 
🎯<b>Инструкция по использованию:</b>
1. Введите команду /start для начала работы бота
2. Нажмите на кнопку "Базар"
3. Нажмите на нужный вам пункт "Купить" или "Продать"
4. Заполните все данные, которые запросит бот

<b>Что важно знать:</b>
1. Для продажи криптовалюты - вам нужно будет создать объявления в боте
2. Для покупки криптовалюты - вам нужно будет ответить на некоторые вопросы и получить уже созданные объявления о продаже
3. Для удаления недействительных объявлений - перейдите в категорию "Мои объявления"
 
<b>Удачи мой друг</b>🙌

P.S. Если есть предложения и отзывы о боте, напиши в личку @hancapital''', parse_mode="HTML")

@bot.message_handler(func=lambda mess: mess.text == "Настройки" or mess.text == "Назад к настройкам",
                     content_types=["text"])
def settings(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    bot.send_message(message.chat.id, '''<b>Инструкция по размещению объявлений:</b>
При использовании данного бота каждую неделю вы получаете право подать 3 бесплатных объявления. По истечению лимита в 3 объявления в неделю, вам необходимо приобрести один из платных пакетов.

<b>💸Стоимость и наименование пакетов:</b>
<b>Silver</b> - дает право размещать 10 объявлений.Цена: <b>2000тг</b>.
<b>Gold</b> - дает право размещать 30 объявлений.Цена: <b>5000тг</b>.
<b>Platinum</b> - дает право размещать 50 объявлений.Цена: <b>8000тг</b>.

<b>Что важно знать:</b>
В случае,если вы не подали за неделю то количество объявлений, которое вы приобрели, то остаток переносится на следующую неделю.
Данное правило не относится к еженедельным 3 бесплатным объявлениям.

<b>Удачи мой друг</b>🙌

P.S Если есть предложения и отзывы о боте,напиши в личку
@hancapital''', parse_mode="HTML")
    msg = bot.send_message(message.chat.id, 'Выберите настройки.', reply_markup=create_keyboard(settings_buttons+['Главное меню'],1,False,False))

@bot.message_handler(func=lambda mess: mess.text == "Главное меню",
                     content_types=["text"])
def handle_main_menu_btn(message):
    if users.find({ 'chat_id': message.chat.id}).count()<1:
        users.insert_one({
            'username': message.chat.username,
            'chat_id':message.chat.id,
            "created_at": datetime.datetime.utcnow()
        })
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(words=main_buttons,width=1))

def iequal(a, b):
    try:
        return a.upper() == b.upper()
    except AttributeError:
        return a == b
if __name__ == '__main__':
    db = client.fuckingtelegrambot
    sell = db.sell_new
    traders = db.traders
    feedbacks = db.feedbacks
    users = db.users
    bot.polling(none_stop=True)
