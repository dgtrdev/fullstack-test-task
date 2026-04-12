import os


def pytest_configure():
    os.environ.setdefault("POSTGRES_USER", "postgres")
    os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
    os.environ.setdefault("POSTGRES_DB", "test_test")
    os.environ.setdefault("POSTGRES_HOST", "backend-db")
    os.environ.setdefault("PGPORT", "5432")
    os.environ.setdefault("CELERY_BROKER_URL", "redis://backend-redis:6379/1")
    os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    os.environ.setdefault("STORAGE_DIR", "storage/test-files")
