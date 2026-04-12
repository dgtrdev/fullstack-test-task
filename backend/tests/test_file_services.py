import pytest
from fastapi import HTTPException

from src.services.alerts import list_alerts
from src.services.files import create_file, delete_file, get_file, list_files


class FakeUploadFile:
    def __init__(
        self,
        *,
        filename: str,
        content: bytes,
        content_type: str = "text/plain",
    ) -> None:
        self.filename = filename
        self.content_type = content_type
        self._content = content

    async def read(self) -> bytes:
        return self._content


async def create_test_file(title: str):
    return await create_file(
        title=title,
        upload_file=FakeUploadFile(filename=f"{title}.txt", content=b"content"),
    )


@pytest.mark.asyncio
async def test_list_files_returns_paginated_active_files(reset_database):
    await create_test_file("first")
    await create_test_file("second")
    await create_test_file("third")

    files, total = await list_files(limit=2, offset=0)

    assert total == 3
    assert len(files) == 2


@pytest.mark.asyncio
async def test_delete_file_soft_deletes_file_and_creates_alert(reset_database):
    file_item = await create_test_file("deleted")

    await delete_file(file_item.id)

    with pytest.raises(HTTPException) as error:
        await get_file(file_item.id)

    assert error.value.status_code == 404

    files, files_total = await list_files(limit=10, offset=0)
    alerts, alerts_total = await list_alerts(limit=10, offset=0)

    assert files == []
    assert files_total == 0
    assert alerts_total == 1
    assert alerts[0].file_id == file_item.id
    assert alerts[0].level == "info"
    assert alerts[0].message == "File deleted"
