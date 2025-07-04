from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["saeb"]

client.close)

print(db.list_collection_names())

