from pymongo import MongoClient


client = MongoClient("mongodb+srv://wmdb_temp:8EDM3sv5WiMBr26K@wmdb-01-7b21x.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
print(db.find())