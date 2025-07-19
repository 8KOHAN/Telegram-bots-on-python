from aiogram import Router, types
from aiogram.filters import Command
from config import GOOGLE_CALENDAR_HTTPS

router = Router()

@router.message(Command("booking"))
async def handle_booking_button(message: types.Message):
    await message.answer(
        "Щоб забронювати час, перейдіть за посиланням нижче:\n"
        f"[🔗 Перейти в Google Календар]({GOOGLE_CALENDAR_HTTPS})",
        parse_mode="Markdown"
    )
