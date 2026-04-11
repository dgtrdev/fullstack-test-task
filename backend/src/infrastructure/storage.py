from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from src.settings import settings


STORAGE_DIR = settings.storage_dir
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload_file: UploadFile, stored_name: str) -> int:
    content = await upload_file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    get_stored_file_path(stored_name).write_bytes(content)
    return len(content)


def get_stored_file_path(stored_name: str) -> Path:
    return STORAGE_DIR / stored_name


def delete_stored_file(stored_name: str) -> None:
    stored_path = get_stored_file_path(stored_name)
    if stored_path.exists():
        stored_path.unlink()


def get_existing_file_path(stored_name: str) -> Path:
    stored_path = get_stored_file_path(stored_name)
    if not stored_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")

    return stored_path
