from aiogram import Bot, Dispatcher,types, executor
from aiogram.utils.exceptions import BadRequest

from config import *

import datetime
import time


counter = 0
last_check = 0
user_data = {}
bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def login(message) -> dict: 
    global user_data

    if user_data.get(message.from_user.username) == None:
        user_data = {message.from_user.username: {
                'username'  : message.from_user.username,
                'id'        : message.from_user.id,
                'captchaend': False,
                'ban'       : False,
                'started'   : False,
                'from_start': 0,
                'last_check': 0      
            }
        }
        print(user_data)
    else:
        print('user already exists')

    return user_data

async def check_captcha(message):
    global last_check

    un = message.from_user.username
    now = str(datetime.datetime.now())[11:].replace('.', ',')
    pt = datetime.datetime.strptime(now,'%H:%M:%S,%f')

    user_data[un]['from_start'] = (pt.second + pt.minute*60 + pt.hour*3600) - user_data[un]['last_check']
    user_data[un]['last_check'] = user_data[un]['from_start'] 

    for x, y in user_data.items():
        if y['captchaend'] == False:
            if user_data[un]['ban'] == False:
                if user_data[un]['from_start'] >= time1 and user_data[un]['from_start'] <= time2:
                    await bot.send_message(y['id'], 'Иначе нам придется удалить вас из телеграм канала агентства недвижимости WellDom')
                    await bot.send_message(y['id'], 'Пожалуйста, пройдите проверку на бота, нажмите кнопку "Я человек"')
                elif user_data[un]['from_start'] >= time2 and user_data[un]['from_start'] <= time3:
                    await bot.send_message(y['id'], 'Пожалуйста, пройдите проверку на бота, нажмите кнопку "Я человек"')
                    user_data[un]['ban'] = True
            else:
                if user_data[un]['last_check'] >= time3 or user_data[un]['from_start'] >= time3:
                    await bot.send_message(y['id'], 'ban')
                    await bot.ban_chat_member(chat_id = -1721449565, user_id = y['id'])

@dp.chat_join_request_handler()
async def start1(update: types.ChatJoinRequest):
    global counter
    try:
        counter += 1
        if counter >= 300:
            time.sleep(1800)
        await update.approve()
        print(update)
    except BadRequest:
        print('user exists')

    global user_data

    await login(message = update)
    print('new user ->', user_data)

    if user_data[update.from_user.username]['started'] == False:
        user_data[update.from_user.username]['started'] = True
        await bot.send_message(update.from_user.id, f'Здравствуйте, это агентство недвижимости WellDom\nБлагодарим вас за подписку на наш телеграм канал!')
        await bot.send_message(update.from_user.id, 'Просим пройти вас проверку на бота, нажмите кнопку\n"Я человек"', reply_markup = not_bot_reply)
        await check_captcha(message = update)
    elif user_data[update.from_user.username]['started'] == True: 
        await check_captcha(message = update) 

@dp.message_handler(content_types = 'text')
async def aprove_captcha(message: types.Message):
    global user_data
    await login(message = message)
    print('new user ->', user_data)

    if 'я человек' in message.text.lower():
        await bot.send_message(message.from_id, 'Спасибо, вы прошли проверку', reply_markup = channel_link)
        print(f'{message.from_user.username} прошел проверку')
        user_data[message.from_user.username]['captchaend'] = True

executor.start_polling(dp)