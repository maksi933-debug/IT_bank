import json
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from src.external_api import convert_to_rub, transaction_rub, transaction_usd


@pytest.fixture(autouse=True)
def mock_env_api_key(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Автоматическая фикстура для установки фейкового API_KEY в переменные окружения.

    Обеспечивает изоляцию тестов от реальных конфигурационных файлов разработчика.

    Args:
        monkeypatch (MonkeyPatch): Встроенная фикстура pytest для модификации окружения.
    """
    monkeypatch.setenv("API_KEY", "fake_api_key")
    yield


def test_convert_rub() -> None:
    """Тест: проверяет, что транзакции в RUB возвращаются без отправки сетевых запросов."""
    result: float = convert_to_rub(transaction_rub)
    assert result == 31957.58


@patch("os.getenv", return_value="fake_api_key")
@patch("requests.get")
def test_convert_usd(mock_requests_get: MagicMock, mock_getenv: MagicMock) -> None:
    """Тест: проверяет успешную конвертацию USD в RUB с корректными параметрами запроса.

    Args:
        mock_requests_get (MagicMock): Мок для перехвата сетевого вызова requests.get.
        mock_getenv (MagicMock): Мок для перехвата чтения переменной API_KEY.
    """
    mock_response: Mock = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 75000.0}
    mock_requests_get.return_value = mock_response

    result: float = convert_to_rub(transaction_usd)
    assert result == 75000.0

    mock_getenv.assert_called_with("API_KEY")
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        params={"to": "RUB", "from": "USD", "amount": "8221.37"},
        headers={"apikey": "fake_api_key"},
    )


@patch("os.getenv", return_value=None)
def test_missing_api_key(mock_getenv: MagicMock) -> None:
    """Тест: проверяет генерацию исключения ValueError при отсутствии ключа API в системе.

    Args:
        mock_getenv (MagicMock): Мок для имитации отсутствия переменной окружения.
    """
    with pytest.raises(ValueError) as exc_info:
        convert_to_rub(transaction_usd)

    assert "API_KEY не найден в переменных окружения." in str(exc_info.value)


def test_unsupported_currency() -> None:
    """Тест: проверяет реакцию системы на валюты, отличные от RUB, USD и EUR."""
    transaction_cny: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "Юань", "code": "CNY"},
        }
    }
    with pytest.raises(ValueError) as exc_info:
        convert_to_rub(transaction_cny)

    assert "Неподдерживаемая валюта для конвертации: CNY" in str(exc_info.value)
