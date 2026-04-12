from typing import Annotated

from fastapi import APIRouter
from fastapi import Query

from src.schemas import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, AlertItem, AlertListResponse
from src.services.alerts import list_alerts


router = APIRouter()


@router.get("/alerts", response_model=AlertListResponse)
async def list_alerts_view(
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_LIMIT)] = DEFAULT_PAGE_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    alerts, total = await list_alerts(limit=limit, offset=offset)
    return AlertListResponse(
        items=[AlertItem.model_validate(alert) for alert in alerts],
        total=total,
        limit=limit,
        offset=offset,
    )
