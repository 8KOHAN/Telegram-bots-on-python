from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery

from handlers.function import download_and_media
import url_storage as storage

router = Router()

@router.callback_query(lambda callback: 'video' in callback.data or 'audio' in callback.data)
async def format_selection(callback: CallbackQuery, bot: Bot):
    storage.url_storage = storage.load_url_storage()
    action, url_id = callback.data.split("|")
    url = storage.url_storage.get(url_id)
    if not url:
        await callback.answer("Ошибка: URL не найден!")
        return
    await callback.answer("потверждено!")
    if action == "video":
        await callback.message.answer("начинаю загрузку видео")
        await download_and_media(bot, callback.message.chat.id, url, media_type='video')
    elif action == "audio":
        await callback.message.answer("начинаю загрузку аудио")
        await download_and_media(bot, callback.message.chat.id, url, media_type='audio')
