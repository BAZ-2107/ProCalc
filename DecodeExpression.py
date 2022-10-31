from exceptions import DecodeError
from functions import to_st
from objects import *

class Decode:
    info = {"numbers": {}, "consts": {}, "variables": {}, "funcs": {}, "Modules": {},
            "Pows": {}, "Adds": {}, "Muls": {}, "Radicals": {}, "Fractions": {}}

    f = open("txt/functions.txt", "r")
    functions = f.read().split()
    f.close()
    

    def decode(self, st):
        array = list(st)
        if ("(" in array) or (")" in array):
            self.check_brackets(array)
        elem = self.decode_expression(array)
        return self.info, elem

    def decode_expression(self, array):
        while "(" in array:
            stop = array.index(")")
            start = stop
            while array[start] != "(":
                start -= 1
            in_brackets = array[start + 1: stop]
            del array[start:stop+1]
            if in_brackets:
                if "|" in in_brackets:
                    in_brackets = self.decode_module(in_brackets)
                in_brackets = self.decode_and_check(in_brackets)
                array.insert(start, in_brackets)
        if "|" in array:
            array = self.decode_module(array)
        result = self.decode_and_check(array)
        return result

    def decode_and_check(self, array):
        array = self.convert_numbers(array)
        array = self.convert_functions(array)
        array = self.convert_constants(array)
        array = self.convert_variables(array)
        array = self.convert_st_f_r_i(array)
        array = self.convert_m_d_a_s(array)
        return array[0]

    def decode_module(self, array):
        issign = lambda x: x in list("+-*/^√[")
        ismodulebracket = lambda x: x == "|"
        k = 0
        for i, ch in enumerate(array):
            if ismodulebracket(ch):
                if (k == 0) or (i != 0 and issign(array[i - 1])):
                    array[i], k = "[", k + 1
                else:
                    array[i], k = "]", k - 1
        if k != 0:
            raise DecodeError("Не удалось расшифровать модуль в выражении")
        while "[" in array:
            stop = array.index("]")
            start = stop
            while array[start] != "[":
                start -= 1
            in_module = array[start + 1: stop]
            del array[start:stop+1]
            in_module = self.decode_and_check(in_module)
            result = Module(in_module)
            self.info["Modules"][to_st(result)] = result
            array.insert(start, result)
        return array

