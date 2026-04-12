from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


MAX_FILE_TITLE_LENGTH = 255
DEFAULT_PAGE_LIMIT = 10
MAX_PAGE_LIMIT = 100


def normalize_file_title(title: str) -> str:
    normalized_title = title.strip()
    if not normalized_title:
        raise ValueError("Название файла не может быть пустым")
    if len(normalized_title) > MAX_FILE_TITLE_LENGTH:
        raise ValueError(f"Название файла не может быть длиннее {MAX_FILE_TITLE_LENGTH} символов")

    return normalized_title


class FileItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    original_name: str
    mime_type: str
    size: int
    processing_status: str
    scan_status: str | None
    scan_details: str | None
    metadata_json: dict | None
    requires_attention: bool
    created_at: datetime
    updated_at: datetime


class FileUpdate(BaseModel):
    title: str = Field(..., max_length=MAX_FILE_TITLE_LENGTH)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return normalize_file_title(value)


class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: str
    level: str
    message: str
    created_at: datetime


class FileListResponse(BaseModel):
    items: list[FileItem]
    total: int
    limit: int
    offset: int


class AlertListResponse(BaseModel):
    items: list[AlertItem]
    total: int
    limit: int
    offset: int
