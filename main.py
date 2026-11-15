from pathlib import Path
from typing import Any

from src.file_handler import csv_data_reader, excel_data_reader
from src.operations import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.utils import get_financial_transactions
from src.widget import get_date, mask_account_card


def normalize_transactions(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Приводит транзакции из CSV/Excel к единому формату для корректной работы фильтров."""
    normalized = []
    for item in transactions:
        if "operationAmount" not in item and "amount" in item:
            item["operationAmount"] = {
                "amount": str(item.get("amount", "")),
                "currency": {
                    "name": str(item.get("currency_name", "")),
                    "code": str(item.get("currency_code", "")),
                },
            }
        normalized.append(item)
    return normalized


def load_transactions(data_dir: Path) -> list[dict[str, Any]]:
    """Запрашивает у пользователя тип файла и загружает список транзакций."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    menu_choice = ""
    while menu_choice not in ["1", "2", "3"]:
        menu_choice = input().strip()

    if menu_choice == "1":
        print("Для обработки выбран JSON-файл.")
        return get_financial_transactions(data_dir / "transactions.json")
    if menu_choice == "2":
        print("Для обработки выбран CSV-файл.")
        return csv_data_reader(data_dir / "transactions.csv")

    print("Для обработки выбран XLSX-файл.")
    return excel_data_reader(data_dir / "transactions_excel.xlsx")


def apply_filters(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Применяет цепочку пользовательских фильтров и сортировок к списку операций."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        raw_status = input().strip()
        status = raw_status.upper()

        if status in valid_statuses:
            break
        print(f'Статус операции "{raw_status}" недоступен.')

    transactions = filter_by_state(transactions, state=status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    print("Отсортировать операции по дате? Да/Нет")
    if input().strip().lower() == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        is_reverse = input().strip().lower() != "по возрастанию"
        transactions = sort_by_date(transactions, is_reverse=is_reverse)

    print("Выводить только рублевые транзакции? Да/Нет")
    if input().strip().lower() == "да":
        transactions = [
            t
            for t in transactions
            if t.get("currency_code") == "RUB"
            or t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    if input().strip().lower() == "да":
        word = input().strip()
        transactions = process_bank_search(transactions, word)

    return transactions


def print_transactions(transactions: list[dict[str, Any]]) -> None:
    """Форматирует и выводит итоговый список транзакций в консоль."""
    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for item in transactions:
        date_str = get_date(str(item.get("date", "")))
        description = item.get("description", "")

        from_acc = str(item.get("from") or "").strip()
        to_acc = str(item.get("to") or "").strip()

        masked_from = mask_account_card(from_acc) if from_acc and from_acc.lower() != "nan" else ""
        masked_to = mask_account_card(to_acc) if to_acc and to_acc.lower() != "nan" else ""
        route = f"{masked_from} -> {masked_to}" if masked_from else masked_to

        op_amount = item.get("operationAmount", {})
        amount = op_amount.get("amount", "")
        currency_code = str(op_amount.get("currency", {}).get("code", "")).strip().upper()
        currency_display = "руб." if currency_code == "RUB" else currency_code

        print(f"{date_str} {description}")
        print(f"{route}")
        print(f"Сумма: {amount} {currency_display}\n")


def main() -> None:
    """Главная функция взаимодействия с пользователем и вывода транзакций."""
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"

    raw_transactions = load_transactions(data_dir)
    normalized = normalize_transactions(raw_transactions)
    filtered = apply_filters(normalized)
    print_transactions(filtered)


if __name__ == "__main__":
    main()
