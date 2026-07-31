from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает её с маской."""
    # Проверка на тип данных
    if not isinstance(info, str):
        raise AttributeError("Входные данные должны быть строкой")

    fragment = info.split()

    # Проверка на пустую строку или отсутствие одного из обязательных элементов
    if len(fragment) < 2:
        raise ValueError("Строка должна содержать как название, так и номер")

    number = fragment[-1]

    # Всё, что идет до номера это название (например, ["Visa", "Platinum"] или ["Счет"])
    name_fragment = fragment[:-1]
    name = " ".join(name_fragment)

    # Проверяем, счет это или карта
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    # Собираем название и замаскированный номер обратно в одну строку
    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает её в формате ДД.ММ.ГГГГ."""
    # Превращаем ISO-строку в объект datetime (обрезка [:19] убирает микросекунды для стабильности)
    date_obj = datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")

    # Форматируем объект в строку нужного вида
    return date_obj.strftime("%d.%m.%Y")
