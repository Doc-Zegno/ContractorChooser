import streamlit as st
import pandas as pd
import math

from dataframe_utils import convert_to_csv
from criterion import Criterion
from problems import Problems
from state import State
from key import Key


class CriteriaView:
    @staticmethod
    def create(
            criteria: list[Criterion],
            view_key: str,
            disable_name: bool = False,
            disable_upload: bool = False,
            disable_add_remove: bool = False
    ) -> Problems:
        st.header("Критерии")
        if not disable_upload:
            criteria_file_changed_key = Key(f"{view_key}.criteria.file.changed", default_value=False)
            csv_file = st.file_uploader("Загрузить критерии", key=f"criteria_upload_{view_key}", type="csv",
                                        on_change=lambda: State.set(criteria_file_changed_key))
            if State.reset(criteria_file_changed_key) and csv_file is not None:
                dataframe = pd.read_csv(csv_file)
                uploaded_criteria = Criterion.from_dataframe(dataframe)
                criteria.clear()
                criteria.extend(uploaded_criteria)
        column_width_weights = [1, 30, 20]
        if not disable_add_remove:
            column_width_weights.append(1)
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
                    criterion.name = st.text_input(Criterion.NAME_TEXT, key=f"criterion_name_{index}_{view_key}",
                                                   value=criterion.name, disabled=disable_name,
                                                   label_visibility="collapsed").strip()
                with columns[2]:
                    CriteriaView._create_criterion_value_input(criterion)
                if not disable_add_remove:
                    with columns[3]:
                        def remove_criterion(i: int = index):
                            criteria.pop(i)

                        st.button(":x:", key=f"criterion_remove_{index}_{view_key}", help="Удалить критерий",
                                  on_click=remove_criterion)
        if not disable_add_remove:
            st.button(":heavy_plus_sign:", key=f"criterion_add_{view_key}", help="Добавить критерий",
                      on_click=lambda: criteria.append(Criterion()))
        problems = CriteriaView._validate_criteria(criteria)
        if not problems.has_errors:
            serialized_criteria = convert_to_csv(Criterion.to_dataframe(criteria))
            st.download_button("Скачать критерии", serialized_criteria,
                               file_name=Criterion.FILE_NAME,
                               mime="text/csv")
        return problems

    @staticmethod
    def _create_criterion_value_input(criterion: Criterion):
        def save_value(widget_key: str):
            criterion.value = st.session_state[widget_key]

        key = State.generate_key()
        st.number_input(Criterion.VALUE_TEXT, value=criterion.value, min_value=0.0, max_value=1.0, key=key,
                        label_visibility="collapsed", on_change=lambda: save_value(key))

    @staticmethod
    def _validate_criteria(criteria: list[Criterion]) -> Problems:
        problems = Problems()
        duplicates = set()
        names = set()
        if len(criteria) == 0:
            problems.add_error("Не задано ни одного критерия")
            return problems  # No need to check any further
        for index, criterion in enumerate(criteria):
            if criterion.name == "":
                problems.add_error(f"Не задано название критерия №{index + 1}")
            elif criterion.name in names:
                if criterion.name not in duplicates:
                    problems.add_error(f"Несколько критериев с одним и тем же названием: {criterion.name}")
                    duplicates.add(criterion.name)
            else:
                names.add(criterion.name)
        total_value = sum(map(lambda c: c.value, criteria))
        if not math.isclose(total_value, 1.0):
            problems.add_warning(f"Суммарная значимость критериев ({total_value:.2f}) не равна 1")
        return problems
