"""Environment module for Alembic."""

import logging.config
import os

import sqlalchemy as sqla
from alembic import context
from sqlmodel import SQLModel

if os.environ.get("ALEMBIC_CONFIGURE_LOGGING", "true") == "true":
    logging.config.fileConfig(context.config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine. Calls to context.execute()
    here emit the given string to the script output.
    """
    context.configure(
        url=os.environ.get("DB_URL", "postgresql://127.0.0.1:5432/db"),
        dialect_opts={"paramstyle": "named"},
        target_metadata=SQLModel.metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    url = os.environ.get("DB_URL", "postgresql://postgres:password@127.0.0.1:5432/klm")
    engine_kwargs = {
        "connect_args": {"connect_timeout": 10},
        "poolclass": sqla.pool.NullPool,
    }
    engine = sqla.create_engine(url, **engine_kwargs)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=SQLModel.metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
