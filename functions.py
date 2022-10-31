from functools import reduce
from exceptions import TrigonometricError

change_sign_in_add = lambda add: list(map(lambda obj: neg(obj), add.objs)) # вызывается, когда знак выражения отрицательный. Возвращает противоположные элементы

simple_nod = lambda a, b: a if b == 0 else simple_nod(b, a % b)
nod = lambda *args: reduce(lambda x, y: simple_nod(x, y), args)

nok = lambda *args: reduce(lambda x, y: x * y // nod(x, y), args)

def neg(cont):
    cont.sign *= -1
    return cont


def one_in_other(obj, obj2):
    typ, typ2 = type(obj).__name__, type(obj2).__name__
    if typ != typ2:
        return {Integer(1)}

def get_muls(num, array=[]):
        if num == 1:
            return array
        for dl in range(2, num + 1):
            if num % dl == 0:
                return get_muls(num // dl, array + [str(dl)])

def in_decimal(obj):
    typ = type(obj).__name__
    if typ in ("sin", "cos", "tg", "ctg"):
        trig_values = [float(i) for i in open("txt/sinus_values.txt")]
        res = round(in_decimal(obj.cont))
        result = res % 360
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
            if result == 90:
                raise TrigonometricError(f"Не существует значения тангенса угла {res} градусов")
            return sign * trig_values[result] / trig_values[90 - result]
        if typ == "ctg":
            if result == 0:
                raise TrigonometricError(f"Не существует значения котангенса угла {res} градусов")
            return sign * trig_values[90 - result] / trig_values[result]

    diction = {"Integer": lambda obj: obj.num,
               "Pi": lambda obj: 3.14,
               "Exp": lambda obj: 2.72,
               "Mul": lambda obj: reduce(lambda el, el2: el * el2, [in_decimal(i) for i in obj.objs]),
               "Add": lambda obj: sum([in_decimal(i) for i in obj.objs]),
               "Fraction": lambda obj: in_decimal(obj.cont) / in_decimal(obj.cont2),
               "Pow": lambda obj: in_decimal(obj.cont)**in_decimal(obj.cont2),
               "Module": lambda obj: abs(in_decimal(obj.cont)),
               "Radical": lambda obj: in_decimal(obj.cont)**0.5}
    return obj.sign * diction.get(type(obj).__name__)(obj)

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

def eq(obj, obj2):
    diction = {"Integer": lambda x, y: x.num == y.num, "Pi": lambda x, y: x.num == y.num,
               "Exp": lambda x, y: x.num == y.num, "Variable": lambda x, y: x.variable == y.variable,
               "Integer": lambda x, y: x.num == y.num}
    if type(obj).__name == type(obj2).__name__ and obj.sign == obj2.sign:
        typ = type(obj).__name
        if typ in ["Pi", "Exp"]:
            return True
        if typ == "Integer":
            return obj.num == obj2.num
        if typ == "Mul":
            return set([to_st(i) for i in obj.objs]) == set([to_st(j) for j in obj2.objs])
        if typ in ["sin", "cos", "tg", "ctg", "arcsin", "arccos", "arctg", "arcctg", "lg", "ln"]:
            return eq(obj.cont, obj2.cont)
    return 

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