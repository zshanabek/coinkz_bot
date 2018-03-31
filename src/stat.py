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

client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')
db = client.fuckingtelegrambot
sell = db.sell
traders = db.traders
feedbacks = db.feedbacks
users = db.users
sell_new = db.sell_new
a=0
for i in users.find():
	print(i)
	a+=1
print(a)

    