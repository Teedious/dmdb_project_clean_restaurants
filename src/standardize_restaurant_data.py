import pprint
import re
from collections import defaultdict
from src import util


def audit_street_type(street_types, street_name, original):
    street_type_re = re.compile(r'\b\S+\.?(?: \w\.?)?$',re.IGNORECASE)
    expected = util.street_suffix_abbreviations.keys()

    result = street_type_re.search(street_name)
    if result:
        street_type = result.group()
        if street_type not in expected:
            a = street_type.split(" ")[0]
            if a not in expected:
                street_types[street_type].add((street_name, original))


def standardize_addresses():
    current_collection = util.current_collection()
    street_types = defaultdict(set)

    directions = re.compile(r"( (at|near|between|off|in) )")

    abbreviations = "|".join(util.invert_dictionary_lists(util.street_suffix_abbreviations))
    abbr_replacement = re.compile(r" (?P<abbr>{})\.?( |$)".format(abbreviations))
    abbr_lookup = util.invert_dictionary_lists(util.street_suffix_abbreviations)

    double_space = re.compile("  ")

    data = current_collection.find({})
    next_collection = util.go_to_next_stage()

    for entry in data:
        address = entry.get(util.address_field)
        original = address

        if not address:
            print("entry with missing '{}' field".format(util.address_field))
            next_collection.save(entry)
            continue

        result = directions.search(address)
        if result:
            address = address[:result.start()]

        while True:
            result = None
            result = abbr_replacement.search(address)
            if result:
                address_1 = address[:result.start()]
                address_2 = abbr_lookup[result.group('abbr')]
                address_3 = address[result.end():]

                address_1 += " "
                address_3 = " "+address_3 if address_3 != "" else ""

                address = address_1 + address_2 + address_3
            else:
                break

        result = double_space.search(address)
        if result:
            address = address[:result.start()]

        audit_street_type(street_types, address, original)

        entry[util.address_field] = address
        next_collection.save(entry)

    return street_types


def standardize_phone_numbers():
    current_collection = util.current_collection()
    data = current_collection.find()

    non_number = re.compile(r"\D+")
    non_number_start_end = re.compile(r"(^\D+)|(\D+$)")

    next_collection = util.go_to_next_stage()

    for entry in data:
        phone: str = entry.get(util.phone_field)

        if not phone:
            print("entry with missing '{}' field".format(util.phone_field_field))
            next_collection.save(entry)
            continue

        phone = re.sub(non_number_start_end, "", phone)
        phone = re.sub(non_number, "-", phone)
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
    district_dict = util.invert_dictionary_lists(util.districts)

    data = current_collection.find({})
    next_collection = util.go_to_next_stage()

    for entry in data:
        std_city = entry.get(util.city_field)
        if not std_city:
            print("entry with missing '{}' field".format(util.city_field))
            next_collection.save(entry)
            continue

        std_city = replace_dict.get(std_city, std_city)
        std_city = district_dict.get(std_city, std_city)

        entry[util.city_field] = std_city
        next_collection.save(entry)


def standardize_restaurant_types():
    current_collection = util.current_collection()

    data = current_collection.find()