from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi import Query
from fastapi.responses import FileResponse

from src.schemas import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, FileItem, FileListResponse, FileUpdate, normalize_file_title
from src.services.files import create_file, delete_file, get_file, get_file_path, list_files, update_file
from src.tasks import scan_file_for_threats


router = APIRouter()


@router.get("/files", response_model=FileListResponse)
async def list_files_view(
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_LIMIT)] = DEFAULT_PAGE_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    files, total = await list_files(limit=limit, offset=offset)
    return FileListResponse(
        items=[FileItem.model_validate(file_item) for file_item in files],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/files", response_model=FileItem, status_code=201)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        normalized_title = normalize_file_title(title)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    file_item = await create_file(title=normalized_title, upload_file=file)
    scan_file_for_threats.delay(file_item.id)
    return file_item


@router.get("/files/{file_id}", response_model=FileItem)
async def get_file_view(file_id: str):
    return await get_file(file_id)


@router.patch("/files/{file_id}", response_model=FileItem)
async def update_file_view(
    file_id: str,
    payload: FileUpdate,
):
    return await update_file(file_id=file_id, title=payload.title)


@router.get("/files/{file_id}/download")
async def download_file(file_id: str):
    file_item, stored_path = await get_file_path(file_id)
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )


@router.delete("/files/{file_id}", status_code=204)
async def delete_file_view(file_id: str):
    await delete_file(file_id)
