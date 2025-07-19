from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import main_reply_kb

router = Router()

HELP_TEXT = (
    "👋 *Вітаю!*\n\n"
    "Я — віртуальний асистент майстра лазерної епіляції.\n\n"
    "/start або /help — інструкція щодо використання бота\n"
    "/booking — записатися на прийом через Google Календар\n\n"
    "Пишіть будь-яке запитання — і я з радістю відповім 😊"
)

@router.message(Command("start"))
@router.message(Command("help"))
async def handle_start(message: types.Message):
    await message.answer(HELP_TEXT, reply_markup=main_reply_kb, parse_mode="Markdown")
