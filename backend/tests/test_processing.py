from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from src.db import async_session_maker
from src.models import Alert, StoredFile
from src.services.processing import check_file_safety, create_processing_alert, get_file_metadata, get_safety_reasons


@pytest.mark.asyncio
async def test_processing_skips_deleted_file(reset_database):
    async with async_session_maker() as session:
        file_item = StoredFile(
            id="deleted-file-id",
            title="Deleted document",
            original_name="document.txt",
            stored_name="deleted-file-id.txt",
            mime_type="text/plain",
            size=1024,
            processing_status="uploaded",
            deleted_at=datetime.now(UTC),
        )
        session.add(file_item)
        await session.commit()

    await check_file_safety(file_item.id)
    await get_file_metadata(file_item.id)
    await create_processing_alert(file_item.id)

    async with async_session_maker() as session:
        stored_file = await session.get(StoredFile, file_item.id)
        alerts = list(await session.scalars(select(Alert).where(Alert.file_id == file_item.id)))

    assert stored_file is not None
    assert stored_file.processing_status == "uploaded"
    assert stored_file.scan_status is None
    assert stored_file.metadata_json is None
    assert alerts == []


def make_file(
    *,
    original_name: str = "document.txt",
    mime_type: str = "text/plain",
    size: int = 1024,
) -> StoredFile:
    return StoredFile(
        id="file-id",
        title="Document",
        original_name=original_name,
        stored_name="file-id.txt",
        mime_type=mime_type,
        size=size,
        processing_status="uploaded",
    )


def test_get_safety_reasons_detects_suspicious_extension():
    reasons = get_safety_reasons(make_file(original_name="installer.exe"))

    assert "suspicious extension .exe" in reasons


def test_get_safety_reasons_detects_large_file():
    reasons = get_safety_reasons(make_file(size=11 * 1024 * 1024))

    assert "file is larger than 10 MB" in reasons


def test_get_safety_reasons_detects_pdf_mime_mismatch():
    reasons = get_safety_reasons(make_file(original_name="contract.pdf", mime_type="text/plain"))

    assert "pdf extension does not match mime type" in reasons


def test_get_safety_reasons_returns_empty_list_for_safe_file():
    assert get_safety_reasons(make_file()) == []
