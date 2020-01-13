import csv
import os

from src import cleaning
from src import util


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
        cleaning.clean(data_file, collection_lane)


def run_duplicate_detection(recreate_training_set):
    util.generate_training_set_once(util.training_set_file, util.training_set_gold_standard_file, recreate_training_set)

    cleaning.clean(util.training_set_file, util.training_collection_lane)

    tr = cleaning.train(util.training_set_gold_standard_file, util.training_collection_lane)
    print(tr)

    get_clean_collection(util.restaurants_file, util.standard_collection)

    return cleaning.test(util.gold_standard_file, util.standard_collection, tr)


def cycle(times, summarize=False):
    if summarize:
        summary_file = "./data/results/summary.txt"
        with open(summary_file, "w") as summary:
            summary.write("x,phone_threshold,name_threshold,address_threshold\n")

    for perdec in range(0, 11):
        util.training_set_size = (864 * perdec) // 10
        results_file = "./data/results/precision_recall_{}.txt".format(perdec)
        if not os.path.isfile(results_file):
            with open(results_file, "a") as file:
                file.write(
                    "phone_threshold,name_threshold,address_threshold,training_data_precision,training_data_recall,test_data_precision,test_data_recall\n")
        for i in range(0, times):
            test_result = run_duplicate_detection(True)
            with open(results_file, "a") as f:
                f.write("{:3.1f}, {:3.1f}, {:3.1f}, {:5.3f}, {:5.3f}, {:5.3f}, {:5.3f}\n".format(test_result[0][0],
                                                                                                 test_result[0][1],
                                                                                                 test_result[0][2],
                                                                                                 test_result[0][3],
                                                                                                 test_result[0][4],
                                                                                                 test_result[1],
                                                                                                 test_result[2]))

        if summarize:
            count = 0
            phone = 0
            name = 0
            address = 0

            with open(results_file, newline='') as f:
                r = csv.DictReader(f, delimiter=",", quotechar='"')
                for entry in r:
                    count += 1
                    phone += float(entry["phone_threshold"])
                    name += float(entry[" name_threshold"])
                    address += float(entry[" address_threshold"])

            with open(summary_file, "a") as summary:
                summary.write("{:3d},{:6.4f},{:6.4f},{:6.4f}\n".format(perdec * 10,
                                                                       phone / count,
                                                                       name / count,
                                                                       address / count))


def create_documentation_data():
    for i in range(0, 30):
        cycle(10)
    cycle(0,summarize=True)