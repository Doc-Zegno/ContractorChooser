from typing import Optional, Union
import streamlit as st
import pandas as pd


class State:
    _IS_CRITERIA_FILE_CHANGED_TEXT = "is_criteria_file_changed"
    _IS_CONTRACTORS_FILE_CHANGED_TEXT = "is_contractors_file_changed"

    @staticmethod
    def set_criteria_file_changed():
        State._set(State._IS_CRITERIA_FILE_CHANGED_TEXT)

    @staticmethod
    def reset_criteria_file_changed() -> bool:
        """
        Atomically check whether the uploaded criteria file has recently changed
        and reset this status flag back to False, so the subsequent
        checks will fail until the next change of file.

        :return: True if uploaded criteria file has changed since the previous reset.
        """
        return State._reset(State._IS_CRITERIA_FILE_CHANGED_TEXT)

    @staticmethod
    def set_contractors_file_changed():
        State._set(State._IS_CONTRACTORS_FILE_CHANGED_TEXT)

    @staticmethod
    def reset_contractors_file_changed():
        """
        Atomically check whether the uploaded contractors file has recently changed
        and reset this status flag back to False, so the subsequent
        checks will fail until the next change of file.

        :return: True if uploaded contractors file has changed since the previous reset.
        """
        return State._reset(State._IS_CONTRACTORS_FILE_CHANGED_TEXT)

    @staticmethod
    def _set(flag_name: str):
        st.session_state[flag_name] = True

    @staticmethod
    def _reset(flag_name: str) -> bool:
        if flag_name not in st.session_state:
            return False
        has_flag_been_set = st.session_state[flag_name]
        st.session_state[flag_name] = False
        return has_flag_been_set


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


class Contractor:
    NAME_TEXT = "Название"
    FILE_NAME = "contractors.csv"

    def __init__(self, name: str = "", scores: Optional[dict[str, int]] = None):
        self.scores = scores if scores is not None else {}
        self.name = name

    @staticmethod
    def to_dataframe(criteria: list[Criterion], contractors: list["Contractor"]) -> pd.DataFrame:
        data: dict[str, Union[list[int], list[str]]] = {}
        names = []
        for criterion in criteria:
            data[criterion.name] = []
        for contractor in contractors:
            names.append(contractor.name)
            for criterion in criteria:
                score = contractor.scores[criterion.name]  # TODO: gracefully handle missing values here
                data[criterion.name].append(score)
        data[Contractor.NAME_TEXT] = names  # TODO (minor): wrong order of columns
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(criteria: list[Criterion], dataframe: pd.DataFrame) -> list["Contractor"]:
        return [Contractor._from_row(criteria, row) for _, row in dataframe.iterrows()]

    @staticmethod
    def _from_row(criteria: list[Criterion], row: pd.Series) -> "Contractor":
        scores = {criterion.name: row[criterion.name] for criterion in criteria}
        return Contractor(row[Contractor.NAME_TEXT], scores)


@st.cache_resource
def create_initial_criteria() -> list[Criterion]:
    return [
        Criterion("Цена", 0.35),
        Criterion("Качество", 0.65),
        Criterion("Удаленность", 0.1),
    ]


@st.cache_resource
def create_initial_contractors() -> list[Contractor]:
    return [
        Contractor("Рога и Копыта", {"Цена": 3, "Качество": 4, "Удаленность": 2})
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
                def remove_criterion(i: int = index):
                    criteria.pop(i)
                st.button(":x:", key=f"criterion_remove_{index}", help="Удалить критерий",
                          on_click=remove_criterion)
    st.button(":heavy_plus_sign:", key="criterion_add", help="Добавить критерий",
              on_click=lambda: criteria.append(Criterion()))
    serialized_criteria = convert_to_csv(Criterion.to_dataframe(criteria))
    st.download_button("Скачать критерии", serialized_criteria,
                       file_name=Criterion.FILE_NAME,
                       mime="text/csv")
    st.dataframe(Criterion.to_dataframe(criteria))  # TODO: for debug purposes only, remove later


def create_contractors_view(criteria: list[Criterion], contractors: list[Contractor]):
    st.header("Подрядчики")
    if len(criteria) == 0:
        st.error("Невозможно отобразить данные о подрядчиках, пока не заданы критерии")
        return
    csv_file = st.file_uploader("Загрузить подрядчиков", type="csv", on_change=State.set_contractors_file_changed)
    if State.reset_contractors_file_changed() and csv_file is not None:
        dataframe = pd.read_csv(csv_file, index_col=0)
        uploaded_contractors = Contractor.from_dataframe(criteria, dataframe)
        contractors.clear()
        contractors.extend(uploaded_contractors)
    large_column_weight = 24 // (len(criteria) + 1)
    column_width_weights = [1, 8] + [large_column_weight] * len(criteria) + [1]
    with st.container():
        columns = st.columns(column_width_weights)
        with columns[1]:
            st.text(Contractor.NAME_TEXT)
        for criterion_index, criterion in enumerate(criteria):
            with columns[2 + criterion_index]:
                st.text(criterion.name)
    for contractor_index, contractor in enumerate(contractors):
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[0]:
                st.text(f"{contractor_index + 1}.")
            with columns[1]:
                contractor.name = st.text_input(Contractor.NAME_TEXT, key=f"contractor_name_{contractor_index}",
                                                value=contractor.name, label_visibility="collapsed")
            for criterion_index, criterion in enumerate(criteria):
                with columns[2 + criterion_index]:
                    old_score = contractor.scores.get(criterion.name, 0)
                    new_score = st.text_input(criterion.name, value=old_score, label_visibility="collapsed",
                                              key=f"contractor_{contractor_index}_criterion_{criterion_index}")
                    contractor.scores[criterion.name] = new_score
            with columns[-1]:
                # def remove_contractor(i: int = contractor_index):  # FIXME: is invoked automatically for some reason
                #     contractors.pop(i)
                st.button(":x:", key=f"contractor_remove_{contractor_index}", help="Удалить подрядчика")
    st.button(":heavy_plus_sign:", key="contractor_add", help="Добавить подрядчика",
              on_click=lambda: contractors.append(Contractor()))
    serialized_contractors = convert_to_csv(Contractor.to_dataframe(criteria, contractors))
    st.download_button("Скачать подрядчиков", serialized_contractors,
                       file_name=Contractor.FILE_NAME,
                       mime="text/csv")
    st.dataframe(Contractor.to_dataframe(criteria, contractors))  # TODO: for debug purposes only, remove later


def main():
    criteria = create_initial_criteria()
    create_criteria_view(criteria)
    contractors = create_initial_contractors()
    create_contractors_view(criteria, contractors)


main()
