def trip(arg_dict):
    ret = []
    add = []
    needed = ('id', 'bdate', 'total')
    for key, value in arg_dict.items():
        if key in needed:
            add.append(value)
    ret.append(tuple(add))
    return ret
