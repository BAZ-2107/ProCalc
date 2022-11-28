# -*- coding: utf-8 -*-
from functools import reduce
from output import out
from exceptions import CalculateError, TrigonometricError, LogarithmicError
from functions import *
from math import log as logg, log10, log1p, sin as sinn, cos as coss, asin, acos, pi, degrees, radians, atan

class NumberExpression:
    def __init__(self, exp):
        self.exp = exp

    def run(self):
        out(f"Распознано как: <{to_st(self.exp)}>")
        out(f"Результат вычисления: <{self.in_decimal()}>")

    def in_decimal(self):
        return self.exp.in_decimal()


class AlphaExpression:
    def __init__(self, exp):
        self.exp = exp

    def run(self):
        out(f"Распознано как: <{to_st(self.exp)}>")
        out("Извините, решать буквенные выражения не умею (")


class Integer:
    sign = 1

    def __init__(self, num):
        self.num = num

    def update(self):
        return False, self

    def in_decimal(self):
        return self.num * self.sign

    def run(self):
        diction = {1: lambda num: "0 - это ничего" if num == 0
                   else "1 - основа натуральных чисел!" if num == 1
                   else f"множители числа <{num}> : {', '.join([str(1)] + get_muls(num))}",
                   -1: lambda num: "0 - это ничего" if num == 0
                   else "1 - основа целых чисел!" if num == 1
                   else f"множители числа <{num}> : {', '.join([str(-1)] + get_muls(num))}"}
        out(diction[self.sign](self.num))


class Pi(Integer):
    def run(self):
        out("""< π > равно < 3,14 >
Число < π > - математическая константа, равная отношению длины окружности к ее диаметру, которое приблизительно равно <3,14>
Используется для задания углов не в градусах, а в радианах. Например, 180° = π""")


class Exp(Pi):
    def run(self):
        out("""< e > равно < 2,72 >.
Число <e> (число Эйлера) - математическая константа, является базовым соотношением роста для всех непрерывно растущих процессов, которое приблизительно равно <2,72>
Используется в основании натурального логарифма ln""")


class Variable(Integer):
    def __init__(self, variable):
        self.variable = variable

    def run(self):
        out(f"{self.variable} - это переменная")


# КОНТЕЙНЕРЫ ДЛЯ ОПЕРАЦИЙ
class Module:
    sign = 1

    def __init__(self, cont):
        self.cont = cont

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * abs(self.cont.in_decimal())


class sin:
    sign = 1

    def __init__(self, cont):
        self.cont = cont

    def run(self):
        pass

    def in_decimal(self):
        k = lambda x: radians(x) if "π" not in to_st(self.cont) else x
        return round(sinn(k(self.cont.in_decimal())), 4)


class cos(sin):
    def in_decimal(self):
        k = lambda x: radians(x) if "π" not in to_st(self.cont) else x
        return round(coss(k(self.cont.in_decimal())), 4)


class tg(sin):
    def in_decimal(self):
        k = lambda x: radians(x) if "π" not in to_st(self.cont) else x
        s, c = sinn(k(self.cont.in_decimal())), coss(k(self.cont.in_decimal()))
        if round(c, 10) == 0:
            raise TrigonometricError("Значения тангенса данного угла не существует")
        return round(s / c, 4)
        
    
class ctg(sin):
    def in_decimal(self):
        k = lambda x: radians(x) if "π" not in to_st(self.cont) else x
        s, c = sinn(k(self.cont.in_decimal())), coss(k(self.cont.in_decimal()))
        if round(s, 10) == 0:
            raise TrigonometricError("Значения котангенса данного угла не существует")
        return round(c / s, 4)


class arcsin(sin):
    def in_decimal(self):
        res = self.cont.in_decimal()
        if abs(res) > 1:
            raise TrigonometricError("Аргумент арксинуса не должен превышать 1")
        return round(degrees(asin(res)), 4)
        
        
class arccos(sin):
    def in_decimal(self):
        res = self.cont.in_decimal()
        if abs(res) > 1:
            raise TrigonometricError("Аргумент арксинуса не должен превышать 1")
        return round(degrees(acos(res)), 4)


class arctg(sin):
    def in_decimal(self):
        return round(degrees(atan(self.cont.in_decimal())), 4)


class arcctg(sin):
    def in_decimal(self):
        res = round(degrees(atan(self.cont.in_decimal())), 4)
        if res >= 0:
            return 90 - res
        return -90 - res

