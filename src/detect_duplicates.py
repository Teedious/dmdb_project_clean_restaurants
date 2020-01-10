from collections import defaultdict
from pprint import pprint

from src import util
from src import aggregate_mongodb
import py_stringmatching as sm
from timeit import default_timer as timer


possible_duplicates = {}


def audit_duplicates(collection_lane):
    tokenized_data = get_tokenized_data(list(util.current_collection(collection_lane).find({})))
    num_entries = len(tokenized_data)
    entry_comparisons = 4
    similarity_values = {}
    similarity_measures = {}
    measured_fields = [util.phone_field, util.address_field, util.name_field]

    for field in util.field_names:
        similarity_measures[field] = sm.SoftTfIdf(get_corpus_list(tokenized_data, field), threshold=0.9)

    for field in measured_fields:

        if field == util.phone_field:
            tokenized_data.sort(key=lambda x: "".join(x[field]))
        else:
            tokenized_data.sort(key=lambda x: "".join(sorted(x[field])))

        for i in range(0, num_entries):
            i_id = tokenized_data[i][util.id_field][0]
            if i_id not in similarity_values:
                similarity_values[i_id] = {}

            for j in range(i+1, min(i+1 + entry_comparisons, num_entries)):
                j_id = tokenized_data[j][util.id_field][0]
                if j_id not in similarity_values[i_id]:
                    similarity_values[i_id][j_id] = {}

                for field_to_check in measured_fields:
                    if field_to_check not in similarity_values[i_id][j_id]:
                        similarity_values[i_id][j_id][field_to_check] = similarity_measures[field_to_check].get_raw_score(
                            tokenized_data[i][field_to_check],
                            tokenized_data[j][field_to_check])
    return similarity_values


def get_duplicates(collection_lane,a, b, c):
    global possible_duplicates
    if collection_lane not in possible_duplicates:
        possible_duplicates[collection_lane] = audit_duplicates(collection_lane)
    duplicates = set()
    for key1 in possible_duplicates:
        for key2 in possible_duplicates[key1]:
            if possible_duplicates[key1][key2][util.phone_field] >= a \
                    and possible_duplicates[key1][key2][util.name_field] >= b \
                    and possible_duplicates[key1][key2][util.address_field] >= c:
                duplicates.add(tuple(sorted([int(key1), int(key2)])))
    return duplicates


def get_tokenized_data(data):
    an_tokenizer = sm.AlphanumericTokenizer()
    tokenized_data = []
    for entry in data:
        new_entry = {}
        for field in util.field_names:
            new_entry[field] = an_tokenizer.tokenize(str(entry[field]))

        tokenized_data.append(new_entry)

    return tokenized_data


def get_corpus_list(tokenized_data, field):
    corpus_list = []
    for entry in tokenized_data:
        corpus_list.append(entry[field])

    return corpus_list


def print_results(result_list):
    for e in result_list:
        print("{id:4} {phone:12} {name:40} {address:30} {city:15} {type_f:30}".format(
            id=e[0][util.id_field],
            phone=e[0][util.phone_field],
            name=e[0][util.name_field],
            address=e[0][util.address_field],
            city=e[0][util.city_field],
            type_f=str(e[0][util.type_field]),
        ))

        print("{id:4} {phone:12} {name:40} {address:30} {city:15} {type_f:30}".format(
            id=e[1][util.id_field],
            phone=e[1][util.phone_field],
            name=e[1][util.name_field],
            address=e[1][util.address_field],
            city=e[1][util.city_field],
            type_f=str(e[1][util.type_field])
        ))

        print("{} {} {} {} {} {}".format("-" * 4, "-" * 12, "-" * 40, "-" * 30, "-" * 15, "-" * 30))
        print(
            "{empty:4} {phone:05.2f}{empty:7} {name:05.2f}{empty:35} {address:05.2f}{empty:25} {city:05.2f}{empty:10} {type_f:05.2f}{empty:25}".format(
                empty="",
                phone=e[2][util.phone_field],
                name=e[2][util.name_field],
                address=e[2][util.address_field],
                city=e[2][util.city_field],
                type_f=e[2][util.type_field]
            ))
        print("{}|{}|{}|{}|{}|{}".format("=" * 4, "=" * 12, "=" * 40, "=" * 30, "=" * 15, "=" * 30))
