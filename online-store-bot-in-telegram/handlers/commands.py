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
    await message.answer("Привет! Выберите действие:", reply_markup=user_reply_kb(is_admin))

@router.message(F.text == "Категории")
async def show_categories(message: Message):
    await message.answer("Выберите категорию:", reply_markup=category_buttons())

@router.message(F.text == "Поддержка")
async def support_message(message: Message):
    await message.answer("Обратитесь в @Alexeikohan для связи.")

@router.message(F.text == "🔧 Админка")
async def admin_access(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Добро пожаловать в админ-панель", reply_markup=admin_main_kb())
    else:
        await message.answer("⛔ У вас нет доступа к админ-панели.")
