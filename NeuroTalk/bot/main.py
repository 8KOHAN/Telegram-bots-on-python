import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import base, booking, start

load_dotenv()

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не заданий у .env")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(booking.router)
    dp.include_router(base.router)

    print("🤖 Бот запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Зупинка бота")
