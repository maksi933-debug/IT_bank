import json
import os
from typing import Any, Dict, List
from unittest.mock import MagicMock, mock_open, patch

import pytest


from src.utils import (
    filter_transactions_by_currency,
    get_financial_transactions,
    main,
    stat_decorator,
)


# === ТЕСТЫ ДЛЯ get_financial_transactions ===
def test_get_transactions_file_not_found() -> None:
    """Тест: проверяет, что если файл не существует, возвращается пустой список."""
    with patch("os.path.exists", return_value=False):
        assert get_financial_transactions("fake_path.json") == []


def test_get_transactions_empty_file() -> None:
    """Тест: проверяет, что пустой файл вызывает ошибку декодирования и возвращает []о список."""
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="")):
            assert get_financial_transactions("empty.json") == []


def test_get_transactions_invalid_json() -> None:
    """Тест: проверяет, что при битом или некорректном JSON возвращается пустой список."""
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="{invalid_json}")):
            assert get_financial_transactions("corrupt.json") == []


def test_get_transactions_not_a_list() -> None:
    """Тест: проверяет, что если JSON содержит словарь вместо списка, возвращается []о список."""
    valid_dict_json: str = '{"key": "value"}'
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=valid_dict_json)):
            assert get_financial_transactions("dict.json") == []


def test_get_transactions_success() -> None:
    """Тест: проверяет успешное чтение и валидацию корректного списка транзакций."""
    mock_data: List[Dict[str, Any]] = [{"id": 1, "amount": 100}]
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            assert get_financial_transactions("valid.json") == mock_data


# === ТЕСТЫ ДЛЯ ДЕКОРАТОРА stat_decorator ===

def test_stat_decorator_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест: декоратор корректно считает сумму и выводит статистику в консоль.

    Args:
        capsys (CaptureFixture): Встроенная фикстура pytest для перехвата вывода в консоль.
    """

    # Добавляем аргументы (*args), чтобы удовлетворить тип Callable[[str, str, str], ...] в декораторе
    @stat_decorator
    def mock_filter(*args: str, **kwargs: str) -> List[Dict[str, Any]]:
        return [
            {"operationAmount": {"amount": "150.50"}},  # Новый формат
            {"amount": "50.00"},  # Старый/плоский формат
            {"amount": "bad_number"},  # Игнорируемая ошибка
        ]

    # Передаем фейковые аргументы при вызове
    mock_filter("in.json", "out.json", "RUB")

    # Убираем явную аннотацию типа CaptureResult, чтобы mypy не ругался на старые версии pytest
    captured = capsys.readouterr()
    assert "Отфильтровано 3 транзакций на сумму 200.50" in captured.out


# === ТЕСТЫ ДЛЯ filter_transactions_by_currency ===
@pytest.fixture
def sample_transactions() -> List[Any]:
    """Фикстура, генерирующая смешанный список транзакций (корректные, плоские, пустые, не-словари).

    Returns:
        List[Any]: Тестовый набор транзакций для фильтрации.
    """
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
        },
        {"id": 3, "currency": "RUB", "amount": "300"},  # Альтернативная структура
        "not_a_dict",  # Некорректный тип данных в списке
        {},  # Пустой словарь
    ]


def test_filter_transactions_by_currency(sample_transactions: List[Any]) -> None:
    """Тест: проверяет фильтрацию транзакций по заданной валюте и запись результата в файл.

    Args:
        sample_transactions (List[Any]): Тестовый набор данных из фикстуры.
    """
    with patch("src.utils.get_financial_transactions", return_value=sample_transactions):
        m_open: MagicMock = mock_open()
        with patch("builtins.open", m_open):
            result: List[Dict[str, Any]] = filter_transactions_by_currency("in.json", "out.json", "RUB")

            # Должны остаться только транзакции 1 и 3
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 3

            m_open.assert_called_once_with("out.json", "w", encoding="utf-8")


# === ТЕСТ ДЛЯ ФУНКЦИИ main ===
@patch("src.utils.filter_transactions_by_currency")
@patch(
    "os.path.abspath",
    return_value=os.path.normpath("D:/project/src/utils.py"),
)
def test_utils_execution(mock_abspath: MagicMock, mock_filter: MagicMock) -> None:
    """Тест: проверяет, что функция main правильно вычисляет пути на базе текущего файла и вызывает фильтр.

    Args:
        mock_abspath (MagicMock): Изолированный метод вычисления абсолютного пути.
        mock_filter (MagicMock): Изолированная функция фильтрации транзакций.
    """
    main()

    expected_input: str = os.path.normpath("D:/project/data/operations.json")
    expected_output: str = os.path.normpath("D:/project/data/operations_filtered.json")

    mock_filter.assert_called_once_with(expected_input, expected_output, "RUB")
