from src import util
from src import aggregate_mongodb
import py_stringmatching as sm
from py_stringmatching.similarity_measure.token_sort import TokenSort
from timeit import default_timer as timer


def test1():
    field_1 = util.phone_field
    field_2 = util.name_field
    data = [a for a in util.current_collection().find()]

    l = []
    s = TokenSort()
    for i in range(0,len(data)-1):
        i_total = timer()
        for j in range(i+1,len(data)-1):
            if data[i][field_1] == data[j][field_1]:
                d = {}
                for cu_fi in util.field_names:
                    d[cu_fi] = s.get_sim_score(str(data[i][cu_fi]), str(data[j][cu_fi]))
                l.append((data[i], data[j], d))
        if i % 50 == 0:
            print(i)
        print(timer()-i_total)

    l.sort(key=lambda x: int(x[0][util.id_field]))
    for e in l:
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
        print("{empty:4} {phone:05.2f}{empty:7} {name:05.2f}{empty:35} {address:05.2f}{empty:25} {city:05.2f}{empty:10} {type_f:05.2f}{empty:25}".format(
            empty="",
            phone=e[2][util.phone_field],
            name=e[2][util.name_field],
            address=e[2][util.address_field],
            city=e[2][util.city_field],
            type_f=e[2][util.type_field]
        ))
        print("{}|{}|{}|{}|{}|{}".format("=" * 4, "=" * 12, "=" * 40, "=" * 30, "=" * 15, "=" * 30))
    # l = sorted(l,key=lambda x: x[4])
    #
    # for e in l:
    #     print("{:11s}\t{:11s}\t{:4d}{:5d} |{:6.2f} {:6s}{:6s}".format(e[0],e[1],e[2],e[3],e[4],e[5]['id'],e[6]['id']))


def get_tokenized_data():
    data = util.current_collection().find({})
    an_tokenizer = sm.AlphanumericTokenizer()
    tokenized_data = []
    for entry in data:
        for field in util.field_names:
            entry[field] = an_tokenizer.tokenize(str(entry[field]))

        tokenized_data.append(entry)

    return tokenized_data

def get_corpus_list(tokenized_data, field):
    corpus_list = []
    for entry in tokenized_data:
        corpus_list.append(entry[field])

    return corpus_list
