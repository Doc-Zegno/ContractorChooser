import math

import streamlit as st

from criterion import Criterion
from supplier import Supplier
from product import Product
from period import Period
import evaluators


class SecondResultView:
    @staticmethod
    def create(
            suppliers: list[Supplier],
            products: list[Product],
            criteria: list[Criterion],
            period: Period,
            has_problems: bool
    ):
        st.header("Результат")
        if has_problems:
            st.info("Устраните выявленные проблемы, чтобы рассчитать наилучшего поставщика", icon="ℹ")
            return
        if st.button("Рассчитать лучшего поставщика", key="supplier_calculate_best"):
            total_scores = []
            for supplier in suppliers:
                scores = evaluators.evaluate(supplier, products, period)
                total_score = SecondResultView._aggregate_scores(scores, criteria)
                st.markdown(SecondResultView._create_scores_markdown(supplier, scores, total_score))
                total_scores.append(total_score)
            min_score = min(total_scores)
            best_suppliers = [supplier for supplier, total_score in zip(suppliers, total_scores)
                              if math.isclose(total_score, min_score)]
            st.success(SecondResultView._create_best_suppliers_markdown(best_suppliers))

    @staticmethod
    def _aggregate_scores(scores: dict[str, float], criteria: list[Criterion]) -> float:
        result = 0.0
        for criterion in criteria:
            result += criterion.value * scores.get(criterion.name, 0.0)
        return result

    @staticmethod
    def _create_scores_markdown(supplier: Supplier, scores: dict[str, float], total_score: float) -> str:
        lines = [
            f"#### Результаты для поставщика '{supplier.name}'"
        ]
        for criterion_name, score in scores.items():
            lines.append(f" * балл по критерию '{criterion_name}': {score}")
        lines.append("")  # To stop filling an item list
        lines.append(f"Общий балл: {total_score}")
        return "\n".join(lines)

    @staticmethod
    def _create_best_suppliers_markdown(suppliers: list[Supplier]) -> str:
        assert len(suppliers) > 0
        if len(suppliers) == 1:
            return f"Лучший поставщик: {suppliers[0].name}"
        else:
            markdown = "Лучшие поставщики:"
            for supplier in suppliers:
                markdown += f"\n * {supplier.name}"
            return markdown
