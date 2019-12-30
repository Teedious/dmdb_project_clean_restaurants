import pymongo,re


def standardize_phone_numbers():
    client = pymongo.MongoClient("mongodb+srv://wmdb_temp:8EDM3sv5WiMBr26K@wmdb-01-7b21x.mongodb.net/test?retryWrites=true&w=majority")
    restaurants_db = client.restaurants_db

    non_number = re.compile(r"\D+")

    restaurants = restaurants_db.imported.find()

    restaurants_db.imported.aggregate([
        {
            "$match": { "name": "bar" }
        }, 
        {
            "$project": { "name": { "$concat": ["foo", "-", "$name"] }}
        }, 
        {
            "$out": "prefixedTest"
        }])