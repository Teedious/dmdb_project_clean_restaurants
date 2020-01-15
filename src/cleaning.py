import pprint

from src import detect_duplicates
from src import import_export
from src import predictability_checker
from src import standardize_restaurant_data
from src import util


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


def train(gold_standard_file, collection_lane):
    steps = 10
    real_duplicates = util.get_gold_standard(gold_standard_file)
    train_temp = {}
    detect_duplicates.reset_duplicates(collection_lane)
    for i in range(0, steps + 1):
        for j in range(0, steps + 1):
            for k in range(0, steps + 1):
                phone_threshold, name_threshold, address_threshold = i / steps, j / steps, k / steps
                found_duplicates = detect_duplicates.get_duplicates(collection_lane,
                                                                    phone_threshold,
                                                                    name_threshold,
                                                                    address_threshold)

                intersect = found_duplicates.intersection(real_duplicates)

                precision = len(intersect) / len(found_duplicates)
                recall = len(intersect) / len(real_duplicates)

                val = precision * recall

                train_temp[val] = (phone_threshold, name_threshold, address_threshold, precision, recall)
    t1 = list(train_temp)
    best = max(t1)
    training_result = train_temp[best]
    return training_result


def test(gold_standard_file, collection_lane, tr_result, verbose):
    real_duplicates = util.get_gold_standard(gold_standard_file)
    found_duplicates = detect_duplicates.get_duplicates(collection_lane, tr_result[0], tr_result[1], tr_result[2])

    intersect = found_duplicates.intersection(real_duplicates)

    precision = len(intersect) / len(found_duplicates)
    recall = len(intersect) / len(real_duplicates)
    if verbose:
        print("phone    |name     |address  |training |training|test     |test  ")
        print("threshold|threshold|threshold|precision|recall  |precision|recall")
        print("{:9.1f}|{:9.1f}|{:9.1f}|{:9.3f}|{:8.3f}|{:9.3f}|{:6.3f}\n".format(tr_result[0],
                                                                                       tr_result[1],
                                                                                       tr_result[2],
                                                                                       tr_result[3],
                                                                                       tr_result[4],
                                                                                       precision,
                                                                                       recall))

    return (tr_result, precision, recall)


def get_clean_collection(data_file, collection_lane):
    lanes = []
    for coll in util.get_restaurant_database().list_collection_names(
            filter={"name": {"$regex": r"^{}\d+".format(collection_lane)}}):
        coll: str
        coll = coll.replace(collection_lane, "")
        lanes.append(int(coll))

    if len(lanes) > 0:
        util.current_stage[collection_lane] = max(lanes)
    else:
        clean(data_file, collection_lane)


def run_duplicate_detection(recreate_training_set=False, verbose=True):
    util.generate_training_set_once(util.training_set_file, util.training_set_gold_standard_file, recreate_training_set)

    clean(util.training_set_file, util.training_collection_lane)

    tr = train(util.training_set_gold_standard_file, util.training_collection_lane)
    print(tr)

    get_clean_collection(util.restaurants_file, util.standard_collection)

    return test(util.gold_standard_file, util.standard_collection, tr, verbose)
