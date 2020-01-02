from src import mongo_import
from src.audit import aggregate_mongodb
from src import predictability_checker
from src import util
from src import standardize_restaurant_data
#mongo_import.import_restaurants_data("./data/restaurants.tsv")

mongo_import.init_cleaning()

unique_counts = aggregate_mongodb.group_and_count(util.current_collection_name(), util.city_field)
for entity in unique_counts:
    print(entity)

standardize_restaurant_data.standardize_cities()

print("\n\n\n")
unique_counts = aggregate_mongodb.group_and_count(util.current_collection_name(), util.city_field)
for entity in unique_counts:
    print(entity)

standardize_restaurant_data.standardize_phone_numbers()

print("\n\n\n")
unique_counts = aggregate_mongodb.group_and_count(util.current_collection_name(), util.phone_field)
for entity in unique_counts:
    print(entity)


#predictability_checker.check_indications1("imported")
