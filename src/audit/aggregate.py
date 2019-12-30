from src.tsvimport import getDicts
import re

data = "../../data/restaurants.tsv"


def aggregate(dictreader):
    aggregates = {}
    for col in dictreader["meta"].fieldnames:
        aggregates[col] = {}

    for row in dictreader["data"]:
        for col in aggregates.keys():
            cell = row[col]
            aggregates[col][cell] = aggregates[col].get(cell, 0) + 1
    return aggregates


def aggregate_col(iterable):
    aggregates = {}
    for cell in iterable:
        aggregates[cell] = aggregates.get(cell, 0) + 1
    return aggregates


def get_col(col, dictreader):
    retval = []
    for row in dictreader["data"]:
        retval.append(row[col])
    return retval


def aggregate_street_types(dictreader):
    addr_col = get_col("address", dictreader)
    directions = re.compile(r"( (at|near|between|off|in) )")
    street_type = re.compile(r"([^ ]+)$")
    addr_col = [row for row in map(lambda x: x[:re.search(directions,x).start() if re.search(directions, x) else len(x)].strip(), addr_col)]
    addr_col = [row for row in map(lambda x: x[:re.search(r"\.",x).start()+1 if re.search(r"\.", x) else len(x)].strip(), addr_col)]
    addr_col = [match.group(0) for match in map(lambda x: re.search(street_type, x), addr_col)]
    aggregates = aggregate_col(addr_col)

    for key in aggregates.keys():
        print("{:10s}\t\t{}".format(key, aggregates[key]))


dict_reader = getDicts(data)
aggregate_street_types(dict_reader)
