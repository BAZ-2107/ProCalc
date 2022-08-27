# -*- coding: utf-8 -*-

import os
from output import out
from exceptions import *
from check_string import check_string
from decoder import decode_string
from ConvertExpression import run

class ProCalc:
    def run(self, st):
        try:
            out(f"На вход получена строка: < {st} >")
            st = st.replace(" ", "")
            check_string(st) # проверка символов
            obj, value = decode_string(st)
            if obj == "ex":
                out(f"Расшифрована как: {value}")
                result = run(value)
                out(f"Результат упрощения: < {str(result)} >")
                
        except UncorrectStringError:
            out("Ошибка! Входная строка не должна быть пустой")
        except UnknownSymbolError as ch:
            out(f"Ошибка! Найден неизвестный символ: <{str(ch)}>")
        except MoreOneSignEqualError:
            out("Ошибка! В выражении не должно быть больше одного знака сравнения")
        except DecodeError as message:
            out("Ошибка! " + str(message))
        except Exception as message:
            out("Упс, реальная ошибка " + str(message))

if __name__ == "__main__":
    with open("info.txt", "w", encoding="utf-8"):
        pass
    expression = "-5"
    ProCalc().run(expression)
    print(open("info.txt", "r", encoding="utf-8").read())
    os.remove("info.txt")
