import pytest

from src.db import async_session_maker
from src.models import Alert, StoredFile
from src.services.alerts import list_alerts


@pytest.mark.asyncio
async def test_list_alerts_returns_paginated_alerts(reset_database):
    async with async_session_maker() as session:
        file_item = StoredFile(
            id="file-id",
            title="Document",
            original_name="document.txt",
            stored_name="document.txt",
            mime_type="text/plain",
            size=100,
            processing_status="processed",
        )
        session.add(file_item)
        await session.commit()

    async with async_session_maker() as session:
        session.add_all(
            [
                Alert(file_id=file_item.id, level="info", message="First"),
                Alert(file_id=file_item.id, level="warning", message="Second"),
                Alert(file_id=file_item.id, level="critical", message="Third"),
            ]
        )
        await session.commit()

    alerts, total = await list_alerts(limit=2, offset=0)

    assert total == 3
    assert len(alerts) == 2