# проверка скобок выражений
    def check_brackets(self, array):
        isleftbracket = lambda x: x == "("
        isrightbracket = lambda x: x == ")"
        k = 0
        for ch in array:
            if isleftbracket(ch):
                k += 1
            if isrightbracket(ch):
                k -= 1
            if k == -1:
                raise DecodeError("Некорректное число скобок")
        if k != 0:
            raise DecodeError("Некорректное число скобок")

    # метод конвертировки цифр в числа
    def convert_numbers(self, array):
        isnumber = lambda ch: ch in list("0123456789,")
        iscorrectnumber = lambda number: (number.count(",") < 2) and ("" not in number.split(","))            
        start, step, end = 0, 0, len(array)
        while start <= end:
            if start != end and isnumber(array[start]):
                step += 1
            elif step:
                stop = start
                start -= step
                number = "".join(array[start:stop])
                if not iscorrectnumber(number):
                    raise DecodeError(f"Неправильная запись числа: <{str(num)}>")
                del array[start:stop]
                if "," not in number:
                    result = Integer(int(number))
                    self.info["numbers"][to_st(result)] = result
                    array.insert(start, result)
                else:
                    num, denom = int(number.replace(",", "")), int(10**len(number.split(",")[-1]))
                    result = Fraction(Integer(num), Integer(denom))
                    self.info["numbers"][to_st(result)] = result
                    self.info["Fractions"][to_st(result)] = result
                    array.insert(start, result)
                step, end = 0, len(array)
            start += 1
        return array

    # функция конвертировки букв в названия функций
    def convert_functions(self, array):
        start, end  = 0, len(array)
        while start != end:
            if (type(array[start]) == str) and (array[start].isalpha()):
                for func in self.functions:
                    stop = start + len(func)
                    if (stop <= end) and (array[start:stop] == list(func)):
                        del array[start:stop]
                        array.insert(start, func)
                        end = len(array)
                        break
            start += 1
        if array[-1] in self.functions:
            raise DecodeError(f"У функции <{array[-1]}> не найден агумент")
        return array

    def convert_constants(self, array):
        diction = {"e": Exp("e"), "π": Pi("π")}
        for i, elem in enumerate(array):
            if elem in diction.keys():
                result = diction[elem]
                self.info["consts"][to_st(result)] = result
                array[i] = result
        return array

    def convert_variables(self, array):
        for i, elem in enumerate(array):
            if (type(elem) == str) and (len(elem) == 1) and elem.isalpha():
                result = Variable(elem)
                self.info["variables"][to_st(result)] = result
                array[i] = result
        return array        

    def convert_st_f_r_i(self, array):
        signs, funcs = lambda x: type(x) == str, self.functions
        message = "Некорректная запись у  объекта  <{}>"
        first, last = array[0], array[-1]
        if last in list("√^"):
            raise DecodeError(f"Объект <{last}> не должен стоять в конце выражения")
        if first == "^":
            raise DecodeError(f"Объект <{first}> не должен стоять в начале выражения")
        for i in range(len(array) - 2, -1, -1):
            elem, elem_1 = array[i], array[i + 1]
            if elem in funcs:
                if elem != "log":
                    if elem_1 == "^":
                        st = array[i + 2]
                        if i + 3 == len(array):
                            raise DecodeError(message.format(elem))
                        arg = array[i + 3]
                        if signs(arg) or signs(st):
                            raise DecodeError(message.format(elem))
                        func = diction[elem](arg)
                        self.info["funcs"][to_st(func)] = func
                        poww = Pow(func, st)
                        self.info["Pows"][to_st(poww)] = poww
                        array[i] = poww
                        del array[i+1:i+4]
                    else:
                        arg = array[i+1]
                        if signs(arg):
                            raise DecodeError(message.format(elem))
                        func = diction[elem](arg)
                        self.info["funcs"][to_st(func)] = func                       
                        array[i] = func
                        del array[i+1]
                elif elem == "log":
                    if elem_1 == "^":
                        st = array[i+2]
                        if i + 4 >= len(array):
                            raise DecodeError(message.format(elem))
                        arg1, arg2 = array[i+3:i+5]
                        if signs(st) or signs(arg1) or signs(arg2):
                            raise DecodeError(message.format(elem))
                        func = diction[elem](arg1, arg2)
                        self.info["funcs"][to_st(func)] = func
                        poww = Pow(func, st)
                        self.info["Pows"][to_st(poww)] = poww
                        array[i] = poww
                        del array[i+1:i+5]
                    else:
                        if i + 2 == len(array):
                            raise DecodeError(message.format(elem))
                        arg1, arg2 = array[i+1:i+3]
                        if signs(arg1) or signs(arg2):
                            raise DecodeError(message.format(elem))
                        func = diction[elem](arg1, arg2)
                        self.info["funcs"][to_st(func)] = func
                        array[i] = func
                        del array[i+1:i+3]
            elif elem == "√":
                if signs(elem_1):
                        raise DecodeError(message.format(elem))
                radical = Radical(elem_1)
                self.info["Radicals"][to_st(radical)] = radical
                array[i] = radical
                del array[i+1]
            elif elem_1 == "^":
                st = array[i+2]
                if signs(elem) or signs(st):
                    raise DecodeError(f"Объект <{elem_1}> не должен соединять <{elem}> и <{st}>")
                poww = Pow(elem, st)
                self.info["Pows"][to_st(poww)] = poww
                array[i] = poww
                del array[i+1:i+3]
            elif (i == 0) and (elem == "-"):
                if signs(elem_1):
                    raise DecodeError(message.format(elem))
                array[i] = neg(elem_1)
                del array[i+1]
                
        return array

    def convert_m_d_a_s(self, array):
        diction = {"*": "Muls", "/": "Fractions", "+": "Adds", "-": "Adds"}
        signs = lambda x: type(x) == str
        message = "Некорректная запись у  объекта  <{}>"
        first, last = array[0], array[-1]
        if last in list("+-*/"):
            raise DecodeError(f"Объект <{last}> не должен стоять в конце выражения")
        if first in list("+-*/"):
            raise DecodeError(f"Объект <{first}> не должен стоять в начале выражения")
        for i in range(1 - len(array), 0):
            elem_1, elem = array[i-1], array[i]
            if not (signs(elem) or signs(elem_1)):
                result = Mul(elem_1, elem)
                self.info["Muls"][to_st(result)] = result
                array[i] = result
                del array[i-1]
            elif elem_1 == "*" or elem_1 == "/":
                elem_2 = array[i-2]
                if signs(elem) or signs(elem_2):
                    raise DecodeError(message.format(elem_1))
                result = Mul(elem_2, elem) if elem_1 == "*" else Fraction(elem_2, elem)
                self.info[diction[elem_1]][to_st(result)] = result
                array[i] = result
                del array[i-2:i]

        for i in range(1 - len(array), 0):
            elem_1, elem = array[i-1], array[i]
            if elem_1 == "+" or elem_1 == "-":
                elem_2 = array[i-2]
                if signs(elem) or signs(elem_2):
                    raise DecodeError(message.format(elem_1))
                result = Add(elem_2, elem) if elem_1 == "+" else Add(elem_2, neg(elem))
                self.info[diction[elem_1]][to_st(result)] = result
                array[i] = result
                del array[i-2:i]

        return array
#a = Decode().decode("log^28,0ab")
#print(str(a), type(a))
"""
objects:
    number 0123456789,
    const pi e
    unknown xyz...
    function sin cos ...
    module ||
    expression ()

signs:
    +
    -
    *
    /
    ^

    √
"""

