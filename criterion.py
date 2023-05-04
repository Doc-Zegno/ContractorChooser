import pandas as pd


class Criterion:
    NAME_TEXT = "Название"
    VALUE_TEXT = "Значимость"
    FILE_NAME = "criteria.csv"

    def __init__(self, name: str = "", value: float = 0.0):
        self.value = value
        self.name = name

    @staticmethod
    def to_dataframe(criteria: list["Criterion"]) -> pd.DataFrame:
        values = []
        names = []
        for criterion in criteria:
            values.append(criterion.value)
            names.append(criterion.name)
        data = {
            Criterion.NAME_TEXT: names,
            Criterion.VALUE_TEXT: values,
        }
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame) -> list["Criterion"]:
        return [Criterion(row[Criterion.NAME_TEXT], row[Criterion.VALUE_TEXT]) for _, row in dataframe.iterrows()]
