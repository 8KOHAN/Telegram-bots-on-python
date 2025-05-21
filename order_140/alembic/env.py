import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.core.database.models import Base


config = context.config

DB_ENGINE = os.getenv("DATABASE_ENGINE")   
DB_HOST = os.getenv("DATABASE_HOST") 
DB_USER = os.getenv("DATABASE_USER")      
DB_PASS = os.getenv("DATABASE_PASSWORD")         
DB_NAME = os.getenv("DATABASE_NAME")     

sync_DB_ENGINE = DB_ENGINE.replace("asyncpg", "psycopg2")
DATABASE_URL = f"{sync_DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
