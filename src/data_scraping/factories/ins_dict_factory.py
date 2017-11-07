import hashlib


def trip(arg_dict):
    bdate = arg_dict['bdate']
    total = arg_dict['total']
    origin = arg_dict['origin']
    destination = arg_dict['destination']
    # Use SHA512 to try our best to make id unique
    s_id = "{}{}{}{}".format(bdate,total,origin,destination)
    id = hashlib.sha512(s_id.encode('utf-8')).hexdigest()
    ret = [id, bdate,total[3:],origin,destination]
    return ",".join(map(str,ret)) + '\n', [id]


def flight(arg_dict):
    arrive, depart = _package_aiports(arg_dict)
    flight_codes = arg_dict['flight_code']
    carriers = _get_carriers(flight_codes)
    dpt_time = arg_dict['depart_times']
    ret = ''
    ids = list()
    for i in range(len(arrive)):
        t = list()
        s_id = "{}{}{}{}{}".format(depart[i], arrive[i], carriers[i], flight_codes[i], dpt_time[i])
        id = hashlib.sha512(s_id.encode('utf-8')).hexdigest()
        t.extend([id, flight_codes[i], dpt_time[i], arrive[i], depart[i], carriers[i]])
        ret += ','.join(map(str, t)) + '\n'
        ids.append(id)
    return ret, ids

def _package_aiports(arg_dict):
    airports = arg_dict['airports']
    arrive = []
    depart = []
    for i in range(0, len(airports), 2):
        depart.append(airports[i])
        arrive.append(airports[i+1])
    return arrive, depart


def _get_carriers(codes):
    ret = []
    for code in codes:
        ret.append(code[:2])
    return ret
