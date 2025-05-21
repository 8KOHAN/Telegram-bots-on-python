from __future__ import annotations

from sqlalchemy import delete as sql_delete
from sqlalchemy import select as sql_select
from sqlalchemy import update as sql_update

from bot.core.database.models import AdminModel


class Admin:

    def __init__(self, session_pool) -> None:
        self._session_pool = session_pool

    async def get(self, user_id: int) -> AdminModel | None:
        async with self._session_pool() as session:
            return (await session.execute(
                sql_select(AdminModel).where(AdminModel.user_id == user_id)
            )).scalars().first()

    async def create(
            self,
            user_id: int,

    ) -> AdminModel:
        async with self._session_pool() as session:
            new_admin = AdminModel(
                user_id=user_id,
            )
            session.add(new_admin)
            await session.commit()
        return new_admin

    async def update(self, user_id: int, update_context: dict) -> None:
        async with self._session_pool() as session:
            await session.execute(
                sql_update(AdminModel).where(AdminModel.user_id == user_id).values(
                    update_context
                )
            )
            await session.commit()

    async def delete(self, user_id: int) -> None:
        async with self._session_pool() as session:
            await session.execute(
                sql_delete(AdminModel).where(AdminModel.user_id == user_id)
            )
            await session.commit()

    async def get_all(self) -> list[AdminModel]:
        async with self._session_pool() as session:
            return (await session.execute(sql_select(AdminModel))
            ).scalars().all()
