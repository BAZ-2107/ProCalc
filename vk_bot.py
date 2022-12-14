# -*- coding: utf-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard

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
    return "Здравствуйте" + open("txt/for_start.txt", encoding="utf-8").read().replace("""
  Также можно воспользоваться командой /calc, которая запустит клавиатуру для набора символов""", "")[20:]

def help():
    return "Здравствуйте" + open("txt/for_help.txt", encoding="utf-8").read().replace("""
  Если Вам неудобно набирать символы со своей клавиатуры, есть вариант воспользоваться командой /calc, которая предложит инлайн-клавиатуру""", "")[20:]

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
    token = 'vk1.a.zrBGSLszP1RY13KVd9cNcD0lWT3xwJ0HYF0guNsRHI8goG-qvW3bvxhSpymn3LSdp-nNe_t_Zn2eVvlqCzwEHtYpBfT_ZEICATGvnlXyRrVcbSDbNhPdiQqTDuik-L9JTKk-qZhzrLxIsOkzCSrQw7u4gFO98f12eIGzCbrw41W1pjkZeU7bhiperAfd0Vp1'
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button("Hi")
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text
            if "/compare" in msg and msg.find("/compare") == 0:
                result = compare(msg)
            elif ("/nok" in msg and msg.find("/nok") == 0) or ("/nod" in msg and msg.find("/nod") == 0):
                result = NODandNOK(msg)
            elif "/start" in msg and msg.find("/start") == 0:
                result = start()
            elif "/help" in msg and msg.find("/help") == 0:
                result = help()            
            else:
                result = ProCalc().run(msg)
            id = event.user_id
            vk.messages.send(user_id=id, message=result, random_id=0)