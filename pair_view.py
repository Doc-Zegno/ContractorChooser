import streamlit as st

from pair import Pair


class PairView:
    @staticmethod
    def create(pair: Pair, view_key: str):
        columns = st.columns(2)
        with columns[0]:
            st.text("Lorem ipsum")
        with columns[1]:
            st.text("Dolor sit amet")
