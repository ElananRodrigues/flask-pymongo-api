from pymongo import MongoClient
from bson.objectid import ObjectId

class ClientMongoModel():

	def db(self):
		db = MongoClient("mongodb://localhost:27017/")['base']['estudantes']
		return db