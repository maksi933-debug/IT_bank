from typing import Any

import pytest

from src.operations import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Фикстура с набором тестовых банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод организации"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": None},
        {"id": 6},
    ]


@pytest.mark.parametrize(
    ("search_query", "expected_ids"),
    [
        ("Перевод организации", [1, 3]),
        ("открытие вклада", [2]),
        ("ПЕРЕВОД", [1, 3, 4]),
        ("Несуществующая", []),
    ],
)
def test_process_bank_search(
    sample_transactions: list[dict[str, Any]], search_query: str, expected_ids: list[int]
) -> None:
    """Тестирование поиска операций по строке описания."""
    result = process_bank_search(sample_transactions, search_query)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_empty_data() -> None:
    """Тестирование поиска при передаче пустого списка операций."""
    assert process_bank_search([], "Перевод") == []


def test_process_bank_operations(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование подсчета операций по заданным категориям."""
    categories = ["Перевод организации", "Открытие вклада", "Оплата услуг"]
    expected = {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Оплата услуг": 0,
    }
    assert process_bank_operations(sample_transactions, categories) == expected


def test_process_bank_operations_empty() -> None:
    """Тестирование подсчета при пустом списке транзакций или категорий."""
    assert process_bank_operations([], ["Открытие вклада"]) == {"Открытие вклада": 0}
    assert process_bank_operations([{"description": "Открытие вклада"}], []) == {}
