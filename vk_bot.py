import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from main import ProCalc


if __name__ == "__main__":
    token = 'vk1.a.zrBGSLszP1RY13KVd9cNcD0lWT3xwJ0HYF0guNsRHI8goG-qvW3bvxhSpymn3LSdp-nNe_t_Zn2eVvlqCzwEHtYpBfT_ZEICATGvnlXyRrVcbSDbNhPdiQqTDuik-L9JTKk-qZhzrLxIsOkzCSrQw7u4gFO98f12eIGzCbrw41W1pjkZeU7bhiperAfd0Vp1'
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text
            id = event.user_id
            result = ProCalc().run(msg)
            vk.messages.send(user_id=id, message=result, random_id=0)