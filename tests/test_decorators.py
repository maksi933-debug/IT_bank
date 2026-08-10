import os
from typing import Generator

import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log


# Тестовые функции для проверки вывода в консоль
@log()
def my_function(x: int, y: int) -> int:
    return x + y


@log()
def function_that_fails(x: int) -> float:
    return x / 0


# Тестовые функции для проверки записи в файл
@log(filename="test_log.txt")
def my_file_function(x: int, y: int) -> int:
    return x + y


@log(filename="test_log.txt")
def file_function_that_fails(x: int) -> float:
    return x / 0


# --- ТЕСТЫ ДЛЯ ВЫВОДА В КОНСОЛЬ ---


def test_my_function_success(capsys: CaptureFixture[str]) -> None:
    """Тест успешного выполнения функции с выводом в консоль."""
    result: int = my_function(1, 2)

    assert result == 3
    content = capsys.readouterr()
    assert "my_function ok\n" == content.out


def test_my_function_error(capsys: CaptureFixture[str]) -> None:
    """Тест логирования ошибки в консоль при нехватке аргументов."""
    with pytest.raises(TypeError) as _:
        my_function(1)  # type: ignore # Передаем только один аргумент вместо двух

    content = capsys.readouterr()
    expected_log: str = "my_function error: TypeError. Inputs: (1,), kwargs: {}\n"
    assert expected_log == content.out


def test_my_function_zero_division_error(capsys: CaptureFixture[str]) -> None:
    """Тест логирования ошибки вычисления в консоль."""
    with pytest.raises(ZeroDivisionError):
        function_that_fails(5)

    content = capsys.readouterr()
    expected_log: str = "function_that_fails error: ZeroDivisionError. Inputs: (5,), kwargs: {}\n"
    assert expected_log == content.out


# --- ТЕСТЫ ДЛЯ ЗАПИСИ В ФАЙЛ ---


@pytest.fixture
def cleanup_log_file() -> Generator[str, None, None]:
    """Фикстура для удаления тестового файла до и после теста."""
    filename: str = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


def test_file_logging_success(cleanup_log_file: str) -> None:
    """Тест успешного выполнения функции с записью в файл."""
    filename: str = cleanup_log_file

    result: int = my_file_function(10, 20)
    assert result == 30

    assert os.path.exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        content: str = f.read()
    assert "my_file_function ok\n" == content


def test_file_logging_error(cleanup_log_file: str) -> None:
    """Тест логирования ошибки с записью в файл."""
    filename: str = cleanup_log_file

    with pytest.raises(ZeroDivisionError):
        file_function_that_fails(10)

    assert os.path.exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        content: str = f.read()

    expected_log: str = "file_function_that_fails error: ZeroDivisionError. Inputs: (10,), kwargs: {}\n"
    assert expected_log == content


def test_file_logging_kwargs(cleanup_log_file: str) -> None:
    """Тест корректного логирования именованных аргументов (kwargs) в файл."""
    filename: str = cleanup_log_file

    @log(filename=filename)
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}"

    greet("Alice", greeting="Hi")

    with open(filename, "r", encoding="utf-8") as f:
        content: str = f.read()

    assert "greet ok\n" == content
