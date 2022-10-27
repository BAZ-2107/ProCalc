# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from  for_tg.keyboards import Keyboards
from main import ProCalc
from functools import reduce
from functions import nod, nok


def run(update, context):
    query = update.callback_query
    if query.data == "text":
        pass
    elif query.data == "running":
        result = ProCalc().run(keyboards.text.text)
        keyboards.text.text = " "
        query.edit_message_text(text=result)    
    else:
        if query.data == "CE":
            if len(keyboards.text.text) != 1:
                keyboards.text.text = keyboards.text.text[:-1]
        elif query.data == "C":
            if keyboards.text.text != " ":
                keyboards.text.text = " "
        elif query.data in ("letters", "back"):
            keyboards.change_calc_keyboard()
        else:
            keyboards.text.text += query.data
        query.answer()
        query.edit_message_text(text="Введите выражение", reply_markup=keyboards.for_calc)

def NODandNOK(update, context):
    try:
        array = list(map(int, update.message.text[5:].split()))
        if any(i < 1 for i in array) or not array:
            raise Exception
        word, answer = ("делителем", nod(*array)) if update.message.text[:4] == "/nod" else ("кратным", nok(*array))
        update.message.reply_text(text=f"Наибольшим общим {word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>")
        
    except Exception:
        update.message.reply_text(text="Введите, пожалуйста, натуральные числа через пробел. Пример: /nod 6 3 4")

def calc(update, context):
    keyboards.text.text = " "
    update.message.reply_text(text="Введите выражение", reply_markup=keyboards.for_calc)

def start(update, context):
    update.message.reply_text(text=f"""
  Здравствуйте, <{update.message.chat.first_name}>! Я - продвинутый калькулятор, могу не только вычислять числовые выражения, но и решать уравнения и неравенства с переменными!

  Если выражение вводится в поле ввода, то использоваться могут только цифры, латинские и греческие буквы (в нижнем регистре) и следующие знаки : < +-*/^√,>⩾=⩽<(|) >

  Также можно воспользоваться командой /calc, которая запустит клавиатуру для набора символов.

  Также есть команда /help, которая, возможно, поможет вам в чем-то.

Для того чтобы вычислить НОД или НОК нескольких НАТУРАЛЬНЫХ чисел, надо записать либо команду /nod, либо команду /nok, затем через ПРОБЕЛ записать натуральные числа. Пример: /nod 2 3 4

  Успехов!""")

def help(update, context):
    update.message.reply_text(text=f"""
  Здравствуйте, <{update.message.chat.first_name}>! Вы находитесь в чате с ботом, который, возможно, поможет вам в вычислении или решении уравнений и неравенств.

  Вы можете вводить ТОЛЬКО греческие или латинские буквы В НИЖНЕМ регистре и следующие знаки : < +-*/^√,>⩾=⩽<(|) >

  Если Вам неудобно набирать со своей клавиатуры, есть вариант воспользоваться командой /calc, которая предложит инлайн-клавиатуру

Для того чтобы вычислить НОД или НОК нескольких НАТУРАЛЬНЫХ чисел, надо записать либо команду /nod, либо команду /nok, затем через ПРОБЕЛ записать натуральные числа. Пример: /nod 2 3 4

  Писать боту что-то, не содержащее в себе выражение, бесполезно: бот Вас не поймет :(""")

def message_input(update, context):
    result = ProCalc().run(update.message.text)
    update.message.reply_text(text=result)


if __name__ == '__main__': # запуск программы    
    TOKEN = "5470284710:AAH5J030yTMQsPH1R64ZjcES_8z6ZIE407U" # токен бота
    updater = Updater(token=TOKEN, use_context=True) # создание объекта, осуществляющего связь между ботом и пользователем
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("calc", calc))
    dispatcher.add_handler(CommandHandler("nod", NODandNOK))
    dispatcher.add_handler(CommandHandler("nok", NODandNOK))
    dispatcher.add_handler(CallbackQueryHandler(run))
    dispatcher.add_handler(MessageHandler(Filters.text, message_input))
    keyboards = Keyboards()
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта