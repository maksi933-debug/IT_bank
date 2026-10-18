import csv
from pathlib import Path
from typing import Any, cast

import pandas as pd


def csv_data_reader(path_to_file: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV и возвращает список словарей."""
    with open(path_to_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def excel_data_reader(path_to_file: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel и возвращает список словарей."""
    df = pd.read_excel(path_to_file)
    df = df.fillna("")

    # Оставляем cast только здесь, так как pandas возвращает Any
    data = cast(list[dict[str, Any]], df.to_dict(orient="records"))

    for row in data:
        if "id" in row and row["id"] != "":
            row["id"] = int(row["id"])
        if "amount" in row and row["amount"] != "":
            row["amount"] = (
                int(row["amount"]) if row["amount"] % 1 == 0 else row["amount"]
            )

    return data


if __name__ == "__main__":
    print(csv_data_reader("../data/transactions.csv"))
