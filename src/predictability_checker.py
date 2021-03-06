data_map = {}


def init(fieldnames, data_list):
    for name in fieldnames:
        data_map[name] = {}
    for row in data_list:
        for row_key in row.keys():
            data_map[row_key][str(row[row_key])] = {}
            for data_name in fieldnames:
                data_map[row_key][str(row[row_key])][data_name] = set()


def check_indications(fieldnames, data):
    data_list = list(data)
    init(fieldnames, data_list)

    for row in data_list:
        for row_key in row.keys():
            for data_name in row.keys():
                data_map[str(row_key)][str(row[row_key])][str(data_name)].add(str(row[data_name]))
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
