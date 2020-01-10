import math

import pymongo
from pymongo import MongoClient
import random
from src import import_export
import os

# mongodb_server = 'mongodb://localhost:27017/'
mongodb_server = "mongodb+srv://wmdb_temp:8EDM3sv5WiMBr26K@wmdb-01-7b21x.mongodb.net"
restaurants_db = "restaurants_db"
imported_collection = "imported"
temp_collection = "temp_collection"
current_stage = {}
training_set_size = 100
standard_collection = "cleaning_stage"
collection_lane_a = "collection_lane_a"
collection_lanes = [standard_collection, collection_lane_a]

gold_standard_file = "./data/restaurants_DPL.tsv"
training_set_file = "./data/restaurants_training.tsv"
training_set_gold_standard_file = "./data/restaurants_training_DPL.tsv"
restaurants_file = "./data/restaurants.tsv"
export_file = "./data/export/restaurants_export.tsv"

id_pm = "_id"
id_field = "id"
name_field = "name"
address_field = "address"
city_field = "city"
phone_field = "phone"
type_field = "type"
field_names = [id_field, name_field, address_field, city_field, phone_field, type_field]


def get_fields_projection():
    a = {"_id": 0}
    for m in field_names:
        a[m] = 1
    return a


def get_temp_collection():
    MongoClient(mongodb_server)[restaurants_db].drop_collection(temp_collection)
    return MongoClient(mongodb_server)[restaurants_db][temp_collection]


def current_collection(collection_lane=standard_collection) -> pymongo.collection.Collection:
    return MongoClient(mongodb_server)[restaurants_db][current_collection_name(collection_lane)]


def current_collection_name(collection_lane=standard_collection):
    return collection_lane + str(current_stage.get(collection_lane, 0))


def copy_current_to_next_stage(collection_lane=standard_collection):
    cur_collection = current_collection(collection_lane)
    cur_collection.aggregate([
        {'$match': {}},
        {'$out': go_to_next_stage(collection_lane).name}
    ])
    return current_collection(collection_lane)


def go_to_next_stage(collection_lane=standard_collection):
    global current_stage
    current_stage[collection_lane] = current_stage.get(collection_lane, 0) + 1
    return current_collection(collection_lane)


def get_restaurant_database():
    return MongoClient(mongodb_server)[restaurants_db]


def get_similarity_index(a, b):
    return 1 if a == b else 0


def is_similar(a, b):
    return get_similarity_index(a, b) > 0


def invert_dictionary_lists(dictionary):
    ret = {}
    for value in dictionary.keys():
        for key in dictionary[value]:
            if key != value:
                ret[key] = value
    return ret


