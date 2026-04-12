import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select

from src.db import async_session_maker
from src.infrastructure.storage import delete_stored_file, get_existing_file_path, save_upload_file
from src.models import StoredFile


async def list_files(limit: int, offset: int) -> tuple[list[StoredFile], int]:
    async with async_session_maker() as session:
        total = await session.scalar(select(func.count()).select_from(StoredFile))
        result = await session.execute(
            select(StoredFile).order_by(StoredFile.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all()), total or 0


async def get_file(file_id: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return file_item


async def create_file(title: str, upload_file: UploadFile) -> StoredFile:
    file_id = str(uuid4())
    suffix = Path(upload_file.filename or "").suffix
    stored_name = f"{file_id}{suffix}"
    file_size = await save_upload_file(upload_file=upload_file, stored_name=stored_name)

    file_item = StoredFile(
        id=file_id,
        title=title,
        original_name=upload_file.filename or stored_name,
        stored_name=stored_name,
        mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
        size=file_size,
        processing_status="uploaded",
    )
    async with async_session_maker() as session:
        session.add(file_item)
        await session.commit()
        await session.refresh(file_item)
    return file_item


async def update_file(file_id: str, title: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        file_item.title = title
        await session.commit()
        await session.refresh(file_item)
        return file_item


async def delete_file(file_id: str) -> None:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        delete_stored_file(file_item.stored_name)
        await session.delete(file_item)
        await session.commit()


async def get_file_path(file_id: str) -> tuple[StoredFile, Path]:
    file_item = await get_file(file_id)
    stored_path = get_existing_file_path(file_item.stored_name)
    return file_item, stored_path
