from os import getenv
from pytz import timezone

__import__("dotenv").load_dotenv()


class Configuration:

    bot_token: str = getenv("BOT_TOKEN")

    database_connection: str = "{engine_url}://{user}:{password}@{host}/{database_name}".format(
        engine_url="postgresql+asyncpg",
        user=getenv('DATABASE_USER'),
        password=getenv('DATABASE_PASSWORD'),
        host=getenv('DATABASE_HOST'),
        database_name=getenv('DATABASE_NAME'),
    )

    time_zone = timezone(zone='Europe/Kyiv')
