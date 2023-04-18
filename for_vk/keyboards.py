# -*- coding: utf-8 -*-
from vk_api.keyboard import VkKeyboard

class Keyboards:
    color = 'primary'
    keyboard1 = VkKeyboard()
    for i, row in enumerate(["start", "help", "calc", "nod", "nok", "compare", "factorize", 
                             "convert_in_number_systems", "info_sqrt", "fact_on_gorner", 
                             "average"]):
        if (i % 2 == 0) and (i != 0):
            keyboard1.add_line()
        keyboard1.add_button(row)

    keyboard2 = VkKeyboard(one_time=False, inline=False)
    keyboard2.add_callback_button(label='✍', payload={"type": "main"})
    keyboard2.add_line()
    for i, smbl in enumerate("(|)❌⌫123+/456-^789*√0,πe"):
        if (i % 5 == 0) and (i != 0):
            keyboard2.add_line()
        keyboard2.add_callback_button(label=smbl, payload={"type": smbl}, color=color)
    keyboard2.add_callback_button(label='f(x)', payload={"type": "funcs"}, color=color)
    keyboard2.add_line()
    keyboard2.add_callback_button(label='✅', payload={"type": "run"}, color=color)
    keyboard2.add_callback_button(label='⤵', payload={"type": "hide"}, color=color)

    keyboard3 = VkKeyboard(one_time=False, inline=False)
    keyboard3.add_callback_button(label='✍', payload={"type": "main"})
    keyboard3.add_line()
    symbols = open("txt/functions.txt", encoding="utf-8").read().split()
    for i, row in enumerate(symbols):
        if (i % 3 == 0) and i != 0:
            keyboard3.add_line()
        keyboard3.add_callback_button(label=row, payload={"type": row}, color=color)
    keyboard3.add_callback_button(label='⌫', payload={"type": "⌫"}, color=color)
    keyboard3.add_callback_button(label='❌', payload={"type": "❌"}, color=color)
    keyboard3.add_callback_button(label='Назад', payload={"type": "back"}, color=color)

    for_calc = keyboard2

    def change_keyboard(self):
        self.for_calc = self.keyboard3 if self.for_calc == self.keyboard2 else self.keyboard2

    def add_symbol(self, symbol):
        label = self.keyboard2.keyboard["buttons"][0][0]["action"]["label"]
        if len(label) == 1 and label == "✍":
            self.keyboard2.keyboard["buttons"][0][0]["action"]["label"] = symbol
            self.keyboard3.keyboard["buttons"][0][0]["action"]["label"] = symbol
        else:
            self.keyboard2.keyboard["buttons"][0][0]["action"]["label"] += symbol
            self.keyboard3.keyboard["buttons"][0][0]["action"]["label"] += symbol

    def clear(self):
        self.keyboard2.keyboard["buttons"][0][0]["action"]["label"] = '✍'
        self.keyboard3.keyboard["buttons"][0][0]["action"]["label"] = '✍'

    def del_one_symbol(self):
        label = self.keyboard2.keyboard["buttons"][0][0]["action"]["label"]
        if len(label) != 1:
            self.keyboard2.keyboard["buttons"][0][0]["action"]["label"] = label[:-1]
            self.keyboard3.keyboard["buttons"][0][0]["action"]["label"] = label[:-1]
        else:
            self.clear()