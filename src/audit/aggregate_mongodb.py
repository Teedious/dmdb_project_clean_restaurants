from pymongo import MongoClient
from bson.son import SON
from src import static_strings


def count_unique_values(collection, field):
    restaurtants_db = MongoClient(static_strings.mongodb_server)[static_strings.restaurants_db]
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