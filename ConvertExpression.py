# -*- coding: utf-8 -*-
from exceptions import *
from output import out
from functions import *

# основная функция
class Convert:
    def __init__(self, obj):
        self.obj = obj

    def run(self):
        types = get_all_types(self.obj)

        if "Variable" not in types:
            out(f"Результат вычисления: <{in_decimal(self.obj)}>")