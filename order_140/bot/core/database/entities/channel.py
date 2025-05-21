from bot.core.database import Database
from bot.core.database.models import ChannelModel


class Channel:

    def __init__(
            self,
            channel_id: int,
            username: str,
            full_name: str,
            database: Database
    ) -> None:

        self.channel_id: int = channel_id
        self.username: str = username
        self.full_name: str = full_name
        self._database = database

    @property
    def data(self) -> dict:
        return {
            ChannelModel.username: self.username,
            ChannelModel.full_name: self.full_name,
        }

    async def commit(self) -> None:
        await self._database.channel.update(channel_id=self.channel_id, update_context=self.data)

    async def delete(self) -> None:
        await self._database.channel.delete(channel_id=self.channel_id)

    @classmethod
    async def from_database(cls, channel_id: int, database: Database) -> "Channel | None":
        channel_model = await database.channel.get(channel_id=channel_id)
        return cls(
            channel_id=channel_model.channel_id,
            username=channel_model.username,
            full_name=channel_model.full_name,
            database=database
        )

    @classmethod
    async def all_from_database(cls, database: Database) -> list["Channel"]:
        channel_models = await database.channel.get_all()
        return [Channel(
            channel_id=channel_model.channel_id,
            username=channel_model.username,
            full_name=channel_model.full_name,
            database=database
        ) for channel_model in channel_models]