class log:
    sign = 1

    def __init__(self, cont, cont2):
        self.cont, self.cont2 = cont, cont2

    def update(self):
        return False, self

    def in_decimal(self):
        base, arg = self.cont.in_decimal(), self.cont2.in_decimal()
        if base <= 0 or base == 1:
            raise LogarithmicError("Основание не может быть равным 1 или быть не больше  0")
        if arg <= 0:
            raise LogarithmicError("Аргумент логарифма не может быть не больше  0")
        return round(logg(arg, base), 4)

class lg(sin):
    def in_decimal(self):
        arg = self.cont.in_decimal()
        if arg <= 0:
            raise LogarithmicError("Аргумент логарифма не может быть не больше  0")
        return round(log10(arg), 4)


class ln(sin):
    def in_decimal(self):
        arg = self.cont.in_decimal()
        if arg <= 0:
            raise LogarithmicError("Аргумент логарифма не может быть не больше  0")
        return round(log1p(arg), 4)


class Add:
    sign = 1

    def __init__(self, *objs):
        self.objs = list(objs)

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * sum(elem.in_decimal() for elem in self.objs)

    def update(self):
        """
        st = to_st(self)
        if self.sign == -1:
            self.sign, self.objs = 1, change_sign_in_add(self)
            out(f"{st} <=> {to_st(self)}")
            return True, self
        # на этом моменте среди слагаемых будут только Mul, Fraction, Pow, Radical, Module, sin, cos, tg, ctg, arcsin, arccos, arctg, arcctg, log, lg, ln, Variable, Pi, Exp, Integer
        """
        for i, value in enumerate(self.objs):
            result, elem = value.update()
            while result:
                st1 = to_st(self)
                self.objs[i] = elem
                st2 = to_st(self)
                out(f"{st1} <=> {st2}")
                result, elem = elem.update()

        #types = reduce(lambda x, y: x & y, list(map(lambda el: get_types(el), self.objs)))
        #if types:
            #return False, types
        return False, self

    def two_adds(self):
        obj, obj2 = self.objs
        typ, typ2 = type(obj).__name__, type(obj2).__name__
        if typ == typ2:
            if typ == "Integer": # складываются 2 числа между собой
                res = obj.sign * obj.num + obj2.sign * obj2.num
                if res < 0:
                    return Integer(abs(res), sign=-1)
                return Integer(res)
            if typ == "variable":
                if obj.variable == obj2.variable:
                    pass


    def add_numbers(self):
        obj = sum(elem() for elem in self.objs)
        if obj < 0:
            return True, neg(Integer(abs(obj)))
        return True, Integer(obj)        


class Mul:
    sign = 1

    def __init__(self, *objs):
        self.objs = list(objs)

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * reduce(lambda x, y: x * y, [elem.in_decimal() for elem in self.objs])

    def update(self):
        return False, self


class Fraction:
    sign = 1

    def __init__(self, cont, cont2):
        self.cont, self.cont2 = cont, cont2
        if type(cont2).__name__ != "AlphaExpression" and cont2.in_decimal() == 0:
            raise CalculateError(f"<{to_st(cont2)}> == 0, делить на ноль нельзя")

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * self.cont.in_decimal() / self.cont2.in_decimal()

    def update(self):
        

        #types = reduce(lambda x, y: get_all_types(x) | get_all_types(y), self.objs)        
        return False, self


class Radical:
    sign = 1

    def __init__(self, cont):
        answer, cont2 = cont.update()
        typ, value = type(cont2).__name__, cont2
        if typ in ["Pi", "Exp", "Integer"] and value.sign == -1:
            raise CalculateError(f"Выражение <{str(cont)}> не может быть отрицательным")
        self.cont = cont

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * self.cont.in_decimal()**0.5

    def update(self):
        typ, value = type(self.cont).__name__, self.cont

        if typ == "Integer":
            num = value.num
            result = num**0.5
            if not result % 1:
                return True, Integer(int(result))
        return False, self


class Pow:
    sign = 1

    def __init__(self, cont, cont2):
        self.cont, self.cont2 = cont, cont2

    def run(self):
        pass

    def in_decimal(self):
        return self.sign * self.cont.in_decimal()**self.cont2.in_decimal()

    def update(self):
        return False, self


diction = {"sin": lambda ex: sin(ex), "cos": lambda ex: cos(ex), "tg": lambda ex: tg(ex),
           "ctg": lambda ex:
ctg(ex), "arcsin": lambda ex: arcsin(ex),
           "arccos": lambda ex: arccos(ex), "arctg": lambda ex: arctg(ex),
           "arcctg": lambda ex: arcctg(ex), "lg": lambda ex: lg(ex),
           "ln": lambda ex: ln(ex), "log": lambda ex, ex_1: log(ex, ex_1)}


nod = lambda a, b: a if b == 0 else nod(b, a % b)