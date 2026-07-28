from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date

# ==================== ТЕСТЫ FILTER_BY_STATE ====================


@pytest.mark.parametrize(
    "target_state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_state_success(
    sample_state_data: List[Dict[str, Any]], target_state: str, expected_ids: List[int]
) -> None:
    """Проверяет корректность фильтрации для различных значений статуса state."""
    result = filter_by_state(sample_state_data, state=target_state)
    assert len(result) == len(expected_ids)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default_argument(sample_state_data: List[Dict[str, Any]]) -> None:
    """Проверяет, что аргумент по умолчанию равен 'EXECUTED'."""
    result = filter_by_state(sample_state_data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


@pytest.mark.parametrize("non_existent_state", ["FAILED", "UNKNOWN", ""])
def test_filter_by_state_no_match(sample_state_data: List[Dict[str, Any]], non_existent_state: str) -> None:
    """Проверяет, что возвращается пустой список, если статус отсутствует."""
    result = filter_by_state(sample_state_data, state=non_existent_state)
    assert result == []


def test_filter_by_state_empty_list() -> None:
    """Проверяет поведение функции при передаче пустого списка данных."""
    assert filter_by_state([], state="EXECUTED") == []


# ==================== ТЕСТЫ SORT_BY_DATE ====================


def test_sort_by_date_order(sample_date_data: List[Dict[str, Any]]) -> None:
    """Тестирует сортировку по убыванию и возрастанию дат."""
    result_desc = sort_by_date(sample_date_data)
    assert [item["id"] for item in result_desc] == [3, 1, 2]

    result_asc = sort_by_date(sample_date_data, is_reverse=False)
    assert [item["id"] for item in result_asc] == [2, 1, 3]


def test_sort_by_date_identical_dates() -> None:
    """Проверяет корректность сортировки при одинаковых датах."""
    data = [
        {"id": 1, "date": "2026-05-20T10:00:00"},
        {"id": 2, "date": "2026-05-20T10:00:00"},
    ]
    result = sort_by_date(data)
    assert [item["id"] for item in result] == [1, 2]


@pytest.mark.parametrize(
    "invalid_data, expected_ids",
    [
        ([{"id": 1, "date": "2026-01-01"}, {"id": 2}], [1, 2]),
        ([{"id": 1, "date": "26-01-2026"}, {"id": 2, "date": "2026-01-26"}], [1, 2]),
    ],
)
def test_sort_by_date_invalid_formats(invalid_data: List[Dict[str, Any]], expected_ids: List[int]) -> None:
    """Тесты на некорректные и нестандартные форматы дат."""
    result = sort_by_date(invalid_data, is_reverse=True)
    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_type_error() -> None:
    """Критический случай: Смешанные типы данных (вызовет TypeError)."""
    mixed_data: List[Dict[str, Any]] = [{"id": 1, "date": "2026-01-01"}, {"id": 2, "date": 12345}]
    with pytest.raises(TypeError):
        sort_by_date(mixed_data)
