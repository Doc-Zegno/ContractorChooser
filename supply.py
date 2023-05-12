from typing import Optional
import pandas as pd

import collection_utils as cu

from product import Product
from period import Period
from pair import Pair


class Supply:
    MONTH_TEXT = "Месяц"
    CSV_FILE_NAME = "supplies.csv"
    EXCEL_FILE_NAME = "supplies.xlsx"

    def __init__(self, quantities: Optional[dict[str, Pair]] = None):
        self.quantities = quantities if quantities is not None else {}

    @staticmethod
    def to_dataframe(supplies: list["Supply"], products: list[Product], period: Period) -> pd.DataFrame:
        cu.extend(supplies, until_length=period.length, with_value=Supply)
        quantities = {}
        for product in products:
            quantities[f"{product.name} {Pair.EXPECTED_MNEMONIC}"] = []
            quantities[f"{product.name} {Pair.ACTUAL_MNEMONIC}"] = []
        for supply in supplies:
            for product in products:
                quantity = cu.get_or_put(supply.quantities, key=product.name, default=Pair)
                quantities[f"{product.name} {Pair.EXPECTED_MNEMONIC}"].append(quantity.expected)
                quantities[f"{product.name} {Pair.ACTUAL_MNEMONIC}"].append(quantity.actual)
        month_names = [month.localized_name for month in period.months]
        data = {Supply.MONTH_TEXT: month_names, **quantities}
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame, products: list[Product]) -> list["Supply"]:
        return [Supply._from_row(row, products) for _, row in dataframe.iterrows()]

    @staticmethod
    def _from_row(row: pd.Series, products: list[Product]) -> "Supply":
        quantities = {}
        for product in products:
            expected = float(row[f"{product.name} {Pair.EXPECTED_MNEMONIC}"])
            actual = float(row[f"{product.name} {Pair.ACTUAL_MNEMONIC}"])
            quantities[product.name] = Pair(expected, actual)
        return Supply(quantities)
