import json
import os
from typing import Any, Callable, Dict, List


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Принимает путь до JSON-файла и возвращает список словарей.

    Args:
        file_path (str): Путь к файлу JSON с транзакциями.

    Returns:
        List[Dict[str, Any]]: Список транзакций в виде словарей.
            Если файл пустой, поврежден или не содержит список,
            возвращается пустой список [].
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, TypeError, OSError):
        return []


def stat_decorator(
    func: Callable[[str, str, str], List[Dict[str, Any]]],
) -> Callable[[str, str, str], List[Dict[str, Any]]]:
    """Декоратор для подсчета суммы и вывода статистики по отфильтрованным транзакциям.

    Args:
        func (Callable): Декорируемая функция фильтрации.

    Returns:
        Callable: Функция-обёртка со встроенным логированием статистики.
    """

    def wrapper(*args: str, **kwargs: str) -> List[Dict[str, Any]]:
        filtered_transactions: List[Dict[str, Any]] = func(*args, **kwargs)

        total_amount: float = 0.0
        for transaction in filtered_transactions:
            if not isinstance(transaction, dict):
                continue                            # type: ignore[unreachable]

            amount_data: Any = transaction.get("operationAmount")
            if isinstance(amount_data, dict):
                amount_value: Any = amount_data.get("amount")
            else:
                amount_value = transaction.get("amount")

            try:
                if amount_value is not None:
                    total_amount += float(amount_value)
            except (ValueError, TypeError):
                continue

        print(f"Отфильтровано {len(filtered_transactions)} транзакций на сумму {total_amount:.2f}")
        return filtered_transactions

    return wrapper


@stat_decorator
def filter_transactions_by_currency(input_file: str, output_file: str, currency: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по коду валюты и сохраняет результат в файл JSON.

    Args:
        input_file (str): Путь к исходному файлу JSON с транзакциями.
        output_file (str): Путь для сохранения отфильтрованных транзакций.
        currency (str): Код валюты для фильтрации (например, 'RUB', 'USD').

    Returns:
        List[Dict[str, Any]]: Список отфильтрованных транзакций.
    """
    transactions: List[Dict[str, Any]] = get_financial_transactions(input_file)

    filtered_transactions: List[Dict[str, Any]] = []
    for transaction in transactions:
        if not isinstance(transaction, dict) or not transaction:
            continue

        # Безопасно извлекаем словарь operationAmount и вложенный словарь currency
        amount_data = transaction.get("operationAmount")

        # Получаем код из вложенной структуры, если она является словарем
        inner_code = ""
        if isinstance(amount_data, dict):
            currency_inner = amount_data.get("currency")
            if isinstance(currency_inner, dict):
                inner_code = str(currency_inner.get("code", ""))

        # Если inner_code пустой, берем значение с верхнего уровня.
        # Никаких сложных ветвлений — чистая линейная логика для mypy.
        curr_code = inner_code or str(transaction.get("currency", ""))

        if curr_code == currency: # mypy: ignore[unreachable]
            filtered_transactions.append(transaction)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(filtered_transactions, f, indent=4, ensure_ascii=False)
    except OSError:
        pass

    return filtered_transactions


def main() -> None:
    """Точка входа в приложение.

    Считывает переменные окружения, собирает абсолютные пути
    и запускает процесс фильтрации транзакций.
    """
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
