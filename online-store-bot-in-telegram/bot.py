import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import callback, commands, admin

async def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(callback.router)
    dp.include_router(admin.router)

    print("bot start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
