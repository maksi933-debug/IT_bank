from types import GeneratorType
from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# ТЕСТИРОВАНИЕ filter_by_currency


def test_filter_by_currency_with_fixture(
    raw_transactions: list[dict[str, Any]], currency_scenario: dict[str, Any]
) -> None:
    """Тест проверяет фильтрацию транзакций по сценариям из conftest."""
    target_currency = currency_scenario["currency"]
    expected_ids = currency_scenario["expected_ids"]

    result_gen = filter_by_currency(raw_transactions, target_currency)

    assert isinstance(result_gen, GeneratorType), "Функция должна возвращать генератор"

    result_ids = [tx["id"] for tx in result_gen]
    assert sorted(result_ids) == sorted(expected_ids)


def test_filter_by_currency_no_match(raw_transactions: list[dict[str, Any]]) -> None:
    """Чекаем, что при отсутствии валюты генератор возвращает пустой результат."""
    target_currency = "EUR"

    result_gen = filter_by_currency(raw_transactions, target_currency)

    assert isinstance(result_gen, GeneratorType)
    assert list(result_gen) == []


def test_filter_by_currency_empty_input() -> None:
    """Чекаем, что пустой список на входе возвращает пустой генератор."""
    result_gen = filter_by_currency([], "USD")
    assert list(result_gen) == []


# ТЕСТИРОВАНИЕ transaction_descriptions
def test_transaction_descriptions_full(raw_transactions: list[dict[str, Any]]) -> None:
    """Проверяем вывод всех описаний из фикстуры."""
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    descr_gen = transaction_descriptions(raw_transactions)

    assert isinstance(descr_gen, GeneratorType)
    assert list(descr_gen) == expected_descriptions


def test_transaction_descriptions_empty() -> None:
    """Проверяем пустой список на входе."""
    descr_gen = transaction_descriptions([])
    assert list(descr_gen) == []


def test_transaction_descriptions_single_item() -> None:
    """Проверяем список из одного элемента."""
    descr_gen = transaction_descriptions([{"description": "Тест"}])
    assert list(descr_gen) == ["Тест"]


# ТЕСТИРОВАНИЕ card_number_generator
def test_card_number_generator_range_and_formatting() -> None:
    """Проверяем правильность номеров и формат из бесконечного генератора."""
    card_gen = card_number_generator(1)

    assert isinstance(card_gen, GeneratorType), "Должен возвращаться генератор"

    result_cards = [next(card_gen) for _ in range(3)]
    assert result_cards == ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]


def test_card_number_generator_boundaries() -> None:
    """Проверяем генерацию с другого стартового значения."""
    card_gen = card_number_generator(5)

    result_cards = [next(card_gen) for _ in range(2)]
    assert result_cards == ["0000 0000 0000 0005", "0000 0000 0000 0006"]


def test_card_number_generator_formatting_check() -> None:
    """Проверяем, что номера карт содержат ровно 16 цифр и разделены пробелами."""
    card_gen = card_number_generator(10)
    card_number = next(card_gen)

    assert len(card_number) == 19
    blocks = card_number.split(" ")
    assert len(blocks) == 4
    for block in blocks:
        assert len(block) == 4
        assert block.isdigit()
