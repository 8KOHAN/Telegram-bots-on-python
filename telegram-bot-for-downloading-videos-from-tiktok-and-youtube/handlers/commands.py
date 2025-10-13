from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import handlers.keyboards.inline_kp as in_kp
import handlers.function as hf
import url_storage as storage

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I can download a TikTok video using a link")

@router.message(lambda message: "tiktok.com" in message.text or "youtube.com" in message.text or "youtube.be" in message.text)
async def video_request(message: Message):
    url = message.text.strip()
    url_id = hf.generate_url_id(url)
    storage.url_storage[url_id] = url
    storage.save_url_storage(storage.url_storage)
    storage.url_storage = storage.load_url_storage()
    await message.answer("select download format: ", reply_markup = await in_kp.format_btn(url_id))
