from datetime import datetime


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает её с маской."""
    fragment = info.split()

    number = fragment[-1]

    """Всё, что идет до номера — это название (например, ["Visa", "Platinum"] или ["Счет"])"""
    name_fragment = fragment[:-1]
    name = " ".join(name_fragment)

    """ Проверяем, счет это или карта"""
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card(number)

    """ Собираем название и замаскированный номер обратно в одну строку"""
    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает её в формате ДД.ММ.ГГГГ."""
    # Превращаем ISO-строку в объект datetime (обрезка [:19] убирает микросекунды для стабильности)
    date_obj = datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")

    # Форматируем объект в строку нужного вида
    return date_obj.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print("--- Проверка маскировки карт и счетов ---")
    cards_and_accounts = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Visa Platinum 8990922113665229",
        "Счет 73654108430135874305",
    ]

    for item in cards_and_accounts:
        print(mask_account_card(item))

    print("\n--- Проверка форматирования даты ---")
    test_date = "2026-06-12T14:16:18.671407"
    print(f"Исходная дата: {test_date}")
    print(f"Результат:     {get_date(test_date)}")
