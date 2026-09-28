import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения один раз при запуске модуля
# 1. Находим путь к папке, где лежит текущий файл (src/)
current_dir: Path = Path(__file__).resolve().parent

# 2. Поднимаемся на один уровень выше — в корень проекта (где и лежит .env)
project_root: Path = current_dir.parent

# 3. Собираем точный путь к файлу .env
dotenv_path: Path = project_root / ".env"

# 4. Передаем этот точный путь в функцию загрузки
load_dotenv(dotenv_path=dotenv_path)

transaction_rub: Dict[str, Any] = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
        "amount": "31957.58",
        "currency": {"name": "руб.", "code": "RUB"},
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589",
}

transaction_usd: Dict[str, Any] = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
        "amount": "8221.37",
        "currency": {"name": "USD", "code": "USD"},
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560",
}


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в российские рубли (RUB) через внешнее API.

    Если валюта транзакции уже является 'RUB', функция возвращает сумму без изменений.
    Для валют 'USD' и 'EUR' выполняется запрос к внешнему сервису APILAYER.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции, содержащий
            структуру ['operationAmount']['amount'] и ['operationAmount']['currency']['code'].

    Returns:
        float: Сумма транзакции, сконвертированная в рубли и округленная до двух знаков.

    Raises:
        ValueError: Если API_KEY отсутствует в переменных окружения, если ответ API
            не содержит поле 'result', или если передана неподдерживаемая валюта.
        RuntimeError: Если сетевой запрос к внешнему API завершился ошибкой.
    """
    API_KEY: str | None = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY не найден в переменных окружения.")

    API_URL: str = "https://api.apilayer.com/exchangerates_data/convert"

    amount: str = transaction["operationAmount"]["amount"]
    currency: str = transaction["operationAmount"]["currency"]["code"]

    # Если валюта уже в рублях, возвращаем сумму без изменений
    if currency == "RUB":
        return round(float(amount), 2)

    # Строго проверяем, что валюта USD или EUR согласно условию задания
    if currency in ("USD", "EUR"):
        params: Dict[str, str] = {
            "to": "RUB",
            "from": currency,
            "amount": amount,
        }
        headers: Dict[str, str] = {
            "apikey": API_KEY,
        }

        try:
            response: requests.Response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()

            result: Dict[str, Any] = response.json()
            if "result" not in result:
                raise ValueError("Некорректный ответ от API.")

            return round(float(result["result"]), 2)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ошибка при запросе к API: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при обработке данных: {e}")

    # Если валюта не RUB, USD или EUR
    raise ValueError(f"Неподдерживаемая валюта для конвертации: {currency}")
