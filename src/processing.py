from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по заданному статусу state.

    Возвращает отфильтрованный список словарей.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], is_reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'.

    По умолчанию сортирует по убыванию (сначала самые свежие).
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=is_reverse)


def main() -> None:
    """Генерация тестовых данных и демонстрация работы функций фильтрации и сортировки."""

    sample_transactions: List[Dict[str, Any]] = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("--- Проверка функции filter_by_state ---")
    print("Фильтр по умолчанию (EXECUTED):")
    executed_transactions = filter_by_state(sample_transactions)
    for transaction in executed_transactions:
        print(transaction)

    print("\nФильтр по статусу CANCELED:")
    canceled_transactions = filter_by_state(sample_transactions, "CANCELED")
    for transaction in canceled_transactions:
        print(transaction)

    print("\n--- Проверка функции sort_by_date (по убыванию) ---")
    transactions_by_date_desc: List[Dict[str, Any]] = sort_by_date(sample_transactions)
    for transaction in transactions_by_date_desc:
        print(transaction)

    print("\n--- Проверка функции sort_by_date (по возрастанию) ---")
    is_ascending_order: bool = False
    transactions_by_date_asc: List[Dict[str, Any]] = sort_by_date(
        sample_transactions, is_reverse=is_ascending_order
    )
    for transaction in transactions_by_date_asc:
        print(transaction)


if __name__ == "__main__":
    main()
