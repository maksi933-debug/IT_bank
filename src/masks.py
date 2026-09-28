import logging
import os
from pathlib import Path
from typing import Union

current_dir = os.path.dirname(os.path.abspath(__file__))
"""Настройка абсолютного пути с авто-созданием папки"""
project_root = os.path.dirname(current_dir)


logs_dir = os.path.join(project_root, "logs")
"""Определение абсолютного пути относительно корня проекта"""

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
"""Если папки logs в корне проекта по какой-то причине нет, создаем её"""
logfile_path = os.path.join(logs_dir, "masks.log")

logger = logging.getLogger(__name__)
"""Создан отдельный объект логера для модуля masks"""

logger.setLevel(logging.DEBUG)
"""Установлен уровень логирования для логера модуля masks не меньше, чем DEBUG"""

file_handler = logging.FileHandler(logfile_path, "w", encoding="utf-8")
"""Настраиваем file_handler для логера модуля masks"""

file_handler.setLevel(logging.DEBUG)


file_formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s")
"""Настроен file_formatter (формат включает: метку времени, название модуля, уровень серьезности и сообщение"""

file_handler.setFormatter(file_formatter)


logger.addHandler(file_handler)
"""Добавлен handler для логера модуля masks"""


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формат: XXXX XX** **** XXXX"""
    logger.debug(f"Начало маскирования карты. Входные данные: {card_number}")

    if not isinstance(card_number, str):
        logger.error(f"Ошибка типа данных: передан {type(card_number)} вместо str")  # type: ignore[unreachable]
        raise TypeError("Номер карты должен быть строкой")

    if not card_number.strip():
        logger.error("Ошибка значения: передана пустая строка")
        raise ValueError("Номер карты не может быть пустым")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Ошибка значения: некорректный формат номера карты '{card_number}'")
        raise ValueError("Номер карты должен состоять ровно из 16 цифр")

    masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.debug("Маскирование карты успешно завершено")
    return masked_card


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счета в формат: **XXXX"""
    logger.debug(f"Начало маскирования счета. Входные данные: {account_number}")

    if not isinstance(account_number, (int, str)) or isinstance(account_number, bool):
        logger.error(f"Ошибка типа данных: передан {type(account_number)} вместо int/str")
        raise TypeError("Номер счета должен быть целым числом или строкой")

    account_str = str(account_number).strip()

    if not account_str.isdigit():
        logger.error(f"Ошибка значения: номер счета содержит не только цифры '{account_str}'")
        raise ValueError("Номер счета должен содержать только цифры")

    if len(account_str) > 20:
        logger.error(f"Ошибка значения: номер счета слишком длинный ({len(account_str)} цифр)")
        raise ValueError("Номер счета слишком длинный (максимум 20 цифр)")

    if len(account_str) < 4:
        logger.error(f"Ошибка значения: номер счета слишком короткий ({len(account_str)} цифр)")
        raise ValueError("Номер счета слишком короткий (минимум 4 цифры)")

    masked_account = f"**{account_str[-4:]}"
    logger.debug("Маскирование счета успешно завершено")
    return masked_account


# ТЕСТОВЫЙ БЛОК: Вызовется, только если вы запускаете файл masks.py напрямую
if __name__ == "__main__":
    get_mask_card_number("1234567890123456")
    try:
        get_mask_account("короткий")
    except ValueError:
        pass
