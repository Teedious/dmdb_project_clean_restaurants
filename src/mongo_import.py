from pymongo import MongoClient
from src import tsvimport
from src import util

client = MongoClient(util.mongodb_server)
restaurants_db = client[util.restaurants_db]

def import_restaurants_data(file_path):


    if 0 < restaurants_db.imported.estimated_document_count():
        print("Data already imported. Deleting {} entries.".format(restaurants_db.imported.estimated_document_count()))
        restaurants_db.imported.delete_many({})

    dicts = tsvimport.getDicts(file_path)["data"]

    print("Importing data...")
    restaurants_db.imported.insert_many(dicts)
    print("done ({} entries)".format(restaurants_db.imported.estimated_document_count()))


def init_cleaning():
    util.current_stage = 0
    for stage in restaurants_db.list_collection_names(filter={"name": {"$regex": r"^{}\d+".format(util.standard_collection)}}):
        restaurants_db.drop_collection(stage)

    restaurants_db[util.imported_collection].aggregate([
        {'$match':{}},
        {'$out':util.current_collection_name()}
        ])