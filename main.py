# -*- coding: utf-8 -*-

import os
from output import out
from exceptions import *
from check_string import check_string
from decoder import decode_string
#from ConvertExpression import run

class ProCalc:
    def run(self, st):
        with open("info.txt", "w", encoding="utf-8"):
            pass        
        try:
            st = st.replace(" ", "")
            check_string(st) # проверка символов
            decode_string(st) # расшифровка строки
        except CheckStringError as message:
            out("Ошибка! " + str(message))
        except DecodeStringError as message:
            out("Ошибка! " + str(message))
        except DecodeError as message:
            out("Ошибка! " + str(message))
        except ConvertError as message:
            out("Ошибка! " + str(message))
        except CalculateError as message:
            out("Ошибка! " + str(message))
        except TrigonometricError as message:
            out("Ошибка! " + str(message))
        except LogarithmicError as message:
            out("Ошибка! " + str(message))        
        except Exception as message:
            out("Ошибка: " + str(message))
        finally:
            st = open("info.txt", "r", encoding="utf-8").read()
            os.remove("info.txt")
            return st