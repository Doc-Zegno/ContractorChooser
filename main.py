import streamlit as st

from contractors_view import ContractorsView
from criteria_view import CriteriaView
from problems_view import ProblemsView
from result_view import ResultView
from state import State


APP_VERSION = "1.1.0"


def enable_vertical_alignment():
    # Workaround from https://github.com/streamlit/streamlit/issues/3052
    st.write(
        """<style>
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def create_footer():
    st.text(f"v{APP_VERSION}")


def main():
    st.set_page_config(page_title="Выбор Подрядчика", layout="wide")
    enable_vertical_alignment()
    criteria = State.get_criteria()
    criteria_problems = CriteriaView.create(criteria)
    ProblemsView.create(criteria_problems)
    contractors = State.get_contractors()
    contractors_problems = ContractorsView.create(criteria_problems.has_errors, criteria, contractors)
    ProblemsView.create(contractors_problems)
    has_problems = criteria_problems.has_issues or contractors_problems.has_issues
    ResultView.create(has_problems, criteria, contractors)
    create_footer()


main()
