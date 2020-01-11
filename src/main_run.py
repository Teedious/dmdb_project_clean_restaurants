import csv
import os

from src import cleaning
from src import util
for a in range(0,2):
    summary_file = "./data/results/summary.txt"
    with open(summary_file, "w") as summary:
        summary.write("x,phone_threshold,name_threshold,address_threshold\n")

    for perdec in range(1, 11):
        util.training_set_size = (864 * perdec) // 10
        results_file = "./data/results/precision_recall_{}.txt".format(perdec)
        if not os.path.isfile(results_file):
            with open(results_file, "a") as file:
                file.write("phone_threshold,name_threshold,address_threshold,training_data_precision,training_data_recall,test_data_precision,test_data_recall\n")
        for i in range(0, 5):
            util.generate_training_set_once(util.training_set_file, util.training_set_gold_standard_file, True)

            cleaning.clean(util.training_set_file, util.training_collection_lane)

            tr = cleaning.train(util.training_set_gold_standard_file, util.training_collection_lane)
            print(tr)

            cleaning.clean(util.restaurants_file, util.standard_collection)

            cleaning.test(util.gold_standard_file, util.standard_collection, tr, results_file)

        count = 0
        phone = 0
        name = 0
        address = 0

        with open(results_file, newline='') as f:
            r = csv.DictReader(f, delimiter=",", quotechar='"')
            for entry in r:
                count +=1
                phone += float(entry["phone_threshold"])
                name += float(entry[" name_threshold"])
                address += float(entry[" address_threshold"])

        with open(summary_file, "a") as summary:
            summary.write("{:3d},{:6.4f},{:6.4f},{:6.4f}\n".format(perdec*10,
                                                  phone/count,
                                                  name/count,
                                                  address/count))