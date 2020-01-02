from src import util


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

def check_util():
    print(str(util.current_stage))
    util.current_stage +=1