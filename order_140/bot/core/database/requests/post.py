from __future__ import annotations

from sqlalchemy import delete as sql_delete
from sqlalchemy import select as sql_select
from sqlalchemy import update as sql_update

from bot.core.database.models import PostModel


class Post:

    def __init__(self, session_pool) -> None:
        self._session_pool = session_pool

    async def get(self, post_id: int) -> PostModel | None:
        async with self._session_pool() as session:
            post = (await session.execute(
                sql_select(PostModel).where(PostModel.post_id == post_id)
            )).scalars().first()
            if post is None:
                return await self._create(post_id=None, session=session)
        return post

    async def _create(self, post_id, session) -> PostModel:
        new_post = PostModel(
            post_id=post_id,
        )
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post

    async def update(self, post_id: int, update_context: dict,) -> None:
        async with self._session_pool() as session:
            await session.execute(
                sql_update(PostModel).where(PostModel.post_id == post_id).values(
                    update_context
                )
            )
            await session.commit()

    async def delete(self, post_id: int) -> None:
        async with self._session_pool() as session:

            await session.execute(
                sql_delete(PostModel).where(PostModel.post_id == post_id)
            )
            await session.commit()

    async def get_all(self) -> list[PostModel]:
        async with self._session_pool() as session:
            return (await session.execute(sql_select(PostModel))
            ).scalars().all()
