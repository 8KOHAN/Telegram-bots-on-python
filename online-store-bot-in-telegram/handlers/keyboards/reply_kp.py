from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_reply_kb(is_admin=False):
    keyboard = [
        [KeyboardButton(text="Категории")],
        [KeyboardButton(text="Поддержка")]
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="🔧 Админка")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
