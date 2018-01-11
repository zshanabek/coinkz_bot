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
search_menu = ['Все', 'Назад']
client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')
date_buttons = ['1 день', '3 дня', 'Неделя', 'Назад']
coin_names = ['Bitcoin', 'Ethereum', 'Litecoin', 'NEO', 'NEM', 'Stratis', 'BitShares', 'Stellar', 'Ripple', 'Dash', 'Lisk', 'Waves', 'Ethereum Classic', 'Monero', 'ZCash']

cities = ['Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Кызылорда','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган']

exchanges =['COINMARKETCAP', 'BLOCKCHAIN', 'CEX.IO', 'ALONIX', 'BITTREX', 'EXMO.ME', 'BITFINEX', 'POLONIEX']

main_buttons = ['Базар', 'Настройки', 'Условия использования']
packages = ['Silver', 'Gold', 'Platinum', 'Узнать свой пакет', 'Отменить подписку', 'Назад']
delete_buttons = ['Удалить', 'Мои объявления', 'Главное меню']
bazaar_buttons = ['Купить', 'Продать', 'Мои объявления', 'Главное меню']
settings_buttons = ['Пакеты']
class Product:
    def __init__(self, city):
        self.name = None
        self.exchange = None
        self.price = None
        self.percent = None
        self.city = city
        self.comment = None
        self.contact = None

class SearchFilter:
    def __init__(self, city):
        self.city = city
        self.currency = None
        self.price = None
        self.commission = None
        self.sort_type = None
        self.current_page = None

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

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text=='Базар':
        bazaar(message)
    elif message.text=='Настройки':
        settings(message)
    elif message.text=='Условия использования':
        command_terms(message)
    elif message.text == "Silver":
        silver_invoice(message)
    elif message.text == "Gold":
        gold_invoice(message)
    elif message.text == "Platinum":
        platinum_invoice(message)
    elif message.text == "Отменить подписку":
        cancel_subscription(message)
    elif message.text == "Узнать свой пакет":
        determine_package(message)
    elif message.text == "Главное меню":
        handle_main_menu_btn(message)


def bazaar(message):
    msg = bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(bazaar_buttons,1,False,False))
    bot.register_next_step_handler(msg, process_bazaar_step)

def process_bazaar_step(message):
    if message.text =='Купить':
        msg = bot.send_message(message.chat.id, 'Выберите город', reply_markup=create_keyboard(["Все"]+cities+['Назад'],1,False,False))
        bot.register_next_step_handler(msg, choose_city_buy)
    elif message.text == 'Продать':
        sell_coin(message)
    elif message.text == 'Мои объявления':
        my_ads(message)
    elif message.text == 'Главное меню':
        handle_main_menu_btn(message)

def choose_city_buy(message):
    try:
        chat_id = message.chat.id
        city = message.text
        if message.text == 'Назад':
            bazaar(message)
        else:
            if not (city in cities+['Все']):
                msg = bot.reply_to(message, 'Выберите город из списка')
                bot.register_next_step_handler(msg, choose_city_buy)
                return
            search_filter = SearchFilter(city)

            search_filter_dict[chat_id] = search_filter
            search_filter.city = city
            msg = bot.reply_to(message, 'Выберите криптовалюту', reply_markup=create_keyboard(["Все"]+coin_names,1,False,False))
            bot.register_next_step_handler(msg, process_name_step_buy)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def list_packages(message):
    msg = bot.send_message(message.chat.id, "Выберите пакет", reply_markup=create_keyboard(words=packages,width=1))
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
    elif message.text == "Назад":
        settings(message)

def cancel_subscription(message):
    buttons = ['Нет', 'Да']
    msg = bot.reply_to(message, 'Вы уверены, что хотите отменить подписку?', reply_markup=create_keyboard(words=buttons,width=1))
    bot.register_next_step_handler(msg, process_package_delete_confirmation_step)

def determine_package(message):
    a = traders.find_one({'username':message.chat.username})
    package_id = a['is_paid']
    if (package_id == False or package_id==None):
        msg = bot.send_message(message.chat.id, "Вы не активировали ни один пакет")
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
        msg = bot.send_message(message.chat.id, "Я отменил подписку")
        list_packages(message)
    elif message.text == "Нет":
        list_packages(message)

