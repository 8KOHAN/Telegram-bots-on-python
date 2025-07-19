from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/booking")],
        [KeyboardButton(text="/help")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
