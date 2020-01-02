import re
from src import util


def standardize_addresses():
    current_collection = util.current_collection()


def standardize_phone_numbers():
    current_collection = util.current_collection()
    data = current_collection.find()

    non_number = re.compile(r"\D+")
    non_number_start_end = re.compile(r"(^\D+)|(\D+$)")

    next_collection = util.go_to_next_stage()


    for entry in data:
        phone: str = entry.get(util.phone_field)
        if not phone:
            next_collection.save(entry)
            continue

        phone = re.sub(non_number_start_end,"",phone)
        phone = re.sub(non_number,"-",phone)
        entry[util.phone_field] = phone

        next_collection.save(entry)

def standardize_cities():
    current_collection = util.current_collection()

    replace_dict = {
        'la': 'los angeles',
        'west la': 'los angeles',
        'w. hollywood': 'west hollywood',
        'new york': 'new york city',
        'st. boyle hts.': 'boyle heights',
    }
    district_dict = util.districts_as_dictionary()

    data = current_collection.find({})
    next_collection = util.go_to_next_stage()

    for entry in data:
        std_city = entry.get(util.city_field)
        if not std_city:
            continue

        std_city = replace_dict.get(std_city, std_city)
        std_city = district_dict.get(std_city, std_city)

        entry[util.city_field] = std_city
        next_collection.save(entry)





