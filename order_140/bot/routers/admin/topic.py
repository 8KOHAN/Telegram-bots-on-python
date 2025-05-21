from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from core.database.requests.topic import save_topic
from core.database.session import get_session

router = Router()

@router.message(Command("register_topic"))
async def register_topic_handler(message: Message):
    topic_id = message.message_thread_id
    chat_id = message.chat.id

    if topic_id is None:
        await message.answer("Цю команду потрібно використовувати у темі (гілці) форуму.")
        return

    async with get_session() as session:
        await save_topic(session, chat_id, topic_id)

    await message.answer("Тему успішно зареєстровано ✅")
