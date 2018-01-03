from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import datetime
import random
from random import randrange
from faker import Faker

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


d1 = datetime.datetime.strptime('1/1/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.datetime.strptime('2/1/2018 4:50 AM', '%m/%d/%Y %I:%M %p')
fake = Faker()

client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

db = client.fuckingtelegrambot

# db.sell.delete_many({})   
# db.traders.delete_many({})   

coin_names = ['Bitcoin','Ethereum','Litecoin','NEO','NEM','Stratis','BitShares','Stellar','Ripple','Dash','Lisk','Waves','Ethereum Classic','Monero','ZCash'] 

cities = ['Алматы','Астана','Шымкент','Караганда','Актобе','Тараз','Павлодар','Семей','Усть-Каменогорск','Уральск','Костанай','Кызылорда','Петропавловск','Кызылорда','Атырау','Актау','Талдыкорган']

exchanges =['COINMARKETCAP', 'BLOCKCHAIN', 'CEX.IO', 'ALONIX', 'BITTREX', 'EXMO.ME', 'BITFINEX', 'POLONIEX']

usernames = ['iSapar', 'zshanabek', 'Yermuhanbet', 'KassymkhanTJ', 'bimurat_mukhtar','vakidzaci']
sell = db.sell
traders = db.traders

# for i in range(0,100):
#     sell.insert_one({
#         'name': random.choice(coin_names),
#         'price': random.randint(10, 200000),
#         'percent': random.randint(0, 20),
#         'exchange': random.choice(exchanges),                
#         'city': random.choice(cities),
#         'username': random.choice(usernames),
#         'comment': fake.text(),      
#         'phone_number': fake.phone_number(),
#         "created_at": random_date(d1, d2)
#     })

cursor = sell.find({ 'city': 'Астана' })

c1 = cursor.find({'exchange':'Bitcoin'})
for document in c1: 
    pprint(document)
