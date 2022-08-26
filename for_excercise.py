a = "11827"






def main(st):
    array = list(st)
    return decode_expression(array)

issign = lambda ch: ch in "+-*/^"

convert_number = lambda number: {"object": "number", "value": number}

convert_const = lambda const: {"object": "const", "value": const}

convert_perem = lambda perem: {"object": "perem", "value": perem}

convert_func = lambda func, arg, osn=None: {"object": "func", "dcim": {"name": func, "arg": arg}} if func != "log" else {"object": "func", "dcim": {"name": func, "arg": arg, "osn": osn}}

convert_module = lambda args: {"object": "module", "objects": args}

convert_expression = lambda args: {"object": "expression", "objects": args}


def decode_expression(array):
    index, end = 0, len(array)
    object, signs = True, False
    pro_array = []
    if not array:
        raise Exception("Пусто")
#    if array[0] == "-":
#        array.insert(0, "0")
    while index != end:
        if object:
            while (index != end) or (not issign(array[index])):
                pass
        else:
            if array[index] not in "+/-*^":
                raise Exception("Ожидался")
            object, signs = True, False

    return {"object": "expression", "objects": pro_array}

def get_number(index, array):
    check_number = lambda number: (number.count(",") < 2) and ("" not in number.split(","))
    isdecimal = lambda x: x in "0123456789,"
    number = ""
    for elem in array[index:]:
        if isdecimal(array):
            number += elem
        else:
            break
    if not check_number(number):
        raise Exception
