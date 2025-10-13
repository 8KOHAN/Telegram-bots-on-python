from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_reply_kb(is_admin=False):
    keyboard = [
        [KeyboardButton(text="Categories")],
        [KeyboardButton(text="Support")]
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="🔧 Admin panel")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
