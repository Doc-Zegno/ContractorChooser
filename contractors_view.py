import streamlit as st
import pandas as pd

from dataframe_utils import convert_to_csv
from contractor import Contractor
from criterion import Criterion
from problems import Problems
from state import State


class ContractorsView:
    @staticmethod
    def create(has_errors: bool, criteria: list[Criterion], contractors: list[Contractor]) -> Problems:
        st.header("Подрядчики")
        problems = Problems()
        if has_errors or len(criteria) == 0:
            problems.add_error("Невозможно отобразить данные о подрядчиках, пока не заданы корректные критерии")
            return problems
        csv_file = st.file_uploader("Загрузить подрядчиков", type="csv", on_change=State.set_contractors_file_changed)
        if State.reset_contractors_file_changed() and csv_file is not None:
            dataframe = pd.read_csv(csv_file)
            uploaded_contractors = Contractor.from_dataframe(criteria, dataframe)
            contractors.clear()
            contractors.extend(uploaded_contractors)
        column_width_weights = [1, 14, 33, 3, 1]
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[1]:
                st.text(Contractor.NAME_TEXT)
            with columns[2]:
                criterion_columns = st.columns(len(criteria))
                for criterion_index, criterion in enumerate(criteria):
                    with criterion_columns[criterion_index]:
                        st.text(criterion.name)
            with columns[-2]:
                st.text("Балл", help="Суммарная оценка подрядчика с учетом всех критериев")
        for contractor_index, contractor in enumerate(contractors):
            with st.container():
                columns = st.columns(column_width_weights)
                with columns[0]:
                    st.text(f"{contractor_index + 1}.")
                with columns[1]:
                    contractor.name = st.text_input(Contractor.NAME_TEXT, key=f"contractor_name_{contractor_index}",
                                                    value=contractor.name, label_visibility="collapsed").strip()
                with columns[2]:
                    criterion_columns = st.columns(len(criteria))
                    for criterion_index, criterion in enumerate(criteria):
                        with criterion_columns[criterion_index]:
                            ContractorsView._create_contractor_score_input(criterion, contractor)
                with columns[-2]:
                    st.text(f"{contractor.calculate_total_score(criteria):.2f}")
                with columns[-1]:
                    def remove_contractor(i: int = contractor_index):
                        contractors.pop(i)

                    st.button(":x:", key=f"contractor_remove_{contractor_index}", help="Удалить подрядчика",
                              on_click=remove_contractor)
        st.button(":heavy_plus_sign:", key="contractor_add", help="Добавить подрядчика",
                  on_click=lambda: contractors.append(Contractor()))
        ContractorsView._validate_contractors(problems, criteria, contractors)
        if not problems.has_errors:
            serialized_contractors = convert_to_csv(Contractor.to_dataframe(criteria, contractors))
            st.download_button("Скачать подрядчиков", serialized_contractors,
                               file_name=Contractor.FILE_NAME,
                               mime="text/csv")
        return problems

    @staticmethod
    def _create_contractor_score_input(criterion: Criterion, contractor: Contractor):
        def save_score(widget_key: str):
            contractor.scores[criterion.name] = st.session_state[widget_key]

        key = State.generate_key()
        old_score = contractor.scores.get(criterion.name, 0)
        st.number_input(criterion.name, value=old_score, label_visibility="collapsed", key=key,
                        min_value=0, max_value=5, on_change=lambda: save_score(key))

    @staticmethod
    def _validate_contractors(problems: Problems, criteria: list[Criterion], contractors: list[Contractor]):
        duplicates = set()
        names = set()
        if len(contractors) == 0:
            problems.add_error("Не задано ни одного подрядчика")
            return
        for index, contractor in enumerate(contractors):
            if contractor.name == "":
                problems.add_error(f"Не задано название подрядчика №{index + 1}")
            elif contractor.name in names:
                if contractor.name not in duplicates:
                    problems.add_error(f"Несколько подрядчиков с одним и тем же названием: {contractor.name}")
                    duplicates.add(contractor.name)
            else:
                names.add(contractor.name)
                for criterion in criteria:
                    if contractor.scores.get(criterion.name, 0) == 0:
                        problems.add_warning(f"{contractor.name}: не задан балл для критерия '{criterion.name}'")
