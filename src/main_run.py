from src import mongo_import
from src.audit import aggregate_mongodb
import pprint

mongo_import.import_restaurants_data("./data/restaurants.tsv")

unique_counts = aggregate_mongodb.count_unique_values("imported","address")

for entity in unique_counts:
    print(entity)