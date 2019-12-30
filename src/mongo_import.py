from pymongo import MongoClient
from src import tsvimport
from src.static_strings import mongodb_server

def import_restaurants_data(file_path):
    client = MongoClient(mongodb_server)
    restaurants_db = client.restaurants_db

    if 0 < restaurants_db.imported.estimated_document_count():
        print("Data already imported. Deleting {} entries.".format(restaurants_db.imported.estimated_document_count()))
        restaurants_db.imported.delete_many({})

    dicts = tsvimport.getDicts(file_path)["data"]

    print("Importing data...")
    restaurants_db.imported.insert_many(dicts)
    print("done ({} entries)".format(restaurants_db.imported.estimated_document_count()))
