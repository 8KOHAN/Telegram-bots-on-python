from bot.core.database import Database
from bot.core.database.models import AdminModel


class Admin:

    def __init__(
            self,
            user_id: int,
            username: str | None,
            full_name: str,
            database: Database
    ) -> None:

        self.user_id: int = user_id
        self.username: str | None = username
        self.full_name: str = full_name
        self._database = database

    @property
    def data(self) -> dict:
        return {
            AdminModel.username: self.username,
            AdminModel.full_name: self.full_name,
        }

    async def commit(self) -> None:
        await self._database.admin.update(user_id=self.user_id, update_context=self.data)

    async def delete(self) -> None:
        await self._database.admin.delete(user_id=self.user_id)

    @classmethod
    async def create(cls, user_id: int, database: Database) -> "Admin | None":
        admin_model = await database.admin.create(user_id=user_id)
        return cls(
            user_id=admin_model.user_id,
            username=admin_model.username,
            full_name=admin_model.full_name,
            database=database
        )

    @classmethod
    async def from_database(cls, user_id: int, database: Database) -> "Admin | None":
        admin_model = await database.admin.get(user_id=user_id)
        if admin_model is None:
            return
        return cls(
            user_id=admin_model.user_id,
            username=admin_model.username,
            full_name=admin_model.full_name,
            database=database
        )

    @classmethod
    async def all_from_database(cls, database: Database) -> list["Admin"]:
        admin_models = await database.admin.get_all()
        return [Admin(
            user_id=admin_model.user_id,
            username=admin_model.username,
            full_name=admin_model.full_name,
            database=database
        ) for admin_model in admin_models]
    
