from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import main_reply_kb

router = Router()

HELP_TEXT = (
    "👋 *Congratulations!*\n\n"
    "I am a virtual assistant to a laser hair removal master\n\n"
    "/start or /help — instructions on how to use the bot\n"
    "/booking — make an appointment via Google Calendar\n\n"
    "Write any question and I will be happy to answer it 😊"
)

@router.message(Command("start"))
@router.message(Command("help"))
async def handle_start(message: types.Message):
    await message.answer(HELP_TEXT, reply_markup=main_reply_kb, parse_mode="Markdown")
