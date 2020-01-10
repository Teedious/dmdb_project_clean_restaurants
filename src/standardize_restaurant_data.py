import pprint
import re
from collections import defaultdict
from src import util
import requests
from urllib.parse import urlencode


def audit_street_type(street_types, street_name: str, original):
    expected = util.street_suffix_abbreviations.keys()

    street_words = street_name.split(" ")
    if len(street_words) > 0:
        street_type = street_words[-1]
        if street_type not in expected and len(street_words) > 1:
            street_type = street_words[-2]
            if street_type not in expected:
                street_types[street_type].add((street_name, original))


def standardize_addresses(collection_lane):
    current_collection = util.current_collection(collection_lane)
    data = [a for a in current_collection.find({})]
    next_collection = util.go_to_next_stage(collection_lane)
    new_data = list()

    street_types = defaultdict(set)

    directions = re.compile(r"( (at|near|between|off|in) )")

    written_numbers = {"first": "1st",
                       "second": "2nd",
                       "third": "3rd",
                       "fourth": "4th",
                       "fifth": "5th",
                       "sixth": "6th",
                       "seventh": "7th",
                       "eighth": "8th",
                       "ninth": "9th",
                       "tenth": "10th",
                       "eleventh": "11th",
                       "twelfth": "12th"}

    written_num_re = re.compile(r"(?P<num>{})".format("|".join(written_numbers.keys())))
    abbreviations = "|".join(util.invert_dictionary_lists(util.street_suffix_abbreviations))
    abbr_replacement = re.compile(r" (?P<abbr>{})\.?( |$)".format(abbreviations))
    abbr_lookup = util.invert_dictionary_lists(util.street_suffix_abbreviations)

    double_space = re.compile("  ")

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

        replacements = [abbr_replacement, written_num_re]
        results = abbr_replacement.finditer(address)
        for result in results:
            address_1 = address[:result.start()]
            address_2 = abbr_lookup[result.group('abbr')]
            address_3 = address[result.end():]

            address_1 = address_1.strip() + " "
            address_3 = " " + address_3 if address_3 != "" else ""

            address = address_1 + address_2 + address_3

        results = written_num_re.finditer(address)
        for result in results:
            address_1 = address[:result.start()]
            address_2 = written_numbers[result.group('num')]
            address_3 = address[result.end():]

            address = address_1 + address_2 + address_3

        result = double_space.search(address)
        if result:
            address = address[:result.start()]

        address = address.strip()

        audit_street_type(street_types, address, original)

        entry[util.address_field] = address
        new_data.append(entry)
    next_collection.insert_many(new_data)
    pprint.pprint(util.current_collection().find_one({util.id_field: "714"}))

    not_expected_count = sum(map(lambda x: len(street_types[x]), street_types))
    total_count = len(data)
    ratio_not_expected = not_expected_count / total_count * 100
    ratio_expected = 100 - ratio_not_expected
    print("Not expected:       {}/{}".format(not_expected_count, total_count))
    print("Ratio not expected: {:5.1f}%".format(ratio_not_expected))
    print("Ratio expected:     {:5.1f}%".format(ratio_expected))
    return street_types


def standardize_phone_numbers(collection_lane):
    current_collection = util.current_collection(collection_lane)
    data = current_collection.find({})
    next_collection = util.go_to_next_stage(collection_lane)
    new_data = list()
    non_number = re.compile(r"\D+")
    non_number_start_end = re.compile(r"(^\D+)|(\D+$)")

    for entry in data:
        phone: str = entry.get(util.phone_field)

        if not phone:
            print("entry with missing '{}' field".format(util.phone_field_field))
            next_collection.save(entry)
            continue

        phone = re.sub(non_number_start_end, "", phone)
        phone = re.sub(non_number, "-", phone)
        entry[util.phone_field] = phone

        new_data.append(entry)
    next_collection.insert_many(new_data)


def standardize_cities(collection_lane):
    current_collection = util.current_collection(collection_lane)
    data = current_collection.find({})
    next_collection = util.go_to_next_stage(collection_lane)
    new_data = list()

    replace_dict = {
        'la': 'los angeles',
        'west la': 'los angeles',
        'w. hollywood': 'west hollywood',
        'new york': 'new york city',
        'st. boyle hts.': 'boyle heights',
    }
    district_dict = util.invert_dictionary_lists(util.districts)

    for entry in data:
        std_city = entry.get(util.city_field)
        if not std_city:
            print("entry with missing '{}' field".format(util.city_field))
            next_collection.save(entry)
            continue

        std_city = replace_dict.get(std_city, std_city)
        std_city = district_dict.get(std_city, std_city)

        entry[util.city_field] = std_city
        new_data.append(entry)
    next_collection.insert_many(new_data)


def standardize_restaurant_types(collection_lane):
    current_collection = util.current_collection(collection_lane)
    data = current_collection.find({})
    next_collection = util.go_to_next_stage(collection_lane)
    new_data = list()

    containing_numbers = re.compile(r" \d.*\d ")
    split_points = re.compile(r"(?: and |/)")

    replace_dict = {"bbq": "barbecue"}

    for entry in data:
        type_content = entry[util.type_field]

        result = containing_numbers.search(type_content)
        if result:
            type_content = type_content[containing_numbers.search(type_content).end():]

        type_content = split_points.split(type_content)

        for i, content in enumerate(type_content):
            type_content[i] = replace_dict.get(content, content)

        entry[util.type_field] = type_content
        new_data.append(entry)
    next_collection.insert_many(new_data)