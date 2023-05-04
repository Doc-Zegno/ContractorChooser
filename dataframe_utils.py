import streamlit as st
import pandas as pd


@st.cache_data
def convert_to_csv(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")
