from src import util
from src import aggregate_mongodb


def test1():
    field_1 = util.phone_field
    field_2 = util.name_field
    data = sorted([a for a in util.current_collection().find()],key=lambda x:x[util.phone_field])

    l = []
    for i in range(0, len(data) - 1):
        d = qgram_distance(4, data[i][field_1], data[i + 1][field_1])[4]
        if d >= 0.:
            d = {}
            for cu_fi in util.field_names:
                d[cu_fi] = qgram_distance(4, data[i][cu_fi], data[i + 1][cu_fi])[4]
            l.append((data[i], data[i + 1], d))

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


def get_padding_char(a, b):
    for i in range(9633, 1114111):
        i = chr(i)
        if (i not in a) and (i not in b):
            return i


def qgram_distance(gram_size, a, b):
    a = str(a)
    b = str(b)
    padding_char = get_padding_char(a, b)

    if gram_size > len(a) or gram_size > len(b):
        a = a + padding_char * max(gram_size - len(a), 0)
        b = b + padding_char * max(gram_size - len(b), 0)

    if len(a) != len(b):
        a = a + padding_char * max(len(b) - len(a), 0)
        b = b + padding_char * max(len(a) - len(b), 0)

    grams_a = {}
    grams_b = {}
    for i in range(0, len(a) - gram_size + 1):
        gram_a = a[i:i + gram_size]
        gram_b = b[i:i + gram_size]

        grams_a[gram_a] = grams_a.get(gram_a, 0) + 1
        grams_b[gram_b] = grams_b.get(gram_b, 0) + 1

    distance = 0
    sum = 0
    for key in set(list(grams_a.keys()) + list(grams_b.keys())):
        sum += grams_b.get(key, 0) + grams_a.get(key, 0)
        distance += abs(grams_b.get(key, 0) - grams_a.get(key, 0))

    return (a, b, distance, sum, 1 - distance / sum, distance/sum)
