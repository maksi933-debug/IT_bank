from typing import Any

import pytest

from src.operations import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Фикстура с тестовым набором банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Перевод организации"},
        {"id": 5, "description": "перевод со счета на счет"},
        {"id": 6, "amount": 500},  # Операция без ключа description
        {"id": 7, "description": None},  # Операция с description=None
    ]


@pytest.mark.parametrize(
    ("search_query", "expected_ids"),
    [
        ("Перевод организации", [1, 4]),
        ("открытие вклада", [2]),  # Проверка регистронезависимости
        ("Перевод", [1, 3, 4, 5]),  # Поиск по частичному совпадению
        ("Покупка в магазине", []),  # Совпадений нет
        ("", [1, 2, 3, 4, 5]),  # Пустая строка поиска
    ],
)
def test_process_bank_search(
    sample_transactions: list[dict[str, Any]],
    search_query: str,
    expected_ids: list[int],
) -> None:
    """Тестирование поиска операций по строке в описании."""
    result = process_bank_search(sample_transactions, search_query)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_empty_data() -> None:
    """Тестирование поиска при пустом списке операций."""
    assert process_bank_search([], "Перевод") == []


def test_process_bank_operations(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование подсчета операций по заданным категориям."""
    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод со счета на счет",
        "Несуществующая категория",
    ]
    expected = {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Перевод со счета на счет": 1,
        "Несуществующая категория": 0,
    }
    assert process_bank_operations(sample_transactions, categories) == expected


def test_process_bank_operations_empty() -> None:
    """Тестирование подсчета при пустых входных данных."""
    assert process_bank_operations([], ["Перевод организации"]) == {"Перевод организации": 0}
    assert process_bank_operations([{"id": 1, "description": "Открытие вклада"}], []) == {}
