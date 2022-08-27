# -*- coding: utf-8 -*-
from objects import *

# основная функция
def run(ex):
    
    if type(ex) in [Natural, Integer, Rational, Const, Perem, Irrational]:
        return ex
    elif type(ex) in [Sub, Add, Mul, Div, Pow]:
        diction = {Add: lambda x, y: add(x, y), Sub: lambda x, y: sub(x, y),
                   Mul: lambda x, y: mul(x, y), Div: lambda x, y: div(x, y), Pow: lambda x, y: pow(x, y)}
        return diction[type(ex)](run(ex.arg), run(ex.arg2))
    elif type(ex) in [Radical, Invers, Module]:
        diction = {Radical: lambda x: radical(x), Module: lambda x: module(x),
                   Invers: lambda x: invers(x)}
        return diction[type(ex)](run(ex.arg))
    elif type(ex) in [sin, cos, tg, ctg, arcsin, arccos, arctg, arcctg, ln, lg]:
        ex.arg = run(ex.arg)
        return ex
    elif type(ex) == log:
        ex.osn, ex.arg = run(ex.osn), run(ex.arg)
        return ex
    return "Пока таких объектов не распознаю"


# вспомогательные функции
def in_decimal(number):
    if type(number) in [Natural, Integer]:
        return number.number
    elif type(number) == Rational:
        return in_decimal(number.num) / in_decimal(number.denom)
    elif type(number) == Irrational:
        return in_decimal(number.number) / in_decimal(number.pow)
    elif type(number) == Const:
        if number.ch == "π":
            return 3.14
        elif number.ch == "e":
            return 2.72

def get_muls(number, array=[]):
        if number == 1:
            return array
        k = 2
        while (number % k) != 0:
            k += 1
        return get_muls(number // k, array + [k])

def nod(a, b):
    if b == 0:
        return a
    return nod(b, a % b)

def to_power(number):
    on_muls = get_muls(number)
    if not on_muls:
        return (1, 1)
    muls = list(set(on_muls))
    if len(muls) == 1:
        return (muls.pop(), len(on_muls))
    array= list(map(lambda x: on_muls.count(x), muls))
    pow = reduce(lambda x, y: nod(x, y), array)
    return (reduce(lambda x, y: x * y, [muls[i]**(array[i]//pow) for i in range(len(array))]), pow)

def from_decimal_to_rational(st):
    num, denom = int(st.replace(",", "")), 10**len(st.split(",")[-1])
    dl = nod(num, denom)
    return num // dl, denom // dl

# функции, выполняющие операции с объектами
def add(arg, arg2):
    if type(arg) == type(arg2) == Natural:
        return Natural(arg.number + arg2.number)

def sub(arg, arg2):
    pass

def mul(arg, arg2):
    pass

def div(arg, arg2):
    pass

def module(arg):
    if type(arg) in [Natural, Const, Perem]:
        return arg
    elif type(arg) == Integer:
        return Natural(-arg.number)

def radical(arg):
    pass

def pow(arg, arg2):
    pass

def invers(arg):
    if type(arg) in [Natural, Const, Perem]:
        return arg