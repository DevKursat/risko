from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.db.session import Base
# Ensure models are imported so they are registered on the Base.metadata for autogenerate
# Prefer importing backend-specific module path to avoid duplicate top-level app package imports
try:
    from backend.app.models.analysis import Analysis  # noqa: F401
except Exception:
    from app.models.analysis import Analysis  # noqa: F401


target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url') or os.environ.get('DATABASE_URL')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = configuration.get('sqlalchemy.url') or os.environ.get('DATABASE_URL')
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
