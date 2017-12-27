from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint


client = MongoClient('mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot')

print(client)