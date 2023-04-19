# -*- coding: utf-8 -*-
import json, requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from for_vk.keyboards import Keyboards
from main import ProCalc
from functools import reduce
from functions import nod, nok, decode_expression, to_st, get_muls, converting_one_in_other, factorize_polynomial, for_info_sqrt
from connect_base import Data
from objects import Watch

def NOD(run=False):
    if not run:
        return "Введите, пожалуйста, натуральные числа через пробел. Пример: 6 5 4"
    try:
        array = [int(i) for i in run.split()]
        if any((i < 1) or (i % 1) for i in array) or (not array):
            raise Exception
        word, answer = "Наибольшим общим делителем", nod(*array)
        return f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>"
    except Exception:
        return "Ошибка! Неверно введены данные!"

def factorize(run=False):
    if not run:
        return "Введите, пожалуйста, ненулевое целое число"
    try:
        num = int(run)
        if not num:
            raise Exception
        return f"Множители числа <{num}> : {', '.join(get_muls(num))}"
    except Exception:
        return "Ошибка! Неверно введены данные!"

def average(run=False):
    if not run:
        return "Введите, пожалуйста, действительные числа через пробел. Пример: 6,4 5 -4"
    try:
        arr = run.replace(",", ".").split()
        arr2 = sorted(list(map(float, arr)))
        length, sm = len(arr), sum(arr2)
        return open("txt/average.txt", encoding="utf-8").read().format(', '.join(arr), length, arr2[-1], arr2[0], sm, sm / length, arr2[length // 2] if length % 2 else sum(arr2[length // 2 - 1:length // 2+1]) / 2)
    except Exception:
        return "Ошибка! Неверно введены данные!"

def convert_in_number_systems(run=False):
    if not run:
        return "Введите, пожалуйста, действительное положительное число, его систему счисления и основание системы, в которую надо перевести данное число, через пробел. Пример: 1,4 6 10"
    try:
        arr = run.replace(".", ",").split()
        converting_one_in_other(arr[0], int(arr[1]), int(arr[2]))
        return open('for_converting_one_in_other.txt', 'rb')
    except Exception as e:
        return "Ошибка! Неверно введены данные!"

def NOK(run=False):
    if not run:
        return "Введите, пожалуйста, натуральные числа через пробел. Пример: 6 5 4"
    try:
        array = [int(i) for i in run.split()]
        if any((i < 1) or (i % 1) for i in array) or (not array):
            raise Exception
        word, answer = "Наименьшим общим кратным", nok(*array)
        return f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>"
    except Exception:
        return "Ошибка! Неверно введены данные!"

def fact_on_gorner(run=False):
    if not run:
        return "Введите, пожалуйста, целые числа через пробел. Пример: Дан многочлен 5x^4 + 5x^3 + x^2 - 11 необходимо ввести его коэффициенты через пробел, начиная с наибольшего, т.е. <5 5 1 0 -11>"
    try:
        factorize_polynomial([int(i) for i in run.split()])
        return open('factorize_polynomial.txt', 'rb')
    except Exception:
        return "Ошибка! Неверно введены данные!"

def calc():
    return "Введите выражение с помощью клавиатуры"

def start(run=False):
    if not run:
        return open("txt/for_start.txt", encoding="utf-8").read()
    return ProCalc().run(run)

def compare(run=False):
    if not run:
        return "Введите, пожалуйста, 2 числа или выражения через точку с запятой - <;>. Пример: 6;4"
    else:
        try:
            array = [decode_expression(ex) for ex in run.split(";")]
            obj, obj2 = array
            num, num2 = [i.in_decimal() for i in array]
            if len(array) != 2:
                raise Exception
            sign = ">" if (num > num2) else "<" if (num < num2) else "="
            return f"""{to_st(obj)} = {num}
    {to_st(obj2)} = {num2}
    {num} {sign} {num2} <=> {to_st(obj)} {sign} {to_st(obj2)}"""
        except Exception:
            return "Ошибка! Неверно введены данные!"

def info_sqrt(run=False):
    if not run:
        return "Введите, пожалуйста, натуральное число, и мы подробно извлечем из него квадратный корень"
    else:
        try:
            for_info_sqrt(run)
            return open('for_info.txt', 'rb')
        except Exception:
            return "Ошибка! Неверно введены данные!"

def help(run=False):
    if not run:
        return open("txt/for_help.txt", encoding="utf-8").read()
    return ProCalc().run(run)

def main():
    try:
        data = Data()
        diction = {"Начать": start, "start": start, "help": help, "nod": NOD, "nok": NOK, "compare": compare,
                   "calc": calc, "factorize": factorize, "convert_in_number_systems": convert_in_number_systems,
                   "info_sqrt": info_sqrt, "fact_on_gorner": fact_on_gorner, "average": average}
        group_id = '211987060'
        token = 'vk1.a.AwdM7xE1N5oXMwF29sKbLeRZrCDw7CYmjSpHER1Zj_8o1rmAHdenPoPh2UYsjlrv6ejzTIA9pealqDZ3Ix0743pgPYj-dYiHgsa0QcSlu02L_uP7R8muUE2Smrpe3vCibIREm401xvp9hrEenHiGZb9bk3jl5LtlDViHgRxl4McmgPUyaCozQVkjFBQtWjclQcvU9YzAl34OIYqj6lAapw'
        API_VERSION = '5.131'
        vk_session = vk_api.VkApi(token=token, api_version=API_VERSION)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, group_id=group_id)
        keyboard = Keyboards()
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                id = event.obj.message['from_id']
                msg = event.obj.message['text']
                if not data.isUser(id):
                    data.addUser(id)
                if not data.getLocation(id):
                    data.setLocation(id, "start")
                if msg in diction.keys():
                    data.setLocation(id, msg)
                    if msg == "calc":
                        vk.messages.send(user_id=id, message=diction[msg](), keyboard=keyboard.for_calc.get_keyboard(), random_id=0)
                    else:
                        vk.messages.send(user_id=id, keyboard=keyboard.keyboard1.get_keyboard(), message=diction[msg](), random_id=0)
                else:
                    location = data.getLocation(id)
                    if location in ["fact_on_gorner", "info_sqrt", "convert_in_number_systems"]:
                        peer = event.obj.message['peer_id']
                        answer = diction[location](msg)
                        if type(answer) == str:
                            vk.messages.send(user_id=id, keyboard=keyboard.keyboard1.get_keyboard(), message=answer, random_id=0)
                        else:
                            result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],
                                    files={'file': answer}).text)
                            jsonAnswer = vk.docs.save(file=result['file'], title=location, tags=[])
                            vk.messages.send(peer_id=peer, random_id=0, attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}")
                    else:
                        vk.messages.send(user_id=id, keyboard=keyboard.keyboard1.get_keyboard(), message=diction[location](msg), random_id=0)
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                id = event.object['user_id']
                typ = event.object.payload.get('type')
                if typ in ("funcs", "back"):
                    keyboard.change_keyboard() 
                if typ == "hide":
                    vk.messages.send(user_id=id, message="Меню", keyboard=keyboard.keyboard1.get_keyboard(), random_id=0)
                    data.setLocation(id, "start")
                    keyboard.clear()
                elif typ == "run":
                    msg = keyboard.keyboard2.keyboard["buttons"][0][0]["action"]["label"]
                    result = ProCalc().run(msg)
                    keyboard.clear()
                    vk.messages.send(user_id=id, message=result, keyboard=keyboard.keyboard1.get_keyboard(), random_id=0)
                    data.setLocation(id, "start")
                    keyboard.clear()
                elif typ != "main":
                    info = vk.messages.getHistory(peer_id=event.object.peer_id)['items'][0]
                    message_id, peer_id = info['id'], info['peer_id']
                    if typ == "❌":
                        keyboard.clear()
                    elif typ == "⌫":
                        keyboard.del_one_symbol()
                    elif typ not in ("funcs", "back"):
                        keyboard.add_symbol(typ)
                    vk.messages.edit(peer_id=peer_id, message_id=message_id, message="Введите выражение с помощью клавиатуры", keyboard=keyboard.for_calc.get_keyboard(), random_id=0)
    except Exception as s:
        print(s)
        main()

if __name__ == "__main__":
    main()