import vk_api
import requests
import random
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
TOKEN = '0f4c69850a09e23c3ded0bc54d4f672684d50b066ec6670a1f863ad954b4348aa9835a21f3fdf016c74a8'
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '187553870')#группа тест

filename = "keyboard.json" 
file = open(filename, "r", encoding="UTF-8") 
keyboard = file.read()

pogoda = [501175,4778626,5601538,534372,578155]
def weather(id):
    
    #s_city = "Rostov-na-Donu,RU"
    #city_id = 4778626 питер
    city_id = id
    appid = "ff804351b97f7a93823cbf829df18b62"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
        params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print (data)
        main = data['main']
        wind = data['wind']
        if data['weather'][0]['description'] == 'легкий дождь':
            reply = """Погода: {} ☂ 
Текущая температура: {}°С
Скорость ветра: {} м/с""".format(data['weather'][0]['description'],\
                             round(main['temp']), round(wind['speed']))
        elif (data['weather'][0]['description'] == 'облачно'):#and(0<main['temp']<20):
            reply = """Погода: {} ☁
Текущая температура: {}°С 
Скорость ветра: {} м/с""".format(data['weather'][0]['description'],\
                             round(main['temp']), round(wind['speed']))
        elif (data['weather'][0]['description'] == 'ясно'):#and(0<main['temp']<20):
            reply = """Погода: {} &#9728; 
Текущая температура: {}°С 
Скорость ветра: {} м/с""".format(data['weather'][0]['description'],\
                             round(main['temp']), round(wind['speed']))
        else:
            reply = """Погода: {} 
Текущая температура: {}°С
Скорость ветра: {} м/с""".format(data['weather'][0]['description'],\
                             round(main['temp']), round(wind['speed']))
    except Exception as e:
        print("Exception (weather):", e)
        pass
    return reply


for event in longpoll.listen(): #Проверка действий
     if event.type == VkBotEventType.MESSAGE_NEW: # последняя строчка
        #проверяем не пустое ли сообщение нам пришло
        if event.obj.text != '': 
            #проверяем пришло сообщение от пользователя или нет
            if event.from_user:
                if event.obj.text == 'Привет':
                    reply = 'Привет'
                    filename = "keyboard.json" 
                    file = open(filename, "r", encoding="UTF-8") 
                    keyboard = file.read()
                elif event.obj.text == 'Как дела?':
                    reply = 'Хорошо, а у тебя?'
            #    elif ((event.obj.text == 'Хорошо') or (event.obj.text == 'хорошо')):
                    
                elif (event.obj.text == 'Скажи погоду'):
                   reply = 'Где?'
                   filename = "keyboard2.json" 
                   file = open(filename, "r", encoding="UTF-8") 
                   keyboard = file.read()
                   
                elif (event.obj.text == 'В Ростове'):
                   reply = weather(pogoda[0])
                elif (event.obj.text == 'В Питере'):
                   reply = weather(pogoda[1])
                elif (event.obj.text == 'В Москве'):
                   reply = weather(pogoda[2])
                elif (event.obj.text == 'В Натальевке'):
                   reply = weather(pogoda[3])
                elif (event.obj.text == 'В Белой Калитве'):
                   reply = weather(pogoda[4])
                   
                else:
                    reply = 'Я тебя не понимаю'
                
                    
                #отправляем сообщение
                vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=get_random_id(),
                        message=reply,
                        keyboard=keyboard)
        