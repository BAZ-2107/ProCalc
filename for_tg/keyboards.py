# -*- coding: utf-8 -*-

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    text = InlineKeyboardButton('✍', callback_data='text')
    one = InlineKeyboardButton('1', callback_data='1')
    two = InlineKeyboardButton('2', callback_data='2')
    three = InlineKeyboardButton('3', callback_data='3')
    four = InlineKeyboardButton('4', callback_data='4')
    five = InlineKeyboardButton('5', callback_data='5')
    six = InlineKeyboardButton('6', callback_data='6')
    seven = InlineKeyboardButton('7', callback_data='7')
    eight = InlineKeyboardButton('8', callback_data='8')
    nine = InlineKeyboardButton('9', callback_data='9')
    zero = InlineKeyboardButton('0', callback_data='0')
    
    add = InlineKeyboardButton('+', callback_data='+')
    sub = InlineKeyboardButton('-', callback_data='-')
    mul = InlineKeyboardButton('*', callback_data='*')
    div = InlineKeyboardButton('/', callback_data='/')
    poww = InlineKeyboardButton('^', callback_data='^')
    sqrt = InlineKeyboardButton('√', callback_data='√')
    
    #more = InlineKeyboardButton('>', callback_data='>')
    #more_or_equal = InlineKeyboardButton('⩾', callback_data='⩾')
    #equal = InlineKeyboardButton('=', callback_data='=')
    #less_or_equal = InlineKeyboardButton('⩽', callback_data='⩽')
    #less = InlineKeyboardButton('<', callback_data='<')
    
    comm = InlineKeyboardButton(',', callback_data=',')
    
    right_bracket = InlineKeyboardButton(')', callback_data=')')
    left_bracket = InlineKeyboardButton('(', callback_data='(')
    module_bracket = InlineKeyboardButton('|', callback_data='|')
    
    del_last = InlineKeyboardButton('⌫', callback_data='⌫')
    del_all = InlineKeyboardButton('❌', callback_data='❌')
    
    running = InlineKeyboardButton('✅', callback_data='✅')
    
    back = InlineKeyboardButton('Назад', callback_data='back')
    
    letters = InlineKeyboardButton('f(x)', callback_data='funcs')

    pi = InlineKeyboardButton('π', callback_data='π')

    exp = InlineKeyboardButton('e', callback_data='e')
    
    
    button_list = [[text],
                   [left_bracket, module_bracket, right_bracket, del_last, del_all],
                   [one, two, three, add, div], [four, five, six, sub, poww],
                   [seven, eight, nine, mul, sqrt],
                    [zero, comm, pi, exp, letters],
                   [running]]
    
    
    symbols, array = open("txt/functions.txt", encoding="utf-8").read().split(), []
    for i, row in enumerate(symbols):
        if i % 3 == 0:
            array.append([])     
        array[-1] += [InlineKeyboardButton(row, callback_data=row)]
    
    button_list_2 = [[text], *array]
    
    button_list_2[-1] += [del_last, del_all, back]    

    for_calc_keyboard_1, for_calc_keyboard_2 = InlineKeyboardMarkup(button_list), InlineKeyboardMarkup(button_list_2)

    for_calc = for_calc_keyboard_1

    def change_calc_keyboard(self):
        self.for_calc = self.for_calc_keyboard_1 if self.for_calc == self.for_calc_keyboard_2 else self.for_calc_keyboard_2