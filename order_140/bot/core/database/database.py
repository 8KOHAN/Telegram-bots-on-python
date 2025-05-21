from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.core.configuration import Configuration

from .requests import Admin, Channel, Post


class Database:

    def __init__(self) -> None:
        self._session_pool = sessionmaker(
            create_async_engine(Configuration.database_connection),
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.admin = Admin(session_pool=self._session_pool)
        self.channel = Channel(session_pool=self._session_pool)
        self.post = Post(session_pool=self._session_pool)
