from sqlalchemy import func, select

from src.db import async_session_maker
from src.models import Alert


async def list_alerts(limit: int, offset: int) -> tuple[list[Alert], int]:
    async with async_session_maker() as session:
        total = await session.scalar(select(func.count()).select_from(Alert))
        result = await session.execute(select(Alert).order_by(Alert.created_at.desc()).limit(limit).offset(offset))
        return list(result.scalars().all()), total or 0


async def create_alert(file_id: str, level: str, message: str) -> Alert:
    alert = Alert(file_id=file_id, level=level, message=message)
    async with async_session_maker() as session:
        session.add(alert)
        await session.commit()
        await session.refresh(alert)
        return alert