def silver_invoice(message):
    bot.send_invoice(message.chat.id,
        title='Пакет Silver',
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Silver пакет даёт возможность размещения 10 объявлений''',
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
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Gold пакет даёт возможность размещения 30 объявлений''',
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
        description='''Хочешь публиковать больше объявлений по продажам криптовалюты? Platinum пакет даёт возможность размеще до 50 объявлений''',
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
                                                " Попробуйте оплатить через несколько минут еще раз. Мне нужен отдых")
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
                    msg = bot.reply_to(message, 'Введите два числа')
                    bot.register_next_step_handler(msg, process_find_price)
                    return
                elif(p[0].isdigit() and p[1].isdigit()):
                    n1 = int(p[0])
                    n2 = int(p[1])
                    if n1>n2:
                        msg = bot.reply_to(message, 'Введите цену от большего к меньшему')
                        bot.register_next_step_handler(msg, process_find_price)
                        return
                    else:
                        search_filter.price = {"$gte": n1, "$lte": n2}
                else:
                    msg = bot.reply_to(message, 'Введите ценовой диапозон')
                    bot.register_next_step_handler(msg, process_find_price)
                    return

            msg = bot.send_message(message.chat.id, 'Какую комиссию вы хотите найти? Если для вас это не важно нажмите "Все"', reply_markup=create_keyboard(words=search_menu,width=1))
            bot.register_next_step_handler(msg, process_commission_filter_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

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
                if(commission.isdigit()):
                    com = int(commission)
                    search_filter.commission = {"$eq": com}
                else:
                    msg = bot.reply_to(message, 'Введите два числа разделенные пробелом')
                    bot.register_next_step_handler(msg, process_commission_filter_step)
                    return
            msg = bot.send_message(message.chat.id, 'Выберите сортировку', reply_markup=create_keyboard(words=date_buttons, width=1))
            bot.register_next_step_handler(msg, process_sort_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_sort_step(message):
    # try:
        chat_id = message.chat.id
        sort_type = message.text
        search_filter = search_filter_dict[chat_id]
        if sort_type == 'Назад':
            bazaar(message)
        else:
            if sort_type == '1 день':
                N = 1
            elif sort_type == '3 дня':
                N = 3
            elif sort_type == 'Неделя':
                N = 7
            date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=N)
            search_filter.sort_type = ({'$gte':date_N_days_ago})
            filter_params = get_filter_params(chat_id)
            pages = get_pages_num(filter_params)
            a = skiplimit(5,1,filter_params, chat_id,pages)
            search_filter.current_page = 1
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="forward")
            keyboard.add(callback_bt2)
            msg = bot.send_message(message.chat.id, a, reply_markup=keyboard)


            bot.register_next_step_handler(msg, process_sort_step)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # try:
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
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=a, reply_markup=keyboard)
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
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=a, reply_markup=keyboard)
    # except Exception as e:
    #     bot.reply_to(call.message, 'oooops')

def get_filter_params(chat_id):
    search_filter = search_filter_dict[chat_id]
    filter_params = {}

    filter_params["price"]=search_filter.price
    filter_params["percent"]=search_filter.commission
    filter_params["created_at"] = search_filter.sort_type
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
    a = 'Найдено продавцoв: {0}\n\n'.format(ads_count)
    for i in cursor:
        while (b < page_size*page_num+1):
            a += '{0}. Криптовалюта: {1}\n'.format(b, i['name'])
            a += 'Сумма покупки: $'+'{}\n'.format(i['price'])
            a += 'Комиссия: {}%\n'.format(i['percent'])
            a += 'Биржа: {}\n'.format(i['exchange'])
            a += 'Город: {}\n'.format(i['city'])
            a += 'Владелец: @{}\n'.format(i['username'])
            a += 'Дата создания (UTC): {}\n\n'.format(i['created_at'].strftime("%d/%m/%Y"))
            b+=1
    return a


@bot.message_handler(commands=['sell'])
def sell_coin(message):
    current_username = message.chat.username
    t = traders.find_one({'username':current_username})

    if (current_username == None):
        bot.send_message(message.chat.id, "У вас нету зарегестрированного имени пользователя Телеграм (username). Username нужен для того, чтобы покупатели могли с вами связаться. Зайдите в настройки вашего аккаунта и укажите юзернейм.")
    else:
        if (sell.find({'username':current_username}).count()==3 and (t['is_paid']==None or t['is_paid']==False)):
            msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (3 объявления). Купите один из пакетов чтобы публиковать больше объявлений")
            list_packages(message)
        elif (sell.find({'username':current_username}).count()==10 and t['is_paid']==1):
            msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (10 объявлений). Купите один из пакетов чтобы публиковать больше объявлений")
            list_packages(message)
        elif (sell.find({'username':current_username}).count()==30 and t['is_paid']==2):
            msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (10 объявлений). Купите один из пакетов чтобы публиковать больше объявлений")
            list_packages(message)
        elif (sell.find({'username':current_username}).count()==50 and t['is_paid']==3):
            msg = bot.send_message(message.chat.id, "Вы достигли лимит объявлений (50 объявлений)")
        else:
            ct = cities+["Назад"]
            msg = bot.reply_to(message, 'Сперва, выберите город из списка', reply_markup=create_keyboard(ct,3,True,False))
            bot.register_next_step_handler(msg, process_city_step)

