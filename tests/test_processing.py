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


def test_filter_by_state_missing_key() -> None:
    """Проверяет устойчивость к отсутствию ключа 'state' в некоторых элементах списка."""
    mixed_data: list[dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},  # Ключ отсутствует
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(mixed_data, "EXECUTED")
    assert len(result) == 2


def test_filter_by_state_case_sensitivity() -> None:
    """Проверяет, как функция реагирует на разный регистр букв в статусе state."""
    data = [
        {"id": 1, "state": "executed"},
        {"id": 2, "state": "EXECUTED"},
    ]
    result = filter_by_state(data, state="EXECUTED")
    assert [item["id"] for item in result] == [2]


def test_filter_by_state_invalid_input_types() -> None:
    """Проверяет поведение при передаче невалидных типов вместо ожидаемой строки в state.
    Поскольку используется метод ==, код не упадет, а просто вернет пустой список.
    """
    data = [{"id": 1, "state": "EXECUTED"}]
    """ Передаем список, число или None вместо строки в аргумент state"""
    # Сравниваем результат с пустым списком == [], чтобы assert не падал на False
    assert filter_by_state(data, state=123) == []  # type: ignore


def test_filter_by_state_elements_are_not_dicts() -> None:
    """Критическая ошибка данных: если в списке data лежат не словари, а другие типы.
    У них нет метода .get(), поэтому код должен упасть с AttributeError.
    """
    bad_data = [
        {"id": 1, "state": "EXECUTED"},
        "я строка, а не словарь",
    ]
    with pytest.raises(AttributeError):
        filter_by_state(bad_data)  # type: ignore


def test_filter_by_state_branch_coverage() -> None:
    """Проверяет обе ветки условия внутри генератора списков (выполняется/пропускается)."""
    mixed_data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    result = filter_by_state(mixed_data, state="EXECUTED")
    assert len(result) == 1


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
    """Проверяет вызов TypeError при сравнении строки и числа."""
    mixed_data = [{"id": 1, "date": "2026-01-01"}, {"id": 2, "date": 12345}]
    with pytest.raises(TypeError):
        sort_by_date(mixed_data)  # type: ignore


def test_sort_by_date_completely_missing_keys() -> None:
    """Проверяет сортировку элементов, в которых вообще нет ключа 'date'."""
    data = [
        {"id": 1},
        {"id": 2},
    ]
    result = sort_by_date(data)
    assert len(result) == 2


def test_sort_by_date_empty_list() -> None:
    """Проверяет поведение функции сортировки при передаче пустого списка."""
    assert sort_by_date([]) == []


def test_sort_by_date_does_not_mutate_original_list(sample_date_data: List[Dict[str, Any]]) -> None:
    """Проверяет, что функция возвращает новый список и не изменяет (не мутирует) исходный."""
    original_copy = sample_date_data.copy()
    sort_by_date(sample_date_data)
    assert sample_date_data == original_copy


def test_sort_by_date_all_elements_missing_date() -> None:
    """Критический случай: у всех элементов отсутствует ключ 'date'.
    Код вернет пустые строки для всех, и список останется в исходном порядке.
    """
    data = [{"id": 3}, {"id": 1}, {"id": 2}]
    result = sort_by_date(data, is_reverse=True)
    assert [item["id"] for item in result] == [3, 1, 2]


@pytest.mark.parametrize(
    "corrupted_data",
    [
        [{"id": 1, "date": None}],
        [{"id": 1, "date": []}],
        [{"id": 1, "date": {"year": 2026}}],
    ],
)
def test_sort_by_date_invalid_types_in_key(corrupted_data: List[Dict[str, Any]]) -> None:
    """Проверяет, что передача неподдерживаемых для сравнения со строкой типов
    (None, list, dict) вызывает TypeError при попытке сортировки с дефолтной строкой.
    """
    corrupted_data.append({"id": 2, "date": "2026-01-01"})
    with pytest.raises(TypeError):
        sort_by_date(corrupted_data)


def test_sort_by_date_with_boolean_date() -> None:
    """Особый случай в Python: bool является подтипом int (True == 1, False == 0).
    Сравнение строки и bool вызовет TypeError."""
    data = [{"id": 1, "date": "2026-01-01"}, {"id": 2, "date": True}]
    with pytest.raises(TypeError):
        sort_by_date(data)  # type: ignore


def test_sort_by_date_elements_are_not_dicts() -> None:
    """Если в sort_by_date придет список строк вместо словарей,
    лямбда-функция вызовет AttributeError при попытке вызвать .get().
    """
    bad_data = ["2026-01-01", "2026-01-02"]
    with pytest.raises(AttributeError):
        sort_by_date(bad_data)  # type: ignore


def test_filter_and_sort_huge_ids() -> None:
    """Проверка работы с экстремально большими числами (overflow check) в id,
    чтобы убедиться, что python-типы их переваривают."""
    huge_data = [{"id": 999999999999999999999999999, "state": "EXECUTED", "date": "2026-01-01"}]
    assert len(filter_by_state(huge_data)) == 1
    assert len(sort_by_date(huge_data)) == 1
