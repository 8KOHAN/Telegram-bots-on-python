from __future__ import annotations

from sqlalchemy import delete as sql_delete
from sqlalchemy import select as sql_select
from sqlalchemy import update as sql_update

from bot.core.database.models import ChannelModel


class Channel:

    def __init__(self, session_pool) -> None:
        self._session_pool = session_pool

    async def get(self, channel_id: int) -> ChannelModel | None:
        async with self._session_pool() as session:
            channel = (await session.execute(
                sql_select(ChannelModel).where(ChannelModel.channel_id == channel_id)
            )).scalars().first()
            if channel is None:
                return await self._create(channel_id=channel_id, session=session)
        return channel

    async def _create(self, channel_id: int, session) -> ChannelModel:
        new_channel = ChannelModel(
            channel_id=channel_id,
        )
        session.add(new_channel)
        await session.commit()
        return new_channel

    async def update(self, channel_id: int, update_context: dict,) -> None:
        async with self._session_pool() as session:
            await session.execute(
                sql_update(ChannelModel).where(ChannelModel.channel_id == channel_id).values(
                    update_context
                )
            )
            await session.commit()

    async def delete(self, channel_id: int) -> None:
        async with self._session_pool() as session:

            await session.execute(
                sql_delete(ChannelModel).where(ChannelModel.channel_id == channel_id)
            )
            await session.commit()

    async def get_all(self) -> list[ChannelModel]:
        async with self._session_pool() as session:
            return (await session.execute(sql_select(ChannelModel))
            ).scalars().all()
