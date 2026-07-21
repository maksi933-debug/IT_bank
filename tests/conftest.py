from typing import Any, Dict, List, Tuple, cast

import pytest


# ==================== ФИКСТУРЫ ДЛЯ КАРТ И СЧЕТОВ (masks) ====================
@pytest.fixture(
    params=[
        ("1234567812345678", "1234 56** **** 5678"),
        ("4145863215377628", "4145 86** **** 7628"),
        ("4464845444997515", "4464 84** **** 7515"),
        ("6963200011116146", "6963 20** **** 6146"),
        ("2502623184659746", "2502 62** **** 9746"),
        ("9197365930646785", "9197 36** **** 6785"),
    ]
)
def valid_card_numbers(request: pytest.FixtureRequest) -> Tuple[str, str]:
    return cast(Tuple[str, str], request.param)


@pytest.fixture(params=[(1234567890, "**7890"), ("736541084305", "**4305"), (64686473678894779589, "**9589")])
def valid_account_numbers(request: pytest.FixtureRequest) -> Tuple[Any, str]:
    return cast(Tuple[Any, str], request.param)


@pytest.fixture(params=[6468648574879343947386, "123456781234567890123"])
def too_long_account_numbers(request: pytest.FixtureRequest) -> Any:
    return request.param


@pytest.fixture(params=[1, 12, 123])
def too_short_account_numbers(request: pytest.FixtureRequest) -> Any:
    return request.param


# ==================== ФИКСТУРЫ ДЛЯ ВИДЖЕТА (widget) ====================


@pytest.fixture(
    params=[
        ("Visa Gold 7365410843013587", "Visa Gold 7365 41** **** 3587"),
        ("Maestro 1596847321596487", "Maestro 1596 84** **** 6487"),
        ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
        ("Мир 1234567812345678", "Мир 1234 56** **** 5678"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 98765432109876543210", "счет **3210"),
        ("СЧЕТ 11112222333344445555", "СЧЕТ **5555"),
    ]
)
def valid_card_and_account_strings(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Возвращает одну пару (входная_строка, ожидаемый_результат) за раз."""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(params=["", "   ", "1234567812345678", "Visa"])
def invalid_mask_inputs(request: pytest.FixtureRequest) -> str:
    """Возвращает одну некорректную строку за раз."""
    return cast(str, request.param)


@pytest.fixture(
    params=[
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-05-19T02:26:18.671407", "19.05.2025"),
        ("2026-07-20T13:53:00", "20.07.2026"),
        ("0001-01-01T00:00:00", "01.01.0001"),
        ("9999-12-31T23:59:59", "31.12.9999"),
        ("2024-02-29T12:00:00", "29.02.2024"),
    ]
)
def valid_date_strings(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Возвращает одну пару (ISO_дата, ДД.ММ.ГГГГ) за раз."""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        "",
        "   ",
        "2024-03-11",
        "11.03.2024T02:26:18",
        "invalid-string-data",
    ]
)
def invalid_date_strings(request: pytest.FixtureRequest) -> str:
    """Возвращает один некорректный формат даты за раз."""
    return cast(str, request.param)


# ==================== ФИКСТУРЫ ДЛЯ ОБРАБОТКИ (processing) ====================


@pytest.fixture
def sample_state_data() -> List[Dict[str, Any]]:
    """Фикстура с общими тестовыми данными для фильтрации по статусу."""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "PENDING", "amount": 400},
        {"id": 5, "amount": 500},
    ]


@pytest.fixture
def sample_date_data() -> List[Dict[str, Any]]:
    """Тестовые данные для стандартной проверки сортировки по датам."""
    return [
        {"id": 1, "date": "2026-10-15T16:00:00"},
        {"id": 2, "date": "2024-05-12T12:00:00"},
        {"id": 3, "date": "2026-12-01T08:30:00"},
    ]
