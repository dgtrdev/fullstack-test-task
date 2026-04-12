import os
import shutil

import asyncpg
import pytest_asyncio


TEST_DATABASE = "test_test"


os.environ.update(
    {
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_DB": TEST_DATABASE,
        "POSTGRES_HOST": "backend-db",
        "PGPORT": "5432",
        "CELERY_BROKER_URL": "redis://backend-redis:6379/1",
        "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
        "STORAGE_DIR": "storage/test-files",
    }
)

from src.db import engine
from src.models import Base
from src.settings import settings


async def ensure_test_database_exists() -> None:
    connection = await asyncpg.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["PGPORT"]),
        database="postgres",
    )
    try:
        database_exists = await connection.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            TEST_DATABASE,
        )
        if not database_exists:
            await connection.execute(f'CREATE DATABASE "{TEST_DATABASE}"')
    finally:
        await connection.close()


@pytest_asyncio.fixture
async def reset_database():
    await ensure_test_database_exists()
    shutil.rmtree(settings.storage_dir, ignore_errors=True)
    settings.storage_dir.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    shutil.rmtree(settings.storage_dir, ignore_errors=True)
