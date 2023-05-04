import streamlit as st

from second_app import SecondApp
from first_app import FirstApp


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
    tabs = st.tabs([FirstApp.TITLE, SecondApp.TITLE])
    with tabs[0]:
        FirstApp.create()
    with tabs[1]:
        SecondApp.create()
    create_footer()


main()
