from src.models import StoredFile
from src.services.processing import get_safety_reasons


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
