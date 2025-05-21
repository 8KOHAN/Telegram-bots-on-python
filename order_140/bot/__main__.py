import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.core.configuration import Configuration
from bot.core.database import Database
from bot.middlewares import setup_middlewares
from bot.routers import setup_routers

# setup dispatcher and logging
logging.basicConfig(level=logging.INFO)


async def main():

    dispatcher = Dispatcher()

    bot = Bot(Configuration.bot_token, parse_mode="html")

    # setup routers
    setup_routers(dispatcher=dispatcher)
    setup_middlewares(dispatcher=dispatcher)
    # -
    database_ = Database()
    # start polling
    await dispatcher.start_polling(
        bot,
        database_=database_,
        allowed_updates=dispatcher.resolve_used_update_types()
    )


if __name__ == "__main__":
    asyncio.run(main())
