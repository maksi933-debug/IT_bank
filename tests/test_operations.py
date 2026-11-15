import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с набором тестовых банковских операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод организации"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": None},
        {"id": 6},  # Операция без ключа description
    ]


@pytest.mark.parametrize(
    ("search_query", "expected_ids"),
    [
        ("Перевод организации", [1, 3]),
        ("открытие вклада", [2]),  # Проверка регистронезависимости
        ("ПЕРЕВОД", [1, 3, 4]),    # Поиск по частичному совпадению
        ("Несуществующая", []),    # Ничего не найдено
    ],
)
def test_process_bank_search(
    sample_transactions: list[dict], search_query: str, expected_ids: list[int]
) -> None:
    """Тестирование поиска операций по строке описания."""
    result = process_bank_search(sample_transactions, search_query)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_empty_data() -> None:
    """Тестирование поиска при передаче пустого списка операций."""
    assert process_bank_search([], "Перевод") == []


def test_process_bank_operations(sample_transactions: list[dict]) -> None:
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
