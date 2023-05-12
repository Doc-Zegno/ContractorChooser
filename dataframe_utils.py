from io import BytesIO
import streamlit as st
import pandas as pd


@st.cache_data
def convert_to_csv(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")


@st.cache_data
def convert_to_excel(dataframe: pd.DataFrame) -> bytes:
    in_memory_writer = BytesIO()
    dataframe.to_excel(in_memory_writer, index=False)
    in_memory_writer.seek(0, 0)
    return in_memory_writer.read()
