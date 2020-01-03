from src import mongo_import, aggregate_mongodb
from src import util
from src import standardize_restaurant_data
#mongo_import.import_restaurants_data("./data/restaurants.tsv")



mongo_import.init_cleaning()

standardize_restaurant_data.standardize_addresses()
standardize_restaurant_data.standardize_cities()
standardize_restaurant_data.standardize_phone_numbers()

unique_counts = aggregate_mongodb.group_and_count(util.current_collection_name(), util.type_field)
for entity in unique_counts:
    print(entity)
#
#
#predictability_checker.check_indications1("imported")
