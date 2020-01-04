from src import util
import re


def group_and_count(collection, field):
    restaurtants_db = util.get_restaurant_database()
    return restaurtants_db[collection].aggregate(
        [
            # The first stage in this pipe is to group data
            {'$group':
                 {'_id': "$"+str(field),
                  "count":
                      {'$sum': 1}
                  }
             },
            {"$sort": {"_id": 1}}
        ]
    )


def unwind_group_and_count(collection, field):
    restaurtants_db = util.get_restaurant_database()
    return restaurtants_db[collection].aggregate(
        [
            {"$unwind":"${}".format(field)},
            {'$group':
                 {'_id': "${}".format(field),
                  "count":
                      {'$sum': 1}
                  }
             },
            {"$sort": {"_id": 1}}
        ]
    )

def sort(collection, field):
    restaurtants_db = util.get_restaurant_database()
    return restaurtants_db[collection].aggregate(
        [
            {"$sort": {field: 1}}
        ]
    )


def aggregate_street_types():
    addr_col = [entry.get(util.address_field) for entry in util.current_collection().find({}, {util.id_pm: 0, util.address_field: 1})]
    directions = re.compile(r"( (at|near|between|off|in) )")
    street_type = re.compile(r'\b\S+\.?(?: [a-z]\.?)?$',re.IGNORECASE)
    addr_col = [row for row in
                map(lambda x: x[:re.search(directions, x).start() if re.search(directions, x) else len(x)].strip(),
                    addr_col)]
    addr_col = [row for row in
                map(lambda x: x[:re.search(r"\.", x).start() + 1 if re.search(r"\.", x) else len(x)].strip(), addr_col)]
    addr_col = [match.group(0) for match in map(lambda x: re.search(street_type, x), addr_col)]
    temp_collection = util.get_temp_collection()
    addr_col = [{util.address_field:address} for address in addr_col]
    temp_collection.insert_many(addr_col)

    aggregates = group_and_count(temp_collection.name, util.address_field)

    for entry in aggregates:
        print(entry)

