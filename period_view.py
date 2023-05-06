import streamlit as st

from problems import Problems
from period import Period
from month import Month
from state import State


class PeriodView:
    @staticmethod
    def create(period: Period) -> Problems:
        st.header("Период Времени")
        columns = st.columns(2)
        with columns[0]:
            PeriodView._create_first_month_input(period)
        with columns[1]:
            PeriodView._create_last_month_input(period)
        return PeriodView._validate(period)

    @staticmethod
    def _create_first_month_input(period: Period):
        def save_score(widget_key: str):
            period.first_month = Month.parse(st.session_state[widget_key])

        key = State.generate_key()
        st.selectbox(Period.FIRST_MONTH_TEXT, Period.OPTIONS, index=period.first_month.value,
                     key=key, on_change=lambda: save_score(key))

    @staticmethod
    def _create_last_month_input(period: Period):
        def save_score(widget_key: str):
            period.last_month = Month.parse(st.session_state[widget_key])

        key = State.generate_key()
        st.selectbox(Period.LAST_MONTH_TEXT, Period.OPTIONS, index=period.last_month.value,
                     key=key, on_change=lambda: save_score(key))

    @staticmethod
    def _validate(period: Period) -> Problems:
        problems = Problems()
        if period.first_month == period.last_month:
            problems.add_error("Первый и последний месяц периода совпадают")
        return problems
