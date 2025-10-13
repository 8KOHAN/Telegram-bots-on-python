from aiogram import Router, types
from aiogram.filters import Command
from config import GOOGLE_CALENDAR_HTTPS

router = Router()

@router.message(Command("booking"))
async def handle_booking_button(message: types.Message):
    await message.answer(
        "To book an appointment, follow the link below:\n"
        f"[🔗 Go to Google Calendar]({GOOGLE_CALENDAR_HTTPS})",
        parse_mode="Markdown"
    )
