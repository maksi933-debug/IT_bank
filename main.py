from pathlib import Path
import sys

# Добавляем корень проекта в пути поиска, чтобы Python всегда видел папку src
sys.path.append(str(Path(__file__).resolve().parent))

from src.generators import filter_by_currency
from src.file_handler import csv_data_reader, excel_data_reader
from src.processing import filter_by_state, sort_by_date
from src.operations import process_bank_search
from src.utils import get_financial_transactions
from src.widget import get_date, mask_account_card


def normalize_transactions(transactions: list[dict]) -> list[dict]:
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


def main() -> None:
    """Главная функция взаимодействия с пользователем и вывода транзакций."""
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"

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
        transactions = get_financial_transactions(data_dir / "transactions.json")
    elif menu_choice == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = csv_data_reader(data_dir / "transactions.csv")
    else:
        print("Для обработки выбран XLSX-файл.")
        transactions = excel_data_reader(data_dir / "transactions_excel.xlsx")

    transactions = normalize_transactions(transactions)

    # 1. Фильтрация по статусу
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

    # 2. Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_date = input().strip().lower()
    if sort_date == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        ascending = input().strip().lower()
        is_reverse = ascending != "по возрастанию"
        transactions = sort_by_date(transactions, is_reverse=is_reverse)

    # 3. Фильтрация по валюте
    print("Выводить только рублевые транзакции? Да/Нет")
    filter_code = input().strip().lower()
    if filter_code == "да":
        transactions = [
            t for t in transactions
            if t.get("currency_code") == "RUB"
               or t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # 4. Фильтрация по слову в описании
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    filter_word = input().strip().lower()
    if filter_word == "да":
        word = input().strip()
        transactions = process_bank_search(transactions, word)

    # 5. Вывод итогового списка транзакций
    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for item in transactions:
        # Форматирование даты и описания
        date_str = get_date(str(item.get("date", "")))
        description = item.get("description", "")

        # Форматирование отправителя и получателя с маскировкой
        from_acc = item.get("from")
        to_acc = item.get("to")
        masked_from = mask_account_card(str(from_acc)) if from_acc and str(from_acc) != "nan" else ""
        masked_to = mask_account_card(str(to_acc)) if to_acc and str(to_acc) != "nan" else ""

        route = f"{masked_from} -> {masked_to}" if masked_from else masked_to

        # Извлечение суммы и валюты (поддержка RUB и всех 100+ мировых валют)
        op_amount = item.get("operationAmount", {})
        amount = op_amount.get("amount", "")
        currency_code = str(op_amount.get("currency", {}).get("code", "")).strip().upper()
        currency_display = "руб." if currency_code == "RUB" else currency_code

        print(f"{date_str} {description}")
        print(f"{route}")
        print(f"Сумма: {amount} {currency_display}\n")


if __name__ == "__main__":
    main()