def choose_random_values_once():
    if os.path.isfile(training_set_file):
        return

    import_export.init_cleaning(restaurants_file, collection_lane_a)
    num_entries = current_collection().estimated_document_count()
    duplicate_possibilites = list(range(1,112+1))
    possibilities = list(range(1, num_entries+1))
    duplicate_ratio = len(duplicate_possibilites*2)/len(possibilities)
    choices = []
    choices_import = []

    choose_duplicates = math.floor(training_set_size*duplicate_ratio/2)*2
    duplicate_ratio *=2

    for i in range(0, choose_duplicates//2):
        choice = random.choice(duplicate_possibilites)

        duplicate_possibilites.remove(choice)
        possibilities.remove(choice*2-1)
        possibilities.remove(choice*2)

        choices.append(str(choice*2-1))
        choices.append(str(choice*2))

        choices_import.append({"id1":str(choice*2-1), "id2":str(choice*2)})

    temp_coll = get_temp_collection()
    temp_coll.insert_many(sorted(choices_import,key=lambda x: int(x["id1"])))
    import_export.export_restaurants_data(training_set_gold_standard_file, temp_coll.name, ["id1","id2"])

    for i in range(0,training_set_size-choose_duplicates):
        choice = random.choice(possibilities)
        possibilities.remove(choice)
        choices.append(str(choice))

    a = [a for a in current_collection().find({id_field: {"$in": choices}})]

    go_to_next_stage(collection_lane_a).insert_many(a)

    import_export.export_restaurants_data(training_set_file, current_collection_name(collection_lane_a), field_names)



def get_gold_standard(file_path):
    gold_data = import_export.import_tsv(file_path)
    keys = gold_data["meta"].fieldnames
    ret = set()
    for entry in gold_data["data"]:
        ret.add((int(entry[keys[0]]), int(entry[keys[1]])))
    return ret


districts = {"los angeles":
             # taken from https://en.wikipedia.org/wiki/List_of_districts_and_neighborhoods_of_Los_Angeles
                 ["angelino heights",
                  "arleta",
                  "arlington heights",
                  "arts district",
                  "atwater village",
                  "baldwin hills",
                  "baldwin hills/crenshaw",
                  "baldwin village",
                  "baldwin vista",
                  "beachwood canyon",
                  "bel air",
                  "bel-air",
                  "bel air estates",
                  "benedict canyon",
                  "beverly crest",
                  "beverly glen",
                  "beverly grove",
                  "beverly hills post office",
                  "beverly park",
                  "beverlywood",
                  "boyle heights",
                  "brentwood",
                  "brentwood circle",
                  "brentwood glen",
                  "broadway-manchester",
                  "brookside",
                  "bunker hill",
                  "cahuenga pass",
                  "canoga park",
                  "canterbury knolls",
                  "carthay",
                  "castle heights",
                  "central-alameda",
                  "central city",
                  "century city",
                  "chatsworth",
                  "chesterfield square",
                  "cheviot hills",
                  "chinatown",
                  "civic center",
                  "crenshaw",
                  "crestwood hills",
                  "cypress park",
                  "del rey",
                  "downtown",
                  "eagle rock",
                  "east gate bel air",
                  "east hollywood",
                  "echo park",
                  "edendale",
                  "el sereno",
                  "elysian heights",
                  "elysian park",
                  "elysian valley",
                  "encino",
                  "exposition park",
                  "faircrest heights ",
                  "fairfax",
                  "fashion district",
                  "filipinotown, historic",
                  "financial district",
                  "florence",
                  "flower district",
                  "franklin hills",
                  "gallery row",
                  "garvanza",
                  "glassell park",
                  "gramercy park",
                  "granada hills",
                  "green meadows",
                  "griffith park",
                  "hancock park",
                  "harbor city",
                  "harbor gateway",
                  "harvard heights",
                  "harvard park",
                  "hermon",
                  "highland park",
                  "historic core",
                  "hollywood",
                  "hollywood dell",
                  "hollywood hills",
                  "hollywood hills west",
                  "holmby hills",
                  "hyde park",
                  "jefferson park",
                  "jewelry district",
                  "kinney heights",
                  "koreatown",
                  "ladera",
                  "lafayette square",
                  "lake balboa",
                  "lake view terrace",
                  "larchmont",
                  "laurel canyon",
                  "leimert park",
                  "lincoln heights",
                  "little armenia",
                  "little ethiopia",
                  "little tokyo",
                  "los feliz",
                  "manchester square",
                  "mandeville canyon",
                  "marina peninsula",
                  "mar vista",
                  "melrose hill",
                  "mid-city",
                  "mid-wilshire",
                  "miracle mile",
                  "mission hills",
                  "montecito heights",
                  "monterey hills",
                  "mount olympus",
                  "mount washington",
                  "nichols canyon",
                  "noho arts district",
                  "north hills",
                  "north hollywood",
                  "northridge",
                  "north university park",
                  "old bank district",
                  "outpost estates",
                  "pacific palisades",
                  "pacoima",
                  "palms",
                  "panorama city",
                  "park la brea",
                  "picfair village",
                  "pico robertson",
                  "pico-union",
                  "platinum triangle",
                  "playa del rey",
                  "playa vista",
                  "porter ranch",
                  "rancho park",
                  "reseda",
                  "reynier village",
                  "rose hills",
                  "rustic canyon",
                  "san pedro",
                  "sawtelle",
                  "shadow hills",
                  "sherman oaks",
                  "sherman village",
                  "silver lake",
                  "skid row",
                  "solano canyon",
                  "south central, historic",
                  "south park",
                  "south robertson",
                  "spaulding square",
                  "studio city",
                  "sunland",
                  "sunset junction",
                  "sun valley",
                  "sylmar",
                  "tarzana",
                  "terminal island",
                  "thai town",
                  "toluca lake",
                  "toy district",
                  "tujunga",
                  "university hills",
                  "university park",
                  "university park, north",
                  "valley glen",
                  "valley village",
                  "van nuys",
                  "venice",
                  "vermont knolls",
                  "vermont-slauson",
                  "vermont square",
                  "vermont vista",
                  "victor heights",
                  "victoria park",
                  "village green",
                  "warehouse district",
                  "warner center",
                  "watts",
                  "west adams",
                  "westchester",
                  "westdale",
                  "western heights",
                  "west hills",
                  "westlake",
                  "west los angeles",
                  "westside village",
                  "westwood",
                  "westwood village",
                  "whitley heights",
                  "wholesale district",
                  "wilmington",
                  "wilshire center",
                  "wilshire park",
                  "windsor square",
                  "winnetka",
                  "woodland hills",
                  "yucca corridor"],
             "new york city":
             # taken from https://en.wikipedia.org/wiki/Boroughs_of_New_York_City
                 ["the bronx",
                  "brooklyn",
                  "manhattan",
                  "queens",
                  "staten island"]
             }

street_suffix_abbreviations = {
    # subset of list at https://pe.usps.com/text/pub28/28apc_002.htm
    "alley": ["allee", "aly", "ally", "aly"],
    "avenue": ["av", "ave", "ave", "aven", "avenu", "avn"],
    "boulevard": ["blvd", "blvd", "boul", "boulv", "blv"],
    "broadway": [],
    "circle": ["cir", "cir", "circ", "circl", "circle", "crcl", "crcle"],
    "court": ["court", "ct", "ct"],
    "drive": ["dr", "dr", "driv", "drive", "drv"],
    "floor": ["fl"],
    "highway": ["highway", "hwy", "highwy", "hiway", "hiwy", "hway", "hwy"],
    "lane": ["lane", "ln", "ln"],
    "park": ["park", "park", "prk"],
    "parkway": ["pkwy", "parkwy", "pkway", "pkwy", "pky"],
    "pacific coast highway": ["pch"],
    "place": ["pl", "pl"],
    "plaza": ["plaza", "plz", "plz", "plza"],
    "road": ["rd", "rd"],
    "roads": ["rds", "rds"],
    "square": ["sq", "sq", "sqr", "sqre", "squ"],
    "street": ["st", "strt", "st", "str"],
    "streets": ["sts"],
    "valley": ["valley", "vly", "vally", "vlly", "vly"],
    "walk": ["walk", "walk"],
    "way": ["wy", "way", "way"],
    "ways": ["ways", "ways"],
}
