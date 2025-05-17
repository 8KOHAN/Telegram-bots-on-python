from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def format_btn(url_id):
    keybord = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="видео", callback_data=f"video|{url_id}"), InlineKeyboardButton(text="аудио", callback_data=f"audio|{url_id}")]
    ])
    return keybord
