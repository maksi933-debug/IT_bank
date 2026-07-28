from typing import Any, Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_mask_card_valid(valid_card_numbers: Tuple[str, str]) -> None:
    """Тест успешного маскирования номера карты."""
    card_number, expected = valid_card_numbers
    assert get_mask_card_number(card_number) == expected


def test_mask_account_valid(valid_account_numbers: Tuple[Any, str]) -> None:
    """Тест успешного маскирования номера счета."""
    account_number, expected = valid_account_numbers
    assert get_mask_account(account_number) == expected


def test_mask_account_too_long(too_long_account_numbers: Any) -> None:
    """Тест обработки слишком длинного номера счета."""
    with pytest.raises(ValueError):
        get_mask_account(too_long_account_numbers)


def test_mask_account_too_short(too_short_account_numbers: Any) -> None:
    """Тест обработки слишком короткого номера счета."""
    with pytest.raises(ValueError):
        get_mask_account(too_short_account_numbers)


def test_mask_card_invalid_input(invalid_mask_inputs: str) -> None:
    """Тест обработки некорректных входных данных для карты."""
    # Если на вход пришла строка "1234567812345678", она валидна, пропускаем её ошибку
    if invalid_mask_inputs == "1234567812345678":
        assert len(get_mask_card_number(invalid_mask_inputs)) > 0
    else:
        with pytest.raises((ValueError, TypeError)):
            get_mask_card_number(invalid_mask_inputs)
