from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import datetime

client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

db = client.fuckingtelegrambot

# db.sell.delete_many({})   
# db.traders.delete_many({})   

sell = db.sell
traders = db.traders

result = sell.insert_one({"last_modified": datetime.datetime.utcnow()})
cursor = sell.find({"price": {"$gte": 0, "$lte": 50000}})

for document in cursor: 
    pprint(document)