import pprint
import subprocess
from src import mongo_import, aggregate_mongodb
from src import util
from src import standardize_restaurant_data
from src import detect_duplicates
from src import  predictability_checker


a = {"_id":0}
for m in util.field_names:
    a[m]=1


# detect_duplicates.qgram_distance(2,"Lorem Ipsum dolor sit amett","Lrem dolor sit amet")
# detect_duplicates.qgram_distance(2,"Lorem Ipsum dolor sit amet","Lorem Ipsum dolor sit amez")
# detect_duplicates.qgram_distance(2,"Lorem Ipsum dolor sit amet","Lorem Ipsum dolor sit amet")
# detect_duplicates.qgram_distance(2,"Lorem Ipsum dolor sit amet","Lorem Ipsum dolor sit ame")
#mongo_import.import_restaurants_data("./data/restaurants.tsv")
mongo_import.init_cleaning()

map_ = predictability_checker.check_indications(util.field_names,util.current_collection().find({},a))
print("Average of different entries in other fields for a given entry")
pprint.pprint(map_)

print("Standardizing addresses")
addr = standardize_restaurant_data.standardize_addresses()
# pprint.pprint(addr)
print("Standardizing cities")
standardize_restaurant_data.standardize_cities()
print("Standardizing phone numbers")
standardize_restaurant_data.standardize_phone_numbers()
print("Standardizing restaurant types")
standardize_restaurant_data.standardize_restaurant_types()

map_ = predictability_checker.check_indications(util.field_names,util.current_collection().find({},a))
print("Average of different entries in other fields for a given entry")
pprint.pprint(map_)

detect_duplicates.test1()
# unique_counts = aggregate_mongodb.unwind_group_and_count(util.current_collection_name(), util.name_field)
# for entity in unique_counts:
#     print(entity)

# subprocess.call(["mongoexport",
#                  "--db={}".format(util.restaurants_db),
#                  "--collection={}".format(util.current_collection_name()),
#                  "--type=csv",
#                  "--fields={}".format(",".join(util.field_names)),
#                  "--out={}".format("./data/export/restaurants_export.csv")
#                  ])
#
#
#predictability_checker.check_indications1("imported")
