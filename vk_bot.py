# -*- coding: utf-8 -*-
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from for_vk.keyboards import Keyboards
from main import ProCalc
from functools import reduce
from functions import nod, nok, decode_expression, to_st

def compare(message):
    try:
        array = [decode_expression(ex) for ex in message[9:].split(";")]
        obj, obj2 = array
        num, num2 = [i.in_decimal() for i in array]
        if len(array) != 2:
            raise Exception
        sign = ">" if (num > num2) else "<" if (num < num2) else "="
        return f"""{to_st(obj)} = {num}
{to_st(obj2)} = {num2}
{num} {sign} {num2} <=> {to_st(obj)} {sign} {to_st(obj2)}"""
    except Exception:
        return "Введите, пожалуйста, 2 числа или выражения через точку с запятой - <;>. Пример: /compare 6;4"

def start():
    return open("txt/for_start.txt", encoding="utf-8").read()

def help():
    return open("txt/for_help.txt", encoding="utf-8").read()

def NODandNOK(msg):
    try:
        array = [decode_expression(ex).in_decimal() for ex in msg[5:].split(";")]
        if any((i < 1) or (i % 1) for i in array) or (not array):
            raise Exception
        word, answer = ("Наибольшим общим делителем", nod(*array)) if msg[:4] == "/nod" else ("Наименьшим общим кратным", nok(*array))
        return f"{word} чисел <{', '.join(list(map(str, array)))}> является число <{answer}>"
    except Exception:
        return "Введите, пожалуйста, натуральные числа через точку с запятой - <;>. Пример: /nod 6;3;4"

if __name__ == "__main__":
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
            if ("/start" in msg and msg.find("/start") == 0) or msg == "Начать":
                print(event.object)
                result = start()
                vk.messages.send(user_id=id, keyboard=keyboard.keyboard1.get_keyboard(), message=result, random_id=0)
            elif "/calc" in msg and msg.find("/calc") == 0:
                vk.messages.send(user_id=id, keyboard=keyboard.for_calc.get_keyboard(), message="Введите выражение с помощью клавиатуры", random_id=0)
            else:
                if "/compare" in msg and msg.find("/compare") == 0:
                    result = compare(msg)
                elif ("/nok" in msg and msg.find("/nok") == 0) or ("/nod" in msg and msg.find("/nod") == 0):
                    result = NODandNOK(msg)
                elif "/help" in msg and msg.find("/help") == 0:
                    result = help()
                else:
                    result = ProCalc().run(msg)
                vk.messages.send(user_id=id, message=result, random_id=0)
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            id = event.object['user_id']
            typ = event.object.payload.get('type')
            if typ in ("funcs", "back"):
                keyboard.change_keyboard() 
            if typ == "hide":
                vk.messages.send(user_id=id, message="Меню", keyboard=keyboard.keyboard1.get_keyboard(), random_id=0)
            elif typ == "run":
                msg = keyboard.keyboard2.keyboard["buttons"][0][0]["action"]["label"]
                result = ProCalc().run(msg)
                keyboard.clear()
                vk.messages.send(user_id=id, message=result, keyboard=keyboard.keyboard1.get_keyboard(), random_id=0)
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