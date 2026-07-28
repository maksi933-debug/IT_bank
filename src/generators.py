from collections.abc import Iterator
from typing import Any, Dict, Generator, List


# Строка 5: Указываем, что транзакция — это словарь Dict[str, Any]
def filter_by_currency(transactions: list[Dict[str, Any]], currency: str = "USD") -> Iterator[Dict[str, Any]]:
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


# Строка 10: Указываем, что генератор возвращает описание транзакции в виде строки (str)
def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    for transaction in transactions:
        yield transaction.get("description", "")


# Строка 15+: Генератор номеров карт (исправление ошибки со start_num)
def card_number_generator(start: int, end: int | None = None) -> Iterator[str]:
    """Генерирует номера карт, начиная со start.
    Если задан end, останавливается на нем. Иначе генерирует бесконечно.
    """
    number = start
    while True:
        if end is not None and number > end:
            break

        # Форматируем число в 16-значную строку с ведущими нулями
        str_number = f"{number:016d}"
        yield f"{str_number[:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:]}"
        number += 1
