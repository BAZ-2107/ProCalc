# -*- coding: utf-8 -*-
from functools import reduce


alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
converting_to_decimal_int = lambda a, ss: sum(alpha.index(a[-i-1])*ss**i for i in range(len(a)))
converting_to_decimal_float = lambda a, ss: sum(alpha.index(a[i])*ss**(-i-1) for i in range(len(a)))


def converting_one_in_other(one, ss1, ss2):
    global alpha
    if any(alpha[ss1] <= i for i in one):
        raise Exception
    st, st2 = "", ""
    n, mod = (converting_to_decimal_int(one, ss1), None) if "," not in one else (converting_to_decimal_int(one.split(",")[0], ss1), converting_to_decimal_float(one.split(",")[-1], ss1))
    while n:
        st += alpha[n % ss2]
        n //= ss2
    if mod:
        st = "," + st
        k, st2 = 0, ""
        while not (k == 6 or (mod % 1) == 0):
            mod *= ss2
            st2 += alpha[int(mod // 1)]
            mod %= 1
            k += 1
    return f"{st[::-1]}{st2}"


change_sign_in_add = lambda add: list(map(lambda obj: neg(obj), add.objs)) # вызывается, когда знак выражения отрицательный. Возвращает противоположные элементы
simple_nod = lambda a, b: a if b == 0 else simple_nod(b, a % b)
nod = lambda *args: reduce(lambda x, y: simple_nod(x, y), args)
nok = lambda *args: reduce(lambda x, y: x * y // nod(x, y), args)


def neg(cont):
    cont.sign *= -1
    return cont

def decode_expression(arg):
    from DecodeExpression import Decode
    return Decode().decode(arg.replace(" ", ""))
    

def one_in_other(obj, obj2):
    typ, typ2 = type(obj).__name__, type(obj2).__name__
    if typ != typ2:
        return {Integer(1)}

def get_muls(num, array=[]):
        if num == 1:
            return array
        for dl in [int(i) for i in open("txt/simple_numbers.txt")]:
            if num % dl == 0:
                return get_muls(num // dl, array + [str(dl)])        
        for dl in range(99991, num // 2 + 1):
            if num % dl == 0:
                return get_muls(num // dl, array + [str(dl)])
        return get_muls(num // num, array + [str(num)])

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
    if typ == "NumberExpression":
        return to_st(obj.exp)      
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
