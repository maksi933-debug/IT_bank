import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
logfile_path = os.path.join(project_root, "logs", "utils.log")

# Создаем папку logs автоматически, если её еще нет
os.makedirs(os.path.dirname(logfile_path), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(logfile_path, "w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_financial_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Принимает путь до JSON-файла и возвращает список словарей."""
    logger.debug(f"Попытка чтения транзакций из файла: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)
            if isinstance(data, list):
                logger.debug(f"Успешно прочитано транзакций: {len(data)}")
                return data

            logger.error("Ошибка структуры: JSON-файл не содержит список")
            return []

    except (json.JSONDecodeError, TypeError, OSError) as e:
        logger.error(f"Ошибка при обработке JSON-файла: {str(e)}")
        return []
