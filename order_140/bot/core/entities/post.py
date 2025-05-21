from bot.core.database import Database
from bot.core.database.models import PostModel
from bot.core.database.requests import post


class Post:

    def __init__(
            self,
            post_id: int,
            channel_id: int,
            creator_id: int,
            timer_delete: int,
            content: dict,
            database: Database
    ) -> None:

        self.post_id: int = post_id
        self.channel_id: int = channel_id
        self.creator_id: int = creator_id
        self.timer_delete: int = timer_delete
        self.content: dict = content
        self._database = database

    @property
    def data(self) -> dict:
        return {
            PostModel.post_id: self.post_id,
            PostModel.channel_id: self.channel_id,
            PostModel.creator_id: self.creator_id,
            PostModel.timer_delete: self.timer_delete,
            PostModel.content: self.content
        }

    async def commit(self) -> None:
        await self._database.post.update(post_id=self.post_id, update_context=self.data)

    async def delete(self) -> None:
        await self._database.post.delete(post_id=self.post_id)

    @classmethod
    async def from_database(cls, post_id, database: Database) -> "Post | None":
        post_model = await database.post.get(post_id=post_id)
        return cls(
            post_id=post_model.post_id,
            channel_id=post_model.channel_id,
            creator_id=post_model.creator_id,
            timer_delete=post_model.timer_delete,
            content=post_model.content,
            database=database
        )

    @classmethod
    async def all_from_database(cls, database: Database) -> list["Post"]:
        post_models = await database.post.get_all()
        return [Post(
            post_id=post_model.post_id,
            channel_id=post_model.channel_id,
            creator_id=post_model.creator_id,
            timer_delete=post_model.timer_delete,
            content=post_model.content,
            database=database
        ) for post_model in post_models]
