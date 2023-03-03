# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from  for_tg.keyboards import Keyboards
from main import ProCalc
from functools import reduce
from functions import nod, nok, decode_expression, to_st, get_muls, converting_one_in_other, factorize_polynomial
from connect_base import Data


def run(update, context):
    query = update.callback_query
    label = keyboards.text.text
    if query.data == "text":
        pass
    elif query.data == "✅":
        result = ProCalc().run(keyboards.text.text)
        keyboards.text.text = "✍"
        query.edit_message_text(text=result)
    else:
        if query.data == "⌫":
            if len(label) == 1:
                keyboards.text.text = "✍"
            else:
                keyboards.text.text = label[:-1]
        elif query.data == "❌":
            keyboards.text.text = "✍"
        elif query.data in ("funcs", "back"):
            keyboards.change_calc_keyboard()
        else:
            if label != "✍":
                keyboards.text.text += query.data
            else:
                keyboards.text.text = query.data
        query.answer()
        try:
            query.edit_message_text(text="Введите выражение", reply_markup=keyboards.for_calc)
        except Exception:
            pass

def NOD(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "nod")
        update.message.reply_text(text="Введите, пожалуйста, натуральные числа через пробел. Пример: 6 5 4")
    else:
        try:
            array = [int(i) for i in update.message.text.split()]
            if any((i < 1) or (i % 1) for i in array) or (not array):
                raise Exception
            word, answer = "Наибольшим общим делителем", nod(*array)
            update.message.reply_text(text=f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def factorize(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "factorize")
        update.message.reply_text(text="Введите, пожалуйста, ненулевое целое число")
    else:
        try:
            num = int(update.message.text)
            if not num:
                raise Exception
            update.message.reply_text(text=f"Множители числа <{num}> : {', '.join(get_muls(num))}")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def average(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "average")
        update.message.reply_text(text="Введите, пожалуйста, действительные числа через пробел. Пример: 6,4 5 -4")
    else:
        try:
            arr = sorted(float(i) for i in update.message.text.replace(",", ".").split())
            update.message.reply_text(text=f"""Дана выборка: <{', '.join(list(map(str, arr)))}>
Количество элементов: <{len(arr)}>
Максимальный элемент: <{arr[-1]}>
Минимальный элемент: <{arr[0]}>
Сумма элементов: <{sum(arr)}>
Среднее арифметическое: <{sum(arr) / len(arr)}>
Медиана выборки: <{arr[len(arr) // 2] if len(arr) % 2 else sum(arr[len(arr) // 2 - 1:len(arr) // 2+1]) / 2}>""")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def convert_in_number_systems(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "convert_in_number_systems")
        update.message.reply_text(text="Введите, пожалуйста, действительное положительное число, его систему счисления и основание системы, в которую надо перевести данное число, через пробел. Пример: 1,4 6 10")
    else:
        try:
            arr = update.message.text.replace(".", ",").split()
            update.message.reply_text(text=f"""Дано число: <{arr[0]}>
Основание его системы счисления: <{arr[-2]}>
Система счисления, в которую надо перевести: <{arr[-1]}>
Результат перевода: <{converting_one_in_other(arr[0], int(arr[-2]), int(arr[-1]))}>""")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def NOK(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "nok")
        update.message.reply_text(text="Введите, пожалуйста, натуральные числа через пробел. Пример: 6 5 4")
    else:
        try:
            array = [int(i) for i in update.message.text.split()]
            if any((i < 1) or (i % 1) for i in array) or (not array):
                raise Exception
            word, answer = "Наименьшим общим кратным", nok(*array)
            update.message.reply_text(text=f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def fact_on_gorner(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "fact_on_gorner")
        update.message.reply_text(text="Введите, пожалуйста, целые числа через пробел. Пример: Дан многочлен 5x^4 + 5x^3 + x^2 - 11 необходимо ввести его коэффициенты через пробел, начиная с наибольшего, т.е. <5 5 1 0 -11>")
    else:
        try:
            arr = [int(i) for i in update.message.text.split()]
            array = factorize_polynomial([arr])
            st = ""
            for i in array:
                st += "("
                n = len(i)
                for j, k in enumerate(i):
                    if j != 0:
                        st += " - " if k < 0 else " + "
                    elif k < 0:
                        st += "-"
                    k = abs(k)
                    if j == n - 1:
                        st += str(k)
                    elif j == n - 2:
                        st += f"{k}x"
                    else:
                        st += f"{k}x^{n - j - 1}"
                st += ")"
            update.message.reply_text(text=f"""Были заданы коэффициенты: {" ".join(str(i) for i in arr)}
Результат: < {st} >""")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def calc(update, context):
    data(update.message.chat.id).setLocation(update.message.chat.id, "calc")
    keyboards.text.text = "✍"
    update.message.reply_text(text="Введите выражение", reply_markup=keyboards.for_calc)

def start(update, context):
    data(update.message.chat.id).setLocation(update.message.chat.id, "menu")
    update.message.reply_text(text=open("txt/for_start.txt", encoding="utf-8").read())

def compare(update=None, context=None, run=False):
    if not run:
        data(update.message.chat.id).setLocation(update.message.chat.id, "compare")
        update.message.reply_text(text="Введите, пожалуйста, 2 числа или выражения через точку с запятой - <;>. Пример: 6;4")
    else:
        try:
            array = [decode_expression(ex) for ex in update.message.text.split(";")]
            obj, obj2 = array
            num, num2 = [i.in_decimal() for i in array]
            if len(array) != 2:
                raise Exception
            sign = ">" if (num > num2) else "<" if (num < num2) else "="
            update.message.reply_text(text=f"""{to_st(obj)} = {num}
    {to_st(obj2)} = {num2}
    {num} {sign} {num2} <=> {to_st(obj)} {sign} {to_st(obj2)}""")
        except Exception:
            update.message.reply_text(text="Ошибка! Неверно введены данные!")

def help(update, context):
    data(update.message.chat.id).setLocation(update.message.chat.id, "menu")
    update.message.reply_text(text=open("txt/for_help.txt", encoding="utf-8").read())

def message_input(update, context):
    try:
        location = data(update.message.chat.id).getLocation(update.message.chat.id)      
        if location == "compare":
            compare(update, context, run=True)
        elif location == "nod":
            NOD(update, context, run=True)
        elif location == "nok":
            NOK(update, context, run=True)
        elif location == "menu":
            result = ProCalc().run(update.message.text)
            update.message.reply_text(text=result)
        elif location == "factorize":
            factorize(update, context, run=True)     
        elif location == "calc":
            run(update.message.text)
        elif location == "average":
            average(update, context, run=True)
        elif location == "convert_in_number_systems":
            convert_in_number_systems(update, context, run=True)
        elif location == "fact_on_gorner":
            fact_on_gorner(update, context, run=True)
    except Exception:
        update.message.reply_text(text="Ой, перезапустите меня, пожалуйста! /start")
    


if __name__ == '__main__': # запуск программы
    TOKEN = "5470284710:AAH5J030yTMQsPH1R64ZjcES_8z6ZIE407U" # токен бота
    updater = Updater(token=TOKEN, use_context=True) # создание объекта, осуществляющего связь между ботом и пользователем
    data = Data()
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("calc", calc))
    dispatcher.add_handler(CommandHandler("nod", NOD))
    dispatcher.add_handler(CommandHandler("factorize", factorize))
    dispatcher.add_handler(CommandHandler("nok", NOK))
    dispatcher.add_handler(CommandHandler("compare", compare))
    dispatcher.add_handler(CommandHandler("average", average))
    dispatcher.add_handler(CommandHandler("fact_on_gorner", fact_on_gorner))
    dispatcher.add_handler(CommandHandler("convert_in_number_systems", convert_in_number_systems))
    dispatcher.add_handler(CallbackQueryHandler(run))
    dispatcher.add_handler(MessageHandler(Filters.text, message_input))
    keyboards = Keyboards()
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта