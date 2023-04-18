from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


MAIN_CHAT_ID = ''
TOKEN = '6209685377:AAHkS4wVUTGtDiL5x0lrM5krljuNdWBYwUg'

time1 = 7200
time2 = 79200
time3 = 850002

not_bot_reply = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('Я человек🧍‍♂️')]
    ],
    resize_keyboard = True
)

channel_link = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton('вернуться в тг-канал', url = 'https://t.me/+lRPXSjpRzIY4MjE6')]
    ]
)