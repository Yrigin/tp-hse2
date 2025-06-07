import pytest
from src.media_indexing.folder_index import get_artist  


@pytest.mark.parametrize(
    "input_str, expected",
    [
        # Happy path - один артист
        ("[artist name]", "Artist Name"),
        ("[The Beatles]", "The Beatles"),
        ("[some ARTIST]", "Some Artist"),
        ("[multiple words artist]", "Multiple Words Artist"),
        # Без артиста
        ("no artist here", None),
        ("", None),
        # Разные регистры
        ("[LoWeRcAsE]", "Lowercase"),
        ("[UPPERCASE]", "Uppercase"),
        ("[MiXeD CaSe]", "Mixed Case"),
    ],
)
def test_get_artist_valid_cases(input_str, expected):
    assert get_artist(input_str) == expected


@pytest.mark.parametrize(
    "input_str, expected_exception",
    [
        # Несколько артистов
        ("[artist1][artist2]", ValueError),
        ("[first] [second]", ValueError),
        # Неправильные скобки
        ("[unclosed", None),  # Возвращает None, так как нет закрывающей скобки
        ("unopened]", None),   # Возвращает None, так как нет открывающей скобки
    ],
)
def test_get_artist_error_cases(input_str, expected_exception):
    if expected_exception is None:
        assert get_artist(input_str) is None
    else:
        with pytest.raises(expected_exception):
            get_artist(input_str)


# def test_get_artist_with_various_artists():
#     # Если у вас есть специальная обработка для VARIOUS_ARTISTS_NAME
#     from your_module import VARIOUS_ARTISTS_NAME
#     assert get_artist(f"[{VARIOUS_ARTISTS_NAME}]") == VARIOUS_ARTISTS_NAME


# # Дополнительные тесты для проверки обработки специальных символов
# @pytest.mark.parametrize(
#     "input_str, expected",
#     [
#         ("[artist with numbers 123]", "Artist With Numbers 123"),
#         ("[artist with !@#$% symbols]", "Artist With !@#$% Symbols"),
#         ("[artist with - hyphen]", "Artist With - Hyphen"),
#         ("[artist with _ underscore]", "Artist With _ Underscore"),
#     ],
# )
# def test_get_artist_special_chars(input_str, expected):
#     assert get_artist(input_str) == expected