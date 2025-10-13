from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def category_buttons():
    keyboard = [
        [InlineKeyboardButton(text="🖥 Computers", callback_data="category:computers")],
        [InlineKeyboardButton(text="📱 Phones", callback_data="category:phones")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
