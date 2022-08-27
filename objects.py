# -*- coding: utf-8 -*-

# вспомогательные классы для сокращения кода
class Str:
    st = ""

    def __str__(self):
        return self.st


# Классы, которые объявляются при кодировке
class Natural(Str):
    def __init__(self, number):
        self.number = number
        self.st = str(number)


class Rational(Natural):
    def __init__(self, num, denom):
        self.num, self.denom = num, denom
        self.st = f"{str(num)}/{str(denom)}"      


class Const(Str):
    def __init__(self, ch):
        self.ch, self.st = ch, ch


class Perem(Const):
    pass


class Add(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}+{str(arg2)})"


class Sub(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}-{str(arg2)})"


class Mul(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}*{str(arg2)})"


class Div(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)}/{str(arg2)})"


class Pow(Str):
    def __init__(self, arg, arg2):
        self.arg, self.arg2 = arg, arg2
        self.st = f"({str(arg)})^({str(arg2)})"


class Radical(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"√{str(arg)}"


class Module(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"|{str(arg)}|"


class Invers(Str):
    def __init__(self, arg):
        self.arg = arg
        self.st = f"(-{str(self.arg)})"


class sin(Str):
    def __init__(self, arg):
        name, self.arg = "sin", arg
        self.st = f"{name}({str(arg)})"


class cos(Str):
    def __init__(self, arg):
        name, self.arg = "cos", arg
        self.st = f"{name}({str(arg)})"


class tg(Str):
    def __init__(self, arg):
        name, self.arg = "tg", arg
        self.st = f"{name}({str(arg)})"
        
    
class ctg(Str):
    def __init__(self, arg):
        name, self.arg = "ctg", arg
        self.st = f"{name}({str(arg)})"


class arcsin(Str):
    def __init__(self, arg):
        name, self.arg = "arcsin", arg
        self.st = f"{name}({str(arg)})"
        
        
class arccos(Str):
    def __init__(self, arg):
        name, self.arg = "arccos", arg
        self.st = f"{name}({str(arg)})"


class arctg(Str):
    def __init__(self, arg):
        name, self.arg = "arctg", arg
        self.st = f"{name}({str(arg)})"


class arcctg(Str):
    def __init__(self, arg):
        name, self.arg = "arcctg", arg
        self.st = f"{name}({str(arg)})"

class log(Str):
    def __init__(self, osn, arg):
        name, self.osn, self.arg = "log", osn, arg
        self.st = f"{name}({str(osn)})({str(arg)})"


class lg(Str):
    def __init__(self, arg):
        name, self.arg = "lg", arg
        self.st = f"{name}({str(arg)})"


class ln(Str):
    def __init__(self, arg):
        name, self.arg = "ln", arg
        self.st = f"{name}({str(arg)})"


# классы, объекты которых появляются при взаимодействии объектов кодировки
class Integer(Natural, Str):
    def __init__(self, number):
        super().__init__(number)
        if number != 0:
            self.st = f"({number})"
        else:
            self.st = "0"


class Irrational(Str):
    def __init__(self, number, pow):
        if in_decimal(pow) == 0.5:
            self.st = f"√({str(number)})"
        else:
            self.st = f"({str(number)})^({str(pow)})"
        self.number, self.pow = number, pow


diction = {"sin": lambda ex: sin(ex), "cos": lambda ex: cos(ex), "tg": lambda ex: tg(ex),
           "ctg": lambda ex: ctg(ex), "arcsin": lambda ex: arcsin(ex),
           "arccos": lambda ex: arccos(ex), "arctg": lambda ex: arctg(ex),
           "arcctg": lambda ex: arcctg(ex), "lg": lambda ex: lg(ex),
           "ln": lambda ex: ln(ex), "log": lambda ex, ex_1: log(ex, ex_1)}

#a = from_decimal_to_rational("5,5")
#print(a)
