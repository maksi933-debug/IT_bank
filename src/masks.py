def get_mask_card_number(card_number: str) -> str:
    """Оставляем первые 6 и последние 4 цифры"""
    masked = card_number[:6] + "**" + "****" + card_number[-4:]

    return " ".join([masked[i : i + 4] for i in range(0, len(masked), 4)])

    """Разбиваем по блокам по 4 символа"""


def get_mask_account(account_number: str) -> str:
    """Показываем только последние 4 цифры"""
    return "**" + account_number[-4:]


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))

    print(get_mask_account("73654108430135874305"))
