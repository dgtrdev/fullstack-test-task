import pytest

from src.schemas import MAX_FILE_TITLE_LENGTH, normalize_file_title


def test_normalize_file_title_trims_spaces():
    assert normalize_file_title("  Договор  ") == "Договор"


@pytest.mark.parametrize("title", ["", "   "])
def test_normalize_file_title_rejects_empty_value(title):
    with pytest.raises(ValueError, match="Название файла не может быть пустым"):
        normalize_file_title(title)


def test_normalize_file_title_rejects_too_long_value():
    title = "a" * (MAX_FILE_TITLE_LENGTH + 1)

    with pytest.raises(ValueError, match="Название файла не может быть длиннее"):
        normalize_file_title(title)
