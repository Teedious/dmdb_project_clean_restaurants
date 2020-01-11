import csv
import os
import subprocess

from src import util

fieldnames = None


def import_restaurants_data(file_path, collection_lane):
    cur_collection = util.current_collection(collection_lane)
    if 0 < cur_collection.estimated_document_count():
        print("Data already imported. Deleting {} entries.".format(cur_collection.estimated_document_count()))
        cur_collection.delete_many({})

    dicts = import_tsv(file_path)["data"]

    print("Importing data...")
    cur_collection.insert_many(dicts)
    print("done ({} entries)".format(cur_collection.estimated_document_count()))


def init_cleaning(file_path, collection_lane):
    util.current_stage[collection_lane] = 0
    for stage in util.get_restaurant_database().list_collection_names(
            filter={"name": {"$regex": r"^{}\d+".format(collection_lane)}}):
        util.get_restaurant_database().drop_collection(stage)

    import_restaurants_data(file_path, collection_lane)


def export_restaurants_data(file_path, collection_name, field_names):
    subprocess.call(["mongoexport",
                     "--uri={}/{}".format(util.mongodb_server, util.restaurants_db),
                     "--collection={}".format(collection_name),
                     "--type=csv",
                     "--fields={}".format(",".join(field_names)),
                     "--out={}".format(file_path)
                     ])

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        lines = [a for a in reader]

    os.remove(file_path)

    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, field_names, delimiter="\t", quotechar='"')
        writer.writeheader()
        writer.writerows(lines)


def import_tsv(data):
    with open(data, newline='') as f:
        r = csv.DictReader(f, delimiter="\t", quotechar='"')
        return {"meta": r, "data": [dict for dict in r]}
