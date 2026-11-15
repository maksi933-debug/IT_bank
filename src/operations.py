from collections import Counter
import csv
import json
from pathlib import Path
import re


def csv_to_json(csv_file_path: Path, json_file_path: Path) -> None:
    """Читает CSV-файл с разделителем ';' и сохраняет данные в JSON-формат."""
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        transactions = list(reader)

    json_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(transactions, json_file, ensure_ascii=False, indent=4)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Возвращает список словарей, у которых в описании есть заданная строка."""
    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for item in data:
        description = item.get("description")
        if isinstance(description, str) and pattern.search(description):
            result.append(item)

    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Принимает список словарей с операциями и список категорий.
    Возвращает словарь с количеством операций для каждой заданной категории.
    """
    descriptions = [
        item.get("description")
        for item in data
        if isinstance(item.get("description"), str)
    ]

    counted_descriptions = Counter(descriptions)

    return {category: counted_descriptions[category] for category in categories}


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    source_csv = data_dir / "transactions.csv"
    result_json = data_dir / "transactions.json"

    # 1. Конвертируем CSV в JSON и проверяем поиск
    if source_csv.exists():
        csv_to_json(source_csv, result_json)
        print(f"Файл успешно сохранен: {result_json}")

        with open(result_json, mode="r", encoding="utf-8") as f:
            loaded_transactions = json.load(f)

        search_query = "Открытие вклада"
        found_operations = process_bank_search(loaded_transactions, search_query)
        print(f"Найдено операций по запросу '{search_query}': {len(found_operations)}")

    # 2. Проверяем подсчет категорий
    sample_data = [
        {"id": 1, "description": "Перевод с карты на карту"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод организации"},
        {"id": 4, "description": "Перевод со счета на счет"},
    ]
    target_categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод с карты на карту",
        "Перевод со счета на счет",
    ]

    result = process_bank_operations(sample_data, target_categories)
    print(result)
