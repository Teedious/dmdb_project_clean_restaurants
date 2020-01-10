import pprint
import subprocess
from src import import_export
from src import util
from src import standardize_restaurant_data
from src import detect_duplicates
from src import predictability_checker


def clean(file_path=util.restaurants_file, collection_lane=util.standard_collection):
    import_export.init_cleaning(file_path, collection_lane)

    print("Average of different entries in other fields for a given entry")
    practicabilities = predictability_checker.check_indications(util.field_names,
                                                    util.current_collection(collection_lane)
                                                        .find({}, util.get_fields_projection()))
    pprint.pprint(practicabilities)

    print("Standardizing addresses")
    standardize_restaurant_data.standardize_addresses(collection_lane)

    print("Standardizing cities")
    standardize_restaurant_data.standardize_cities(collection_lane)

    print("Standardizing phone numbers")
    standardize_restaurant_data.standardize_phone_numbers(collection_lane)

    print("Standardizing restaurant types")
    standardize_restaurant_data.standardize_restaurant_types(collection_lane)

    print("Average of different entries in other fields for a given entry")
    practicabilities = predictability_checker.check_indications(util.field_names,
                                                    util.current_collection(collection_lane).find({},
                                                                                                  util.get_fields_projection()))
    pprint.pprint(practicabilities)


def train(file_path, collection_lane):
    steps = 50
    real_duplicates = util.get_gold_standard()
    for i in range(0, steps + 1):
        for j in range(0, steps + 1):
            for k in range(0, steps + 1):
                found_duplicates = detect_duplicates.get_duplicates(i / steps, j / steps, k / steps)

                intersect = found_duplicates.intersection(real_duplicates)

                precision = len(intersect) / len(found_duplicates)
                recall = len(intersect) / len(real_duplicates)