def my_ads(message):
    # try:
        chat_id = message.chat.id
        username = message.chat.username
        a = "Ваши объявления\n\n"
        b = 1
        if sell.find({'username':username}).count()==0:
            bot.send_message(message.chat.id, 'У вас пока нету объявлений')
        else:
            search_filter = SearchFilter('')
            search_filter_dict[chat_id] = search_filter            
            search_filter.current_page = 1
            pages = get_pages_num({'username':username})
            a = skiplimit(5,1,{'username':username}, chat_id,pages)
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="1")
            keyboard.add(callback_bt2)
            msg1 = bot.send_message(message.chat.id, a, reply_markup=keyboard)
            msg = bot.send_message(message.chat.id, 'Ваши объявления', reply_markup=create_keyboard(delete_buttons,1,False,False))
            bot.register_next_step_handler(msg, process_my_ads_step)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')

def process_my_ads_step(message):
    if message.text == 'Мои объявления':
        my_ads(message)
    elif message.text == 'Удалить':
        remove(message)
    elif message.text == 'Главное меню':
        handle_main_menu_btn(message)
def remove(message):
    # try:
        username = message.chat.username
        chat_id = message.chat.id
        ads_number = sell.find({'username':username}).count()
        if ads_number==0:
            bot.send_message(message.chat.id, "У вас пока нету объявлений", reply_markup=create_keyboard(delete_buttons,1,False,False))
        else:
            numbers = range(1,ads_number+1)
            str_numbers = [str(i) for i in numbers]
            str_numbers.append('Назад')

            msg = bot.send_message(message.chat.id, "Какое по счету объявление вы хотите удалить?", reply_markup=create_keyboard(str_numbers,1,False,False))
            a = "Ваши объявления\n\n"
            b = 1
            if sell.find({'username':username}).count()==0:
                bot.send_message(message.chat.id, 'У вас пока нету объявлений')
            else:
                pages = get_pages_num({'username':username})
                a = skiplimit(5,1,{'username':username}, chat_id,pages)

                keyboard = types.InlineKeyboardMarkup(row_width = 2)
                callback_bt1= types.InlineKeyboardButton(text="Назад", callback_data="-1")
                callback_bt2 = types.InlineKeyboardButton(text="Вперед", callback_data="1")
                search_filter = search_filter_dict[chat_id]
                if search_filter.current_page == 1:
                    keyboard.add(callback_bt2)
                elif search_filter.current_page == pages:
                    keyboard.add(callback_bt1)
                else:
                    keyboard.add(callback_bt1, callback_bt2)

                msg1 = bot.send_message(message.chat.id, a, reply_markup=keyboard)
                msg = bot.send_message(message.chat.id, 'Что вы хотите удалить?')
                bot.register_next_step_handler(msg, process_remove_step)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')
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
            msg =bot.send_message(chat_id, "Ok, я удалил {0} объявление".format(seq_num+1))
            bot.register_next_step_handler(msg, remove)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_city_step(message):
    try:
        chat_id = message.chat.id
        city = message.text
        if message.text == 'Назад':
            bazaar(message)
        else:
            if not (city in cities):
                msg = bot.reply_to(message, 'Выберите город из списка')
                bot.register_next_step_handler(msg, process_city_step)
                return
            product = Product(city)

            product_dict[chat_id] = product

            product.city = city
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Нет')
            itembtn2 = types.KeyboardButton('Отправить контакт',request_contact=True)
            markup.add(itembtn1, itembtn2)
            msg = bot.reply_to(message, 'Хотите поделиться своим телефонным номером? Если нет, то с вами свяжутся через ваш username в Телеграме', reply_markup=markup)
            bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_phone_step(message):
    chat_id = message.chat.id
    product = product_dict[chat_id]
    if message.contact:
        product.contact = message.contact.phone_number
    else:
        product.contact = ''

    msg = bot.reply_to(message, 'Теперь выберите криптовалюту.', reply_markup=create_keyboard(coin_names,1,True,False))
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step_buy(message):
    try:
        chat_id = message.chat.id
        currency = message.text
        if currency=="Главное меню":
            bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(main_buttons,1,False,False))
        else:
            if not (currency in ["Все"]+coin_names):
                msg = bot.reply_to(message, 'Выберите криптовалюту из списка')
                bot.register_next_step_handler(msg, process_name_step_buy)
                return

            search_filter = search_filter_dict[chat_id]
            search_filter.currency = currency

            msg = bot.send_message(message.chat.id, "Введите ценовой диапозон, разделенный тире, от меньшего к большому. Например: 2000-5000. Чтобы искать все цены нажмите на кнопку 'Все'",reply_markup=create_keyboard(words=search_menu,width=1))

            bot.register_next_step_handler(msg, process_find_price)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if name=="Главное меню":
            bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(main_buttons,1,False,False))
        else:
            if not (name in coin_names):
                msg = bot.reply_to(message, 'Выберите криптовалюту из списка')
                bot.register_next_step_handler(msg, process_name_step)
                return

            product = product_dict[chat_id]
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
        msg = bot.reply_to(message, 'Какую комиссию вы берете? От 0 до 20')
        bot.register_next_step_handler(msg, process_percent_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_percent_step(message):
    try:
        chat_id = message.chat.id
        percent = message.text
        rng = range(0,21)
        if not percent.isdigit():
            msg = bot.reply_to(message, 'Процент комиссии должен быть числом')
            bot.register_next_step_handler(msg, process_percent_step)
            return
        if int(percent) not in rng:
            msg = bot.reply_to(message, 'Процент комиссии должен быть между 0 и 20')
            bot.register_next_step_handler(msg, process_percent_step)
            return
        product = product_dict[chat_id]
        product.percent = percent
        msg = bot.reply_to(message, 'По какому курсу?', reply_markup = create_keyboard(exchanges,2,False,False))
        bot.register_next_step_handler(msg, process_exchange_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_exchange_step(message):
    try:
        chat_id = message.chat.id
        exchange = message.text.upper()
        product = product_dict[chat_id]
        if not (exchange in exchanges):
            msg = bot.reply_to(message, 'Выберите биржу из списка')
            bot.register_next_step_handler(msg, process_exchange_step)
            return
        product.exchange = exchange
        msg = bot.reply_to(message, 'Есть ли у вас комментарии? Если нет, то можете оставить пустым', reply_markup=create_keyboard(['Нет'],1,False,False))
        bot.register_next_step_handler(msg, process_comment_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


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
        msg = bot.reply_to(message, 'Подтвердите объявление о продаже\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange +'\nГород: ' + product.city+'\nUsername: @'+username+'\nКомментарий: '+product.comment, reply_markup=create_keyboard(buttons,2,False,False))
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
            sell.insert_one({
                'name': product.name,
                'price': int(product.price),
                'percent': int(product.percent),
                'exchange': product.exchange,
                'city': product.city,
                'username': username,
                'comment': product.comment,
                'phone_number': product.contact,
                "created_at": datetime.datetime.utcnow()
            })
            bot.send_message(chat_id, 'Вы успешно опубликовали!\n\nВалюта: ' + product.name + '\nСумма покупки: ' + '$'+str(product.price) + '\nПроцент: ' + product.percent+'%' + '\nКурс: '+ product.exchange +'\nГород: ' + product.city+'\nUsername: @'+username+'\nКомментарий: '+product.comment, reply_markup = create_keyboard(main_buttons,1,False,False))
        else:
            bot.send_message(chat_id, 'Вы отменили объявление о продаже', reply_markup=create_keyboard(main_buttons,1,False,False))
    except Exception as e:
        bot.reply_to(message, 'oooops')

def create_keyboard(words=None, width=None, isOneTime=False, isPhone=False):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=isOneTime, row_width=width, resize_keyboard = True)
    for word in words:
        keyboard.add(types.KeyboardButton(text=word, request_contact=isPhone))
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

@bot.message_handler(commands=['settings'])
def settings(message):
    msg = bot.send_message(message.chat.id, 'Выберите настройки', reply_markup=create_keyboard(settings_buttons+['Главное меню'],1,False,False))
    bot.register_next_step_handler(msg, process_settings_step)

def process_settings_step(message):
    if message.text == 'Пакеты':
        list_packages(message)
    elif message.text=='Главное меню':
        handle_main_menu_btn(message)


@bot.message_handler(regexp="/Главное меню/")
def handle_main_menu_btn(message):
	bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=create_keyboard(words=main_buttons,width=1))

if __name__ == '__main__':
    db = client.fuckingtelegrambot
    sell = db.sell
    traders = db.traders
    bot.polling(none_stop=True)
