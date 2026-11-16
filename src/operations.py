import re
from collections import Counter
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Возвращает список словарей, у которых в описании есть заданная строка."""
    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for item in data:
        description = item.get("description")
        if isinstance(description, str) and pattern.search(description):
            result.append(item)

    return result


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """
    Принимает список словарей с операциями и список категорий.
    Возвращает словарь с количеством операций для каждой заданной категории.
    """
    descriptions = [item["description"].lower() for item in data if isinstance(item.get("description"), str)]

    counted_descriptions = Counter(descriptions)

    return {category: counted_descriptions[category.lower()] for category in categories}
