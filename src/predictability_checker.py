import csv
from src import util

data_map = {}


def init(fieldnames, data_list):
    for name in fieldnames:
        data_map[name] = {}
    for row in data_list:
        for row_key in row.keys():
            data_map[row_key][row[row_key]] = {}
            for data_name in fieldnames:
                data_map[row_key][row[row_key]][data_name] = set()


def check_indications(data):
    fieldnames = data.fieldnames
    data_list = list(data)
    init(fieldnames, data_list)

    for row in data_list:
        for row_key in row.keys():
            for data_name in row.keys():
                data_map[row_key][row[row_key]][data_name].add(row[data_name])
    print("done creating dictionary")

    prediction_map = {}
    for key in fieldnames:
        prediction_map[key] = {}
        for key1 in fieldnames:
            prediction_map[key][key1] = {
                "count": 0,
                "sum": 0
            }

    for fieldname in fieldnames:
        for f_key in data_map[fieldname].keys():
            item = data_map[fieldname][f_key]
            for keyfield in item.keys():
                prediction_map[fieldname][keyfield]["count"] += 1
                prediction_map[fieldname][keyfield]["sum"] += len(item[keyfield])
    print("done summing dictionary")

    avg_map = {}
    for top_key in prediction_map.keys():
        sum = 0
        count = 0
        for fieldname in prediction_map[top_key].keys():
            sum += prediction_map[top_key][fieldname]["sum"]
            count += prediction_map[top_key][fieldname]["count"]
        avg_map[top_key] = sum / count

    return avg_map


from bson.code import Code


def check_indications1(collection):
    db = util.get_restaurant_database()
    for source_field in util.field_names:
        for target_field in util.field_names:
            map = Code("function () {" + \
                       "emit(this.{}, [this.{}]);".format(source_field, target_field)) + \
                  "}"
            reduce = Code("function(key, values){"
                          "return [values.length];"
                          "}")
            result = db[collection].map_reduce(map, reduce, {"replace": "mydict"})
            for doc in db["mydict"].find():
                print(doc)
            print("----")
