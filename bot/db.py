from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint


client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

db = client.fuckingtelegrambot
# db.sell.delete_many({})   
# db.traders.delete_many({})   

sell = db.sell
traders = db.traders

# traders.update_one({'username':'zshanabek'},{'$set':{'is_paid':None}})

cursor = traders.find({})
for document in cursor: 
    pprint(document)