# -*- coding: utf-8 -*-
from exceptions import DecodeStringError
from DecodeExpression import Decode
from ConvertExpression import Convert
from output import out
from functions import to_st


def decode_string(st):
    out(f"На вход получена строка: < {st} >")
    k, sign = 0, None
    for ch in st:
        if ch == "=":
            k, sign = k + 1, "="
        elif ch in ">⩾⩽<":
            k, sign = k + 1, ch
        if k > 1:
            raise DecodeStringError("В строке более 1 знака отношения")
    if not sign:
        info, res = Decode().decode(st)
        if type(res).__name__ in ("Integer", "Variable", "Pi", "Exp"):
            res.run()
        elif not info["variables"]:
            out(f"Результат вычисления: <{res.in_decimal()}>")
        else:
            out("Извините, решать буквенные выражения не умею (")
            #Convert(res, info).run()
            
    else:
        if "" in st.split(sign):
            raise DecodeStringError("Знак отношения должен соединять выражения")
        out("Извините, решать уравнения или неравенства не умею (")
        #answer, obj = 
#    if sign == "=":
#        return Decoded_Equal(st).run()
#    return Decoded_Unequal(st).run()

