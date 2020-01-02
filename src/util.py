import pymongo
from pymongo import MongoClient

mongodb_server = 'mongodb://localhost:27017/'
# mongodb_server = "mongodb+srv://wmdb_temp:8EDM3sv5WiMBr26K@wmdb-01-7b21x.mongodb.net/test?retryWrites=true&w=majority"
restaurants_db = "restaurants_db"

imported_collection = "imported"
current_stage = 0
standard_collection = "cleaning_stage"

id_pm = "_id"
id_field = "id"
name_field = "name"
address_field = "address"
city_field = "city"
phone_field = "phone"
type_field = "type"
field_names = [id_field, name_field, address_field, city_field, phone_field, type_field]


def current_collection() -> pymongo.collection.Collection:
    return MongoClient(mongodb_server)[restaurants_db][current_collection_name()]


def current_collection_name():
    return standard_collection + str(current_stage)


def go_to_next_stage():
    global current_stage
    current_stage += 1
    return current_collection()


def get_restaurant_database():
    return MongoClient(mongodb_server)[restaurants_db]


def get_similarity_index(a, b):
    return 1 if a == b else 0


def is_similar(a, b):
    return get_similarity_index(a, b) > 0


def districts_as_dictionary():
    ret = {}
    for city in districts.keys():
        for district in districts[city]:
            ret[district] = city
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
