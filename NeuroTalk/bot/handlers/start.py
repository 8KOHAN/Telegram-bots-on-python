from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer("Вітаю! Я віртуальний менеджер майстра лазерної епіляції. Готовий відповісти на ваші запитання або допомогти з записом 🌸")
