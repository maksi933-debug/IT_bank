def filter_by_state(data: list[dict], state: str = "EXECUTED") -> str:
    """Фильтрует список словарей и возвращает их в виде строки, где каждый элемент записан с новой строки."""
    filtered_items = [item for item in data if item.get("state") == state]


    return "\n".join(str(item) for item in filtered_items)
    """Объединяем словари в одну строку, разделяя их символом переноса строки \n"""


if __name__ == "__main__":

    mock_data = [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
        },
    ]

    # 1. Тест со значением по умолчанию ('EXECUTED')
    print("Фильтр по умолчанию (EXECUTED):")
    print(filter_by_state(mock_data))

    # 2. Тест со значением 'CANCELED'
    print("\nФильтр по статусу CANCELED:")
    print(filter_by_state(mock_data, "CANCELED"))


    def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
        """Сортирует список словарей по дате.

        По умолчанию сортирует по убыванию (сначала самые свежие).
        Если передать reverse=False, отсортирует по возрастанию.
        """
        return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)


    # Блок проверки работы функций
    if __name__ == "__main__":
        mock_data = [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
        ]

        print("--- Проверка функции sort_by_date (по убыванию) ---")
        sorted_data_desc = sort_by_date(mock_data)
        # Выводим результат так, чтобы каждый словарь начинался со следующей строки
        for item in sorted_data_desc:
            print(item)

        print("\n--- Проверка функции sort_by_date (по возрастанию) ---")
        sorted_data_asc = sort_by_date(mock_data, reverse=False)
        for item in sorted_data_asc:
            print(item)