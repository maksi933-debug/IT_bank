import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
logfile_path = os.path.join(project_root, "logs", "utils.log")

# Создаем папку logs автоматически, если её еще нет
os.makedirs(os.path.dirname(logfile_path), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(logfile_path, "w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_financial_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Принимает путь до JSON-файла и возвращает список словарей."""
    logger.debug(f"Попытка чтения транзакций из файла: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)
            if isinstance(data, list):
                logger.debug(f"Успешно прочитано транзакций: {len(data)}")
                return data

            logger.error("Ошибка структуры: JSON-файл не содержит список")
            return []

    except (json.JSONDecodeError, TypeError, OSError) as e:
        logger.error(f"Ошибка при обработке JSON-файла: {str(e)}")
        return []


def stat_decorator(
    func: Callable[[str, str, str], List[Dict[str, Any]]],
) -> Callable[[str, str, str], List[Dict[str, Any]]]:
    """Декоратор для подсчета суммы и вывода статистики по отфильтрованным транзакциям."""

    def wrapper(*args: str, **kwargs: str) -> List[Dict[str, Any]]:
        filtered_transactions: List[Dict[str, Any]] = func(*args, **kwargs)

        total_amount: float = 0.0
        for transaction in filtered_transactions:
            if not isinstance(transaction, dict):
                continue

            amount_data: Any = transaction.get("operationAmount")
            if isinstance(amount_data, dict):
                amount_value: Any = amount_data.get("amount")
            else:
                amount_value = transaction.get("amount")

            try:
                if amount_value is not None:
                    total_amount += float(amount_value)
            except (ValueError, TypeError) as e:
                logger.error(f"Не удалось преобразовать сумму транзакции в float: {str(e)}")
                continue

        stats_message = f"Отфильтровано {len(filtered_transactions)} транзакций на сумму {total_amount:.2f}"
        print(stats_message)
        logger.debug(stats_message)
        return filtered_transactions

    return wrapper


@stat_decorator
def filter_transactions_by_currency(input_file: str, output_file: str, currency: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по коду валюты и сохраняет результат в файл JSON."""
    logger.debug(f"Запуск фильтрации транзакций по валюте '{currency}'")
    transactions: List[Dict[str, Any]] = get_financial_transactions(input_file)

    filtered_transactions: List[Dict[str, Any]] = []
    for transaction in transactions:
        if not isinstance(transaction, dict) or not transaction:
            continue

        amount_data = transaction.get("operationAmount")
        inner_code = ""
        if isinstance(amount_data, dict):
            currency_inner = amount_data.get("currency")
            if isinstance(currency_inner, dict):
                inner_code = str(currency_inner.get("code", ""))

        curr_code = inner_code or str(transaction.get("currency", ""))
        if curr_code == currency:
            filtered_transactions.append(transaction)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(filtered_transactions, f, indent=4, ensure_ascii=False)
        logger.debug(f"Отфильтрованные транзакции успешно сохранены в файл: {output_file}")
    except OSError as e:
        logger.error(f"Не удалось записать результат фильтрации в файл {output_file}: {str(e)}")

    return filtered_transactions


def main() -> None:
    """Точка входа в приложение."""
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    project_root: str = os.path.dirname(current_dir)

    input_file: str = os.getenv("INPUT_FILE_PATH", os.path.join(project_root, "data", "operations.json"))
    output_file: str = os.getenv(
        "OUTPUT_FILE_PATH",
        os.path.join(project_root, "data", "operations_filtered.json"),
    )
    currency: str = os.getenv("DEFAULT_CURRENCY", "RUB")

    filter_transactions_by_currency(input_file, output_file, currency)


if __name__ == "__main__":
    main()
