from typing import Optional
import streamlit as st
import pandas as pd
import math


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

    def calculate_total_score(self, criteria: list[Criterion]) -> float:
        return sum(map(lambda criterion: self.scores.get(criterion.name, 0) * criterion.value, criteria))

    @staticmethod
    def find_best(criteria: list[Criterion], contractors: list["Contractor"]) -> list["Contractor"]:
        total_scores = [contractor.calculate_total_score(criteria) for contractor in contractors]
        max_score = max(total_scores)
        return [contractor for contractor, total_score in zip(contractors, total_scores) if total_score == max_score]

    @staticmethod
    def to_dataframe(criteria: list[Criterion], contractors: list["Contractor"]) -> pd.DataFrame:
        scores = {criterion.name: [] for criterion in criteria}
        names = []
        for contractor in contractors:
            names.append(contractor.name)
            for criterion in criteria:
                score = contractor.scores.get(criterion.name, 0)
                scores[criterion.name].append(score)
        data = {Contractor.NAME_TEXT: names, **scores}
        return pd.DataFrame(data)

    @staticmethod
    def from_dataframe(criteria: list[Criterion], dataframe: pd.DataFrame) -> list["Contractor"]:
        return [Contractor._from_row(criteria, row) for _, row in dataframe.iterrows()]

    @staticmethod
    def _from_row(criteria: list[Criterion], row: pd.Series) -> "Contractor":
        scores = {criterion.name: row[criterion.name] for criterion in criteria}
        return Contractor(row[Contractor.NAME_TEXT], scores)


class Problems:
    def __init__(self):
        self._warnings = []
        self._errors = []

    def add_warning(self, warning: str):
        self._warnings.append(warning)

    def add_error(self, error: str):
        self._errors.append(error)

    @property
    def warnings(self) -> list[str]:
        return self._warnings

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def has_warnings(self) -> bool:
        return len(self._warnings) > 0

    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def has_issues(self) -> bool:
        return self.has_errors or self.has_warnings


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


def validate_criteria(criteria: list[Criterion]) -> Problems:
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


def create_criteria_view(criteria: list[Criterion]) -> Problems:
    st.header("Критерии")
    csv_file = st.file_uploader("Загрузить критерии", type="csv", on_change=State.set_criteria_file_changed)
    if State.reset_criteria_file_changed() and csv_file is not None:
        dataframe = pd.read_csv(csv_file, index_col=0)
        uploaded_criteria = Criterion.from_dataframe(dataframe)
        criteria.clear()
        criteria.extend(uploaded_criteria)
    column_width_weights = [1, 30, 20, 1]
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
                                               label_visibility="collapsed").strip()
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
    problems = validate_criteria(criteria)
    if not problems.has_errors:
        serialized_criteria = convert_to_csv(Criterion.to_dataframe(criteria))
        st.download_button("Скачать критерии", serialized_criteria,
                           file_name=Criterion.FILE_NAME,
                           mime="text/csv")
    st.dataframe(Criterion.to_dataframe(criteria))  # TODO: for debug purposes only, remove later
    return problems


def validate_contractors(problems: Problems, criteria: list[Criterion], contractors: list[Contractor]):
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


def create_contractors_view(has_errors: bool, criteria: list[Criterion], contractors: list[Contractor]) -> Problems:
    st.header("Подрядчики")
    problems = Problems()
    if has_errors or len(criteria) == 0:
        problems.add_error("Невозможно отобразить данные о подрядчиках, пока не заданы корректные критерии")
        return problems
    csv_file = st.file_uploader("Загрузить подрядчиков", type="csv", on_change=State.set_contractors_file_changed)
    if State.reset_contractors_file_changed() and csv_file is not None:
        dataframe = pd.read_csv(csv_file, index_col=0)
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
                        old_score = contractor.scores.get(criterion.name, 0)
                        new_score = st.number_input(criterion.name, value=old_score, label_visibility="collapsed",
                                                    key=f"contractor_{contractor_index}_criterion_{criterion_index}",
                                                    min_value=0, max_value=5)
                        contractor.scores[criterion.name] = new_score
            with columns[-2]:
                st.text(f"{contractor.calculate_total_score(criteria):.2f}")
            with columns[-1]:
                def remove_contractor(i: int = contractor_index):
                    contractors.pop(i)
                st.button(":x:", key=f"contractor_remove_{contractor_index}", help="Удалить подрядчика",
                          on_click=remove_contractor)
    st.button(":heavy_plus_sign:", key="contractor_add", help="Добавить подрядчика",
              on_click=lambda: contractors.append(Contractor()))
    validate_contractors(problems, criteria, contractors)
    if not problems.has_errors:
        serialized_contractors = convert_to_csv(Contractor.to_dataframe(criteria, contractors))
        st.download_button("Скачать подрядчиков", serialized_contractors,
                           file_name=Contractor.FILE_NAME,
                           mime="text/csv")
    st.dataframe(Contractor.to_dataframe(criteria, contractors))  # TODO: for debug purposes only, remove later
    return problems


def get_best_contractor_text(best_contractors: list[Contractor]) -> str:
    assert len(best_contractors) > 0
    if len(best_contractors) == 1:
        return f"Лучший подрядчик: {best_contractors[0].name}"
    else:
        markdown = "Лучшие подрядчики:"
        for contractor in best_contractors:
            markdown += f"\n * {contractor.name}"
        return markdown


def create_result_view(has_problems: bool, criteria: list[Criterion], contractors: list[Contractor]):
    st.header("Результат")
    if has_problems:
        st.info("Устраните выявленные проблемы, чтобы рассчитать наилучшего подрядчика")
        return
    if st.button("Рассчитать лучшего подрядчика", key="contractor_calculate_best"):
        best_contractors = Contractor.find_best(criteria, contractors)
        st.success(get_best_contractor_text(best_contractors))


def get_problems_text(lines: list[str]) -> str:
    assert len(lines) > 0
    if len(lines) == 1:
        return lines[0]
    else:
        return "\n".join(map(lambda l: " * " + l, lines))


def create_problems_view(problems: Problems):
    if problems.has_errors:
        st.error(get_problems_text(problems.errors))
    if problems.has_warnings:
        st.warning(get_problems_text(problems.warnings))


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


def main():
    st.set_page_config(layout="wide")
    enable_vertical_alignment()
    criteria = create_initial_criteria()
    criteria_problems = create_criteria_view(criteria)
    create_problems_view(criteria_problems)
    contractors = create_initial_contractors()
    contractors_problems = create_contractors_view(criteria_problems.has_errors, criteria, contractors)
    create_problems_view(contractors_problems)
    has_problems = criteria_problems.has_issues or contractors_problems.has_issues
    create_result_view(has_problems, criteria, contractors)


main()
