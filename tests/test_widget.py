from typing import Tuple

import pytest

from src.widget import get_date, mask_account_card

# 1. ТЕСТЫ ДЛЯ ВИДЖЕТА (МАСКИРОВАНИЕ)


def test_mask_account_card_valid(valid_card_and_account_strings: Tuple[str, str]) -> None:
    """Автоматически тестирует каждый корректный случай отдельно."""
    input_str, expected = valid_card_and_account_strings
    assert mask_account_card(input_str) == expected


def test_mask_account_card_invalid(invalid_mask_inputs: str) -> None:
    """Автоматически тестирует каждую некорректную строку отдельно."""
    with pytest.raises((ValueError, IndexError, AttributeError)):
        mask_account_card(invalid_mask_inputs)


# 2. ТЕСТЫ ДЛЯ ДАТЫ


def test_get_date_valid(valid_date_strings: Tuple[str, str]) -> None:
    """Автоматически тестирует каждый валидный случай даты отдельно."""
    date_str, expected = valid_date_strings
    assert get_date(date_str) == expected


def test_get_date_invalid(invalid_date_strings: str) -> None:
    """Автоматически тестирует каждый невалидный случай даты отдельно."""
    with pytest.raises((ValueError, TypeError, IndexError)):
        get_date(invalid_date_strings)
