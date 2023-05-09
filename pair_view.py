import streamlit as st

from state import State
from pair import Pair


class PairView:
    @staticmethod
    def create(pair: Pair):
        columns = st.columns(2)
        with columns[0]:
            PairView._create_expected_input(pair)
        with columns[1]:
            PairView._create_actual_input(pair)

    @staticmethod
    def _create_expected_input(pair: Pair):
        def save_expected(widget_key: str):
            pair.expected = st.session_state[widget_key]

        key = State.generate_key()
        st.number_input(Pair.EXPECTED_TEXT, min_value=0.0, value=pair.expected,
                        key=key, label_visibility="collapsed", on_change=lambda: save_expected(key))

    @staticmethod
    def _create_actual_input(pair: Pair):
        def save_actual(widget_key: str):
            pair.actual = st.session_state[widget_key]

        key = State.generate_key()
        st.number_input(Pair.ACTUAL_TEXT, min_value=0.0, value=pair.actual,
                        key=key, label_visibility="collapsed", on_change=lambda: save_actual(key))
