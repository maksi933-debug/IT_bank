from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по заданному статусу state. Возвращает отфильтрованный список словарей."""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], is_reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате.Безопасно обрабатывает отсутствие ключа 'date' и
    вызывает TypeError при смешанных типах."""

    return sorted(data, key=lambda item: item.get("date", ""), reverse=is_reverse)
