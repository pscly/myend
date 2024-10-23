from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 导入您的模型
from entities.models import Base
# from models import Base

# 新增：导入必要的模块来读取 YAML 配置文件
import os
from utils.factory import load_conf

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置 target_metadata
target_metadata = Base.metadata

# 修改：从配置文件中获取数据库 URL
def get_url():
    # 获取当前环境
    mode = os.environ.get("MODE", "DEVELOPMENT").upper()
    # 读取配置文件
    yaml_config = load_conf(mode, "config.yaml")
    # 获取对应环境的数据库 URL
    config.set_main_option("sqlalchemy.url", yaml_config["SQLALCHEMY_DATABASE_URI"])
    return yaml_config["SQLALCHEMY_DATABASE_URI"]

get_url()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
