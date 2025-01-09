from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os
import urllib.parse


# Load environment variables from .env
load_dotenv()

# Get database credentials from environment variables
user = os.getenv("DB_USER")
raw_password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Encode the password to handle special characters
encoded_password = urllib.parse.quote_plus(raw_password).replace("%", "%%")

# Construct the database URL dynamically
sqlalchemy_url = f"postgresql://{user}:{encoded_password}@{host}/{db_name}"

# Alembic Config object, which provides access to the .ini file values
config = context.config

# Override the sqlalchemy.url value dynamically
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Import your metadata object here (from your models.py)
from app.models import db 
target_metadata = db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
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
