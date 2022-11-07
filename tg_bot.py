# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from  for_tg.keyboards import Keyboards
from main import ProCalc
from functools import reduce
from functions import nod, nok, decode_expression, to_st


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
        array = [decode_expression(ex).in_decimal() for ex in update.message.text[5:].split(";")]
        if any((i < 1) or (i % 1) for i in array) or (not array):
            raise Exception
        word, answer = ("Наибольшим общим делителем", nod(*array)) if update.message.text[:4] == "/nod" else ("Наименьшим общим кратным", nok(*array))
        update.message.reply_text(text=f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>")
    except Exception:
        update.message.reply_text(text="Введите, пожалуйста, натуральные числа через точку с запятой - <;>. Пример: /nod 6;3;4")

def calc(update, context):
    keyboards.text.text = " "
    update.message.reply_text(text="Введите выражение", reply_markup=keyboards.for_calc)

def start(update, context):
    update.message.reply_text(text=open("txt/for_start.txt", encoding="utf-8").read().format(update.message.chat.first_name))

def compare(update, context):
    try:
        array = [decode_expression(ex) for ex in update.message.text[9:].split(";")]
        obj, obj2 = array
        num, num2 = [i.in_decimal() for i in array]
        if len(array) != 2:
            raise Exception
        sign = ">" if (num > num2) else "<" if (num < num2) else "="
        update.message.reply_text(text=f"""{to_st(obj)} = {num}
{to_st(obj2)} = {num2}
{num} {sign} {num2} <=> {to_st(obj)} {sign} {to_st(obj2)}""")
    except Exception:
        update.message.reply_text(text="Введите, пожалуйста, 2 числа или выражения через точку с запятой - <;>. Пример: /compare 6;4")

def help(update, context):
    update.message.reply_text(text=open("txt/for_help.txt", encoding="utf-8").read().format(update.message.chat.first_name))

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
    dispatcher.add_handler(CommandHandler("compare", compare))
    dispatcher.add_handler(CallbackQueryHandler(run))
    dispatcher.add_handler(MessageHandler(Filters.text, message_input))
    keyboards = Keyboards()
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта