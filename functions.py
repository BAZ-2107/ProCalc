# -*- coding: utf-8 -*-
from functools import reduce
#from objects import Watch


alpha = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
converting_to_decimal_int = lambda a, ss: sum(alpha.index(a[-i-1])*ss**i for i in range(len(a)))
converting_to_decimal_float = lambda a, ss: sum(alpha.index(a[i])*ss**(-i-1) for i in range(len(a)))


class Watch:
    def __init__(self, size=16, border=False):
        self.size = size
        self.arr = []

    def setTitle(self, name):
        self.arr += [name]
        self.arr += ['+']
        

    def setEmptyString(self):
        self.arr += [" "]

    def setString(self, name):
        self.setTitle(name)
        del self.arr[-1]

    def __str__(self):
        st, arr_2 = "", self.arr[:]
        arr_2.insert(0, "+")
        arr_2 += ["+"]
        self.size = max(len(i) for i in self.arr)
        for i, elem in enumerate(arr_2):
            if elem == "+":
                arr_2[i] = elem * (self.size + 4)
            else:
                arr_2[i] = f"+ {elem.ljust(self.size)} +"
        return "\n".join(arr_2)

    def create_table(self, arr):
        size = max(max(len(str(j)) for j in i) for i in arr) + 2
        k = size * len(arr[-1]) + len(arr[-1]) - 1
        while arr:
            self.arr += ["|".join(str(elem).center(size) for elem in arr.pop(0))]
            if arr:
                self.arr += ["-" * k]


def for_info_sqrt(s):
    b, res, arr = s, 0, []
    if int(b) < 0:
        raise Exception
    s = list(str(s))
    if len(s) % 2:
        arr += [int(s.pop(0))]
    while s:
        arr += [int(s.pop(0) + s.pop(0))]
    n = "1"
    a = Watch()
    f = open("txt/info_sqrt.txt", "r", encoding="utf-8")
    a.setTitle(f.readline()[:-1])
    for i in range(10):
        a.setString(f.readline()[:-1])
    a.setString(f.readline()[:-1].format(b))
    a.setString(f.readline()[:-1])
    a.setString(f.readline()[:-1].format("'".join(str(i) for i in arr)))
    a.setString(f.readline()[:-1].format(arr[0]))
    ost, part1, part2 = 0, f.readline()[:-1], f.readline()[:-1]
    while arr:
        ost = ost * 100 + arr.pop(0)
        for_sub = res * 20
        for i in range(9, -1, -1):
            vych = (for_sub + i) * i
            if vych <= ost:
                a.setString(part1.format(i, ost, res, i, i, res*10+i, ost, vych, ost-vych))
                if arr:
                    a.setString(part2.format((ost - vych) * 100 + arr[0]))
                res = res * 10 + i
                ost -= vych
                break
    if ost:
        a.setString(f.readline().format(res) + "(целая часть)")
    else:
        a.setString(f.readline().format(res))
    f.close()
    print(a, file=open("for_info.txt", "w", encoding="utf-8"))

def converting_one_in_other(one, ss1, ss2):
    global alpha
    if any(alpha[ss1] <= i for i in one):
        raise Exception
    st, st2 = "", ""
    f = open("txt/converting_one_in_other.txt", encoding="utf-8")
    a = Watch()
    a.setTitle(f.readline()[:-1])
    for i in range(28):
        a.setString(f.readline()[:-1])
    a.setString(f.readline()[:-1].format(one, ss1, ss2))
    n, mod = (converting_to_decimal_int(one, ss1), None) if "," not in one else (converting_to_decimal_int(one.split(",")[0], ss1), converting_to_decimal_float(one.split(",")[-1], ss1))
    if ss1 != 10:
        b = one.split(",")[0]
        a.setString("Перевод в 10 с.с.: " + "+".join(f"{b[-i-1]}*{ss1}^{i}" for i in range(len(b))) + f"={n}")
        a.setEmptyString()
        if mod:
            k = one.split(",")[-1]
            a.setString("Перевод в 10 с.с. дробной части: "+"+".join(f"{k[i]}*{ss1}^({-i-1})" for i in range(len(k))) + f"={mod}")
    a.setEmptyString()
    a.setString(f"Теперь переводим {n}  в с.с. с основанием {ss2}")
    while n:
        a.setString(f"{n}/{ss2}={n // ss2} (ост. {alpha[n % ss2]})")
        st += alpha[n % ss2]
        n //= ss2
    a.setString(f"При записи остатков наоборот: {st[::-1]}")
    if mod:
        a.setEmptyString()
        a.setString(f"Теперь переводим дробную часть {mod}  в с.с. с основанием {ss2}")        
        st = "," + st
        k, st2 = 0, ""
        while not (k == 6 or (mod % 1) == 0):
            a.setString(f"{mod}*{ss2}={mod * ss2}, Целая часть: {alpha[int(mod * ss2)//1]}, остаток: {mod * ss2 % 1}")
            mod *= ss2
            st2 += alpha[int(mod // 1)]
            mod %= 1
            k += 1
        a.setString(f"В результате дробная часть записывается так: {st2}")
    a.setString(f"Результат перевода: {st[::-1]}{st2}")
    print(a, file=open("for_converting_one_in_other.txt", "w", encoding="utf-8"))
    f.close()


def factorize_polynomial(arr):
    a = Watch()
    a.setTitle("Разложение многочлена по схеме Горнера")
    a.setEmptyString()
    a.setString("Если дан многочлен с целыми коэффициентами,")
    a.setString("то один из его корней может быть делителем свободного члена")
    a.setString("Обозначим его за х. Пусть r = 0. Запишем в строчку коэффициенты")
    a.setString("Действуем по следующему алгоритму: под каждым коэффициентом(a)")
    a.setString("Записываем результат выражения x*r + a, r становится равным x*r + a")
    a.setString("Если под последним коеффициентом получился 0, то мы нашли этот корень")
    a.setEmptyString()
    a.setTitle(f"На вход получены коеффициенты: {', '.join(str(i) for i in arr)}")
    arr2, n, answer = [["x"] + arr[:]], arr[-1], None
    for d in range(1, abs(arr[-1]) + 1):
        if n % d == 0:
            arr2, k = arr2 + [[d]], 0
            for x in arr:
                k = d * k + x
                arr2[-1] += [k]
            if arr2[-1][-1] == 0:
                answer = d
                break
            arr2, k = arr2 + [[-d]], 0
            for x in arr:
                k = -d * k + x
                arr2[-1] += [k]
            if arr2[-1][-1] == 0:
                answer = -d
                break
    a.setEmptyString()
    a.create_table(arr2)
    if answer:
        a.setEmptyString()
        a.setString(f"Подошло число {answer}")
    else:
        a.setEmptyString()
        a.setString(f"К сожалению, никакое число не подошло")        
    print(a, file=open("factorize_polynomial.txt", "w", encoding="utf-8"))


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