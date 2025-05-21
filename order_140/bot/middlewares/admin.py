from typing import Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser

from bot.core.database import Database
from bot.core.entities import Admin


class AdminMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: [[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        # get data from event
        event_user: TelegramUser = data["event_from_user"]
        database: Database = data["database_"]

        # get admin from the database
        admin = await Admin.from_database(user_id=event_user.id, database=database)

        # check if user is admin
        if admin is None:
            return

        # update data and return handler
        data["admin_"] = admin
        return await handler(event, data)
