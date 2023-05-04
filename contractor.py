from typing import Optional
import pandas as pd
import math

from criterion import Criterion


class Contractor:
    NAME_TEXT = "Название"
    FILE_NAME = "contractors.csv"

    def __init__(self, name: str = "", scores: Optional[dict[str, int]] = None):
        self.scores = scores if scores is not None else {}
        self.name = name

    def calculate_total_score(self, criteria: list[Criterion]) -> float:
        return sum(map(lambda criterion: self.scores.get(criterion.name, 0) * criterion.value, criteria))

    @staticmethod
    def find_best(criteria: list[Criterion], contractors: list["Contractor"]) -> list["Contractor"]:
        total_scores = [contractor.calculate_total_score(criteria) for contractor in contractors]
        max_score = max(total_scores)
        return [contractor for contractor, total_score in zip(contractors, total_scores)
                if math.isclose(total_score, max_score)]

    @staticmethod
    def to_dataframe(criteria: list[Criterion], contractors: list["Contractor"]) -> pd.DataFrame:
        scores = {criterion.name: [] for criterion in criteria}
        names = []
        for contractor in contractors:
            names.append(contractor.name)
            for criterion in criteria:
                score = contractor.scores.get(criterion.name, 0)
                scores[criterion.name].append(score)
        data = {Contractor.NAME_TEXT: names, **scores}
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(criteria: list[Criterion], dataframe: pd.DataFrame) -> list["Contractor"]:
        return [Contractor._from_row(criteria, row) for _, row in dataframe.iterrows()]

    @staticmethod
    def _from_row(criteria: list[Criterion], row: pd.Series) -> "Contractor":
        scores = {criterion.name: row[criterion.name] for criterion in criteria}
        return Contractor(row[Contractor.NAME_TEXT], scores)
