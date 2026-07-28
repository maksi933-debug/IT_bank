from typing import Union


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формат: XXXX XX** **** XXXX"""
    if not isinstance(card_number, str):
        raise TypeError("Номер карты должен быть строкой")
    if not card_number.strip():
        raise ValueError("Номер карты не может быть пустым")
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять ровно из 16 цифр")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счета в формат: **XXXX"""
    if not isinstance(account_number, (int, str)) or isinstance(account_number, bool):
        raise TypeError("Номер счета должен быть целым числом или строкой")

    account_str = str(account_number).strip()

    if not account_str.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(account_str) > 20:
        raise ValueError("Номер счета слишком длинный (максимум 20 цифр)")
    if len(account_str) < 4:
        raise ValueError("Номер счета слишком короткий (минимум 4 цифры)")

    return f"**{account_str[-4:]}"


# === БЛОК ЗАПУСКА КОДА ===
if __name__ == "__main__":
    # Передаем тестовые данные для получения вашего результата
    card_result = get_mask_card_number("7000790012346361")
    account_result = get_mask_account("736541084305")

    print(card_result)  # Выведет: 7000 79** **** 6361
    print(account_result)  # Выведет: **4305
