# -*- coding: utf-8 -*-
from exceptions import *
from output import out
from functions import *

#{'numbers': {'2': <objects.Integer object at 0x000001B654D14790>}, 'consts': {}, 'variables': {}, 'funcs': {}, 'Modules': {}, 'Pows': {}, 'Adds': {'2+2': <objects.Add object at 0x000001B654D149D0>}, 'Muls': {}, 'Radicals': {}, 'Fractions': {}}

# основная функция
class Convert:
    def __init__(self, obj, info):
        self.obj, self.info = obj, info

    def run(self):
        st, typ = to_st(self.obj), type(self.obj).__name__
        print(self.info)
        result = True
        while result:
            result, self.obj = self.obj.update()
        '''
        if typ == "Add":
            pass
        elif typ == "Module":
            if not self.info["variables"]:
                res = in_decimal(self.obj.cont)
                self.obj = neg(self.obj.cont) if res < 0 else self.obj.cont
                out(f"Модуль раскрыт: <{to_st(self.obj)}>")
                return
        '''
        if not self.info["variables"]:
            out(f"Результат вычисления: <{in_decimal(self.obj)}>")