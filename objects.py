# -*- coding: utf-8 -*-

# вспомогательные классы для сокращения кода
class Str:
    st = ""

    def __str__(self):
        return self.st

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
    pass

def sub(arg, arg2):
    pass

def mul(arg, arg2):
    pass

def div(arg, arg2):
    pass

def module(arg):
    pass

def radical(arg):
    pass

def pow(arg, arg2):
    pass

def invers(arg):
    pass


# Классы, которые объявляются при кодировке
class Natural(Str):
    def __init__(self, number):
        self.number = number
        self.st = str(number)

    def run(self):
        return self


class Rational(Natural):
    def __init__(self, num, denom):
        self.num, self.denom = num, denom
        self.st = f"{str(num)}/{str(denom)}"


class Const(Str):
    def __init__(self, ch):
        self.ch, self.st = ch, ch

    def run(self):
        return self


class Perem(Const):
    pass


class Add(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}+{str(arg2)})"

    def run(self):
        return add(self.arg.run(), self.arg2.run())


class Sub(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}-{str(arg2)})"

    def run(self):
        return sub(self.arg.run(), self.arg2.run())


class Mul(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}*{str(arg2)})"

    def run(self):
        return mul(self.arg.run(), self.arg2.run())


class Div(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}/{str(arg2)})"

    def run(self):
        return div(self.arg.run(), self.arg2.run())


class Pow(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)})^({str(arg2)})"

    def run(self):
        return pow(self.arg.run(), self.arg2.run())


class Radical(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"√{str(arg)}"
        
    def run(self):
        return radical(self.arg.run())


class Module(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"|{str(arg)}|"

    def run(self):
        return module(self.arg.run())


class Invers(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"(-{str(self.arg)})"

    def run(self):
        return invers(self.arg.run())


class sin(Str):
    def __init__(self, arg):
        name, self.arg = "sin", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class cos(Str):
    def __init__(self, arg):
        name, self.arg = "cos", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
            return self


class tg(Str):
    def __init__(self, arg):
        name, self.arg = "tg", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self
        
    
class ctg(Str):
    def __init__(self, arg):
        name, self.arg = "ctg", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class arcsin(Str):
    def __init__(self, arg):
        name, self.arg = "arcsin", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self
        
        
class arccos(Str):
    def __init__(self, arg):
        name, self.arg = "arccos", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class arctg(Str):
    def __init__(self, arg):
        name, self.arg = "arctg", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class arcctg(Str):
    def __init__(self, arg):
        name, self.arg = "arcctg", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class log(Str):
    def __init__(self, osn, arg):
        name, self.osn, self.arg = "log", osn, arg
        self.st = f"{name}({str(osn)})({str(arg)})"

    def run(self):
        return self


class lg(Str):
    def __init__(self, arg):
        name, self.arg = "lg", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self


class ln(Str):
    def __init__(self, arg):
        name, self.arg = "ln", arg
        self.st = f"{name}({str(arg)})"

    def run(self):
        return self

# классы, объекты которых появляются при взаимодействии объектов кодировки
class Integer(Natural, Str):
    def __init__(self, number):
        super().__init__(number)
        if number != 0:
            self.st = f"({number})"


class Irrational(Str):
    def __init__(self, number, pow):
        if in_decimal(pow) == 0.5:
            self.st = f"√({str(number)})"
        else:
            self.st = f"({str(number)})^({str(pow)})"
        self.number, self.pow = number, pow


diction = {"sin": lambda ex: sin(ex), "cos": lambda ex: cos(ex), "tg": lambda ex: tg(ex), "ctg": lambda ex: ctg(ex), "arcsin": lambda ex: arcsin(ex), "arccos": lambda ex: arccos(ex), "arctg": lambda ex: arctg(ex), "arcctg": lambda ex: arcctg(ex), "lg": lambda ex: lg(ex), "ln": lambda ex: ln(ex), "log": lambda ex, ex_1: log(ex, ex_1)}

#a = from_decimal_to_rational("5,5")
#print(a)
