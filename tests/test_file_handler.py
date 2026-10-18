import csv
from unittest.mock import mock_open, patch
import pandas as pd
import pytest

# Замените 'src.file_handler' на правильный путь импорта,
# в зависимости от того, как называется ваш файл с кодом ридеров
from src.file_handler import csv_data_reader, excel_data_reader


# =====================================================================
# ТЕСТЫ ДЛЯ CSV_DATA_READER (с использованием mock_open и patch)
# =====================================================================

@patch("builtins.open", new_callable=mock_open, read_data="id;state;amount\n123;EXECUTED;500\n")
def test_csv_data_reader_success(mock_file):
    """Тест успешного чтения CSV с использованием mock_open."""
    result = csv_data_reader("fake_path.csv")

    # Проверяем, что функция вернула список словарей
    assert result == [{"id": "123", "state": "EXECUTED", "amount": "500"}]
    # Проверяем, что встроенный open вызвался с правильными параметрами
    mock_file.assert_called_once_with("fake_path.csv", mode="r", encoding="utf-8")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_csv_data_reader_file_not_found(mock_file):
    """Тест поведения CSV-ридера при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        csv_data_reader("missing_file.csv")


# =====================================================================
# ТЕСТЫ ДЛЯ EXCEL_DATA_READER (с использованием Mock и patch)
# =====================================================================

@patch("pandas.read_excel")
def test_excel_data_reader_success(mock_read_excel):
    """Тест успешного чтения Excel с использованием patch."""
    # Создаем фейковый DataFrame, который якобы возвращает pandas при чтении файла
    fake_df = pd.DataFrame([
        {"id": 2177828.0, "state": "EXECUTED", "amount": 24853.0},
        {"id": 4137938.0, "state": "EXECUTED", "amount": ""}  # Пустая ячейка преобразуется в NaN в pandas
    ])
    mock_read_excel.return_value = fake_df

    result = excel_data_reader("fake_path.xlsx")

    # Проверяем, что float-числа успешно сконвертировались в целые int,
    # а пропущенное поле amount корректно заменилось на пустую строку ""
    assert result == [
        {"id": 2177828, "state": "EXECUTED", "amount": 24853},
        {"id": 4137938, "state": "EXECUTED", "amount": ""}
    ]
    # Убеждаемся, что библиотека pandas сделала вызов по указанному нами фейковому пути
    mock_read_excel.assert_called_once_with("fake_path.xlsx")


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_excel_data_reader_file_not_found(mock_read_excel):
    """Тест поведения Excel-ридера при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        excel_data_reader("missing_file.xlsx")
