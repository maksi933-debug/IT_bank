import csv
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.file_handler import csv_data_reader, excel_data_reader

# =====================================================================
# ТЕСТЫ ДЛЯ CSV_DATA_READER
# =====================================================================

@patch("builtins.open", new_callable=mock_open, read_data="id;state;amount\n123;EXECUTED;500\n")
def test_csv_data_reader_success(mock_file: MagicMock) -> None:
    """Тест успешного чтения CSV с использованием mock_open."""
    result = csv_data_reader("fake_path.csv")

    assert result == [{"id": "123", "state": "EXECUTED", "amount": "500"}]
    mock_file.assert_called_once_with("fake_path.csv", mode="r", encoding="utf-8")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_csv_data_reader_file_not_found(mock_file: MagicMock) -> None:
    """Тест поведения CSV-ридера при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        csv_data_reader("missing_file.csv")


# =====================================================================
# ТЕСТЫ ДЛЯ EXCEL_DATA_READER
# =====================================================================

@patch("pandas.read_excel")
def test_excel_data_reader_success(mock_read_excel: MagicMock) -> None:
    """Тест успешного чтения Excel с использованием patch."""
    fake_df = pd.DataFrame([
        {"id": 2177828.0, "state": "EXECUTED", "amount": 24853.0},
        {"id": 4137938.0, "state": "EXECUTED", "amount": ""}
    ])
    mock_read_excel.return_value = fake_df

    result = excel_data_reader("fake_path.xlsx")

    assert result == [
        {"id": 2177828, "state": "EXECUTED", "amount": 24853},
        {"id": 4137938, "state": "EXECUTED", "amount": ""}
    ]
    mock_read_excel.assert_called_once_with("fake_path.xlsx")


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_excel_data_reader_file_not_found(mock_read_excel: MagicMock) -> None:
    """Тест поведения Excel-ридера при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        excel_data_reader("missing_file.xlsx")
