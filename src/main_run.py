import csv
import os
import statistics

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


def run_duplicate_detection(recreate_training_set=False, verbose=True):
    util.generate_training_set_once(util.training_set_file, util.training_set_gold_standard_file, recreate_training_set)

    cleaning.clean(util.training_set_file, util.training_collection_lane)

    tr = cleaning.train(util.training_set_gold_standard_file, util.training_collection_lane)
    print(tr)

    get_clean_collection(util.restaurants_file, util.standard_collection)

    return cleaning.test(util.gold_standard_file, util.standard_collection, tr, verbose)


def cycle(times, summarize=False):
    if summarize:
        summary_file = "./data/results/summary.txt"
        with open(summary_file, "w") as summary:
            summary.write("x,phone_threshold,phone_threshold_stdev,"
                          "name_threshold,name_threshold_stdev,"
                          "address_threshold,address_threshold_stdev,"
                          "training_data_precision,training_data_precision_stdev,"
                          "training_data_recall,training_data_recall_stdev,"
                          "test_data_precision,test_data_precision_stdev,"
                          "test_data_recall,test_data_recall_stdev\n")

    for perdec in range(1, 11):
        util.training_set_size = (864 * perdec) // 10
        results_file = "./data/results/precision_recall_{}.txt".format(perdec)
        if not os.path.isfile(results_file):
            with open(results_file, "a") as file:
                file.write(
                    "phone_threshold,name_threshold,address_threshold,training_data_precision,training_data_recall,test_data_precision,test_data_recall\n")
        for i in range(0, times):
            test_result = run_duplicate_detection(recreate_training_set=True, verbose=False)
            with open(results_file, "a") as f:
                f.write("{:3.1f}, {:3.1f}, {:3.1f}, {:5.3f}, {:5.3f}, {:5.3f}, {:5.3f}\n".format(test_result[0][0],
                                                                                                 test_result[0][1],
                                                                                                 test_result[0][2],
                                                                                                 test_result[0][3],
                                                                                                 test_result[0][4],
                                                                                                 test_result[1],
                                                                                                 test_result[2]))

        if summarize:
            keys = None
            stuff = {}
            with open(results_file, newline='') as f:
                r = csv.DictReader(f, delimiter=",", quotechar='"')
                l = list(r)
                keys = list(r.fieldnames)
                for key in r.fieldnames:
                    if key not in stuff:
                        stuff[key] = []
                for entry in l:
                    for key in r.fieldnames:
                            stuff[key].append(float(entry[key]))
            out={}
            out_string = ""
            for key in keys:
                out[key]=[]
                cur_list = stuff[key]
                out_list = out[key]
                out_list.append(sum(cur_list)/len(cur_list))
                out_list.append(statistics.stdev(cur_list))
                out_string += ",{:6.3f},{:6.3f}".format(out_list[0],out_list[1])


            out_string = "{:3d}".format(perdec*10) + out_string +"\n"
            with open(summary_file, "a") as summary:
                summary.write(out_string)


def create_documentation_data(size):
    for i in range(0, size):
        cycle(1)
    cycle(0, summarize=True)


# ################################
# util.training_set_size = 86
# run_duplicate_detection(True)
create_documentation_data(0)
# ################################
