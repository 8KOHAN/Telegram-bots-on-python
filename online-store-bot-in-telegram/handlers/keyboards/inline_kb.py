from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def category_buttons():
    keyboard = [
        [InlineKeyboardButton(text="🖥 Компьютеры", callback_data="category:computers")],
        [InlineKeyboardButton(text="📱 Телефоны", callback_data="category:phones")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
