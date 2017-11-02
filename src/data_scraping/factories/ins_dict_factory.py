import hashlib
import datetime

def trip(arg_dict):
    ret = []
    bdate = arg_dict['bdate']
    total = arg_dict['total']
    origin = arg_dict['origin']
    destination = arg_dict['destination']
    # Use SHA512 to try our best to make id unique
    # add time for extra uniqueness in hash
    s_id = "{}{}{}{}{}".format(bdate,total,origin,destination,datetime.datetime.now())
    id = hashlib.sha512(s_id.encode('utf-8')).hexdigest()
    ret.extend([id, bdate,float(total[3:]), origin, destination])
    return [tuple(ret)]


def flight(arg_dict):
    arrive, depart = _package_aiports(arg_dict)
    flight_codes = arg_dict['flight_code']
    carriers = _get_carriers(flight_codes)
    dpt_time = arg_dict['depart_times']
    ret = []
    for i in range(len(arrive)):
        s_id = "{}{}{}{}{}{}".format(depart[i], arrive[i], carriers[i], flight_codes[i], dpt_time[i],
                                     datetime.datetime.now())
        id = hashlib.sha512(s_id.encode('utf-8')).hexdigest()
        ret.append((id, flight_codes[i], dpt_time[i], arrive[i], depart[i], carriers[i]))
    return ret

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
