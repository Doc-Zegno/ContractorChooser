import streamlit as st
import pandas as pd


class State:
    _IS_CRITERIA_FILE_CHANGED_TEXT = "is_criteria_file_changed"

    @staticmethod
    def set_criteria_file_changed():
        st.session_state[State._IS_CRITERIA_FILE_CHANGED_TEXT] = True

    @staticmethod
    def reset_criteria_file_changed() -> bool:
        """
        Atomically check whether the uploaded criteria file has recently changed
        and reset this status flag back to False, so the subsequent
        checks will fail until the next change of file.

        :return: True if uploaded criteria file has changed since the previous reset.
        """
        if State._IS_CRITERIA_FILE_CHANGED_TEXT not in st.session_state:
            return False
        is_criteria_file_changed = st.session_state[State._IS_CRITERIA_FILE_CHANGED_TEXT]
        st.session_state[State._IS_CRITERIA_FILE_CHANGED_TEXT] = False
        return is_criteria_file_changed


class Criterion:
    NAME_TEXT = "Название"
    VALUE_TEXT = "Значимость"
    FILE_NAME = "criteria.csv"

    def __init__(self, name: str = "", value: float = 0.0):
        self.value = value
        self.name = name

    @staticmethod
    def to_dataframe(criteria: list["Criterion"]) -> pd.DataFrame:
        values = []
        names = []
        for criterion in criteria:
            values.append(criterion.value)
            names.append(criterion.name)
        data = {
            Criterion.NAME_TEXT: names,
            Criterion.VALUE_TEXT: values,
        }
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame) -> list["Criterion"]:
        return [Criterion(row[Criterion.NAME_TEXT], row[Criterion.VALUE_TEXT]) for _, row in dataframe.iterrows()]


@st.cache_resource
def create_initial_criteria() -> list[Criterion]:
    return [
        Criterion("Цена", 0.35),
        Criterion("Качество", 0.65),
        Criterion("Удаленность", 0.1),
    ]


@st.cache_data
def convert_to_csv(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv().encode("utf-8")


def create_criteria_view(criteria: list[Criterion]):
    st.header("Критерии")
    csv_file = st.file_uploader("Загрузить критерии", type="csv", on_change=State.set_criteria_file_changed)
    if State.reset_criteria_file_changed() and csv_file is not None:
        dataframe = pd.read_csv(csv_file, index_col=0)
        uploaded_criteria = Criterion.from_dataframe(dataframe)
        criteria.clear()
        criteria.extend(uploaded_criteria)
    column_width_weights = [1, 8, 8, 1]
    with st.container():
        columns = st.columns(column_width_weights)
        with columns[1]:
            st.text(Criterion.NAME_TEXT)
        with columns[2]:
            st.text(Criterion.VALUE_TEXT, help="Дробный вес от 0 до 1")
    for index, criterion in enumerate(criteria):
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[0]:
                st.text(f"{index + 1}.")
            with columns[1]:
                criterion.name = st.text_input(Criterion.NAME_TEXT, key=f"criterion_name_{index}", value=criterion.name,
                                               label_visibility="collapsed")
            with columns[2]:
                criterion.value = st.number_input(Criterion.VALUE_TEXT, key=f"criterion_value_{index}",
                                                  value=criterion.value, min_value=0.0, max_value=1.0,
                                                  label_visibility="collapsed")
            with columns[3]:
                st.button(":x:", key=f"criterion_remove_{index}", help="Удалить критерий",
                          on_click=lambda: criteria.pop(index))
    st.button(":heavy_plus_sign:", key="criterion_add", help="Добавить критерий",
              on_click=lambda: criteria.append(Criterion()))
    serialized_criteria = convert_to_csv(Criterion.to_dataframe(criteria))
    st.download_button("Скачать критерии", serialized_criteria,
                       file_name=Criterion.FILE_NAME,
                       mime="text/csv")
    st.dataframe(Criterion.to_dataframe(criteria))  # TODO: for debug purposes only, remove later


def main():
    criteria = create_initial_criteria()
    create_criteria_view(criteria)


main()
