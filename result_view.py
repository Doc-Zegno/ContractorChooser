import streamlit as st

from contractor import Contractor
from criterion import Criterion


class ResultView:
    @staticmethod
    def create(has_problems: bool, criteria: list[Criterion], contractors: list[Contractor]):
        st.header("Результат")
        if has_problems:
            st.info("Устраните выявленные проблемы, чтобы рассчитать наилучшего подрядчика", icon="ℹ")
            return
        if st.button("Рассчитать лучшего подрядчика", key="contractor_calculate_best"):
            best_contractors = Contractor.find_best(criteria, contractors)
            st.success(ResultView._get_best_contractor_text(best_contractors))

    @staticmethod
    def _get_best_contractor_text(best_contractors: list[Contractor]) -> str:
        assert len(best_contractors) > 0
        if len(best_contractors) == 1:
            return f"Лучший подрядчик: {best_contractors[0].name}"
        else:
            markdown = "Лучшие подрядчики:"
            for contractor in best_contractors:
                markdown += f"\n * {contractor.name}"
            return markdown
