from functools import reduce

change_sign_if_neg = lambda add: list(map(lambda obj: neg(obj), add.objs)) # вызывается, когда знак выражения отрицательный. Возвращает противоположные элементы
    

def neg(cont):
    cont.sign *= -1
    return cont

def get_all_types(obj):
    typ, types = type(obj).__name__, set()
    if typ in ["Integer", "Pi", "Exp", "Variable"]:
        return {typ}
    types |= {typ}
    if typ in ("Mul", "Add"):
        types |= reduce(lambda x, y: x | y, [get_all_types(elem) for elem in obj.objs])
    elif typ in ("Fraction", "Pow", "log"):
        types |= get_all_types(obj.cont)
        types |= get_all_types(obj.cont2)
    else:
        types |= get_all_types(obj.cont)
    return types

def in_decimal(obj):
    typ = type(obj).__name__
    if typ in ("sin", "cos", "tg", "ctg"):
        trig_values = [float(i) for i in open("txt/sinus_values.txt")]
        result = round(in_decimal(obj.cont)) % 360
        sign = 1
        if 90 < result <= 180:
            result = 180 - result
            if typ != "sin":
                sign = -1
        elif 180 < result <= 270:
            result -= 180
            if typ in ("sin", "cos"):
                sign = -1
        elif 270 < result < 360:
            result = 360 - result
            if typ != "cos":
                sign = -1

        if typ == "sin":
            return sign * trig_values[result]
        if typ == "cos":
            return sign * trig_values[90 - result]
        if typ == "tg":
            return sign * trig_values[result] / trig_values[90 - result]
        if typ == "ctg":
            return sign * trig_values[90 - result] /  trig_values[result]

    diction = {"Integer": lambda obj: obj.sign * obj.num,
               "Pi": lambda obj: obj.sign * 3.14,
               "Exp": lambda obj: obj.sign * 2.72,
               "Mul": lambda obj: reduce(lambda el, el2: el * el2, [in_decimal(i) for i in obj.objs]),
               "Add": lambda obj: sum([in_decimal(i) for i in obj.objs]),
               "Fraction": lambda obj: in_decimal(obj.cont) / in_decimal(obj.cont2),
               "Pow": lambda obj: in_decimal(obj.cont)**in_decimal(obj.cont2),
               "Module": lambda obj: abs(in_decimal(obj.cont)),
               "Radical": lambda obj: in_decimal(obj.cont)**0.5}
    return diction.get(type(obj).__name__)(obj)

def add__in_objs(objs): # вызывается, когда среди слагаемых есть объект Add. Рекурсивно возвращает объект, у которого нет среди слагаемых Add
    if not "Add" in [type(elem).__name__ for elem in objs]:
        return objs
    for i, elem in enumerate(objs):
        if type(elem).__name__ == "Add":
            del objs[i]
            array = [neg(j) for j in elem.objs] if elem.sign == -1 else elem.objs
            objs = objs[:i] + array + objs[i:]
            return add__in_objs(objs)

def sort_elems_and_return_answer(elems):
    for_sort = lambda arg: ["Mul", "Fraction", "Pow", "Radical", "Module", "sin", "cos",
            "tg", "ctg", "arcsin", "arccos", "arctg", "arcctg", "log", "lg",
            "ln", "Variable", "Pi", "Exp", "Integer"].index(type(arg).__name__)
    return sorted(elems, key=for_sort)

def to_st(obj):
    typ = type(obj).__name__
    sign = "" if obj.sign == 1 else "-"
    
    if typ == "Integer":
        return sign + str(obj.num)
    if typ == "Pi":
        return sign + "π"
    if typ == "Exp":
        return sign + "e"
    if typ == "Variable":
        return sign + obj.variable
    if typ == "Add":
        st = to_st(obj.objs[0]) + "".join(f"+{to_st(elem)}" if elem.sign == 1 else to_st(elem) for elem in obj.objs[1:])
        if not sign:
            return st
        return sign + f"({st})"
    if typ == "Mul":
        return sign + "*".join(f"({to_st(elem)})" if (type(elem).__name__ == "Add" or elem.sign == -1) else to_st(elem) for elem in obj.objs)
    if typ == "Fraction":
        return sign + "/".join(f"({to_st(elem)})" if (type(elem).__name__ in ["Add", "Mul", "Fraction"] or elem.sign == -1) else to_st(elem) for elem in (obj.cont, obj.cont2))
    if typ == "Radical":
        return sign + "√" + str(f"({to_st(obj.cont)})" if (obj.cont.sign == -1) or (type(obj.cont).__name__ not in ("Integer", "Variable", "Pi", "Exp")) else to_st(obj.cont))
    if typ == "Pow":
        return sign + "^".join(f"({to_st(elem)})" if (type(elem).__name__ not in ["Integer", "Variable", "Exp", "Pi"] or elem.sign == -1) else to_st(elem) for elem in (obj.cont, obj.cont2))
    if typ == "Module":
        return sign + f"|{to_st(obj.cont)}|"
    if typ == "log":
        return sign + typ + f"({to_st(obj.cont)})({to_st(obj.cont2)})"
    if typ in ["sin", "cos", "tg", "ctg", "arcsin", "arccos", "arctg", "arcctg",
            "lg", "ln"]:
        return sign + typ + f"({to_st(obj.cont)})"
