from collections.abc import Iterator
from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str = "USD") -> Iterator[Dict[str, Any]]:
    """Фильтрует список транзакций по заданному коду валюты."""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """Извлекает описание (назначение платежа) из каждой транзакции."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int | None = None) -> Iterator[str]:
    """Генерирует 16-значные номера банковских карт в заданном диапазоне."""
    if start < 0 or start > 9999999999999999:
        raise ValueError("Начальное значение должно быть в диапазоне от 0 до 9999999999999999")
    number = start
    while True:
        if end is not None and number > end:
            break
        """Форматируем число в 16-значную строку"""
        str_number = f"{number:016d}"
        """ Разделяем строку на 4 блока по 4 цифры через пробел и возвращаем как элемент генератора"""
        yield f"{str_number[:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:]}"
        number += 1