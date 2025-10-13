from aiogram import Router, F
from aiogram.types import Message
from handlers.keyboards.reply_kp import user_reply_kb
from handlers.keyboards.inline_kp import category_buttons
from handlers.keyboards.admin_kp import admin_main_kb
from handlers.admin import ADMIN_IDS

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    is_admin = message.from_user.id in ADMIN_IDS
    await message.answer("Hello! Choose an action:", reply_markup=user_reply_kb(is_admin))

@router.message(F.text == "Categories")
async def show_categories(message: Message):
    await message.answer("Select a category:", reply_markup=category_buttons())

@router.message(F.text == "Support")
async def support_message(message: Message):
    await message.answer("Contact @telegram_name for communication")

@router.message(F.text == "🔧 Admin panel")
async def admin_access(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Welcome to the admin panel", reply_markup=admin_main_kb())
    else:
        await message.answer("⛔ You don't have access to the admin panel..")
