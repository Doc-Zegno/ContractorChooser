import streamlit as st


class Criterion:
    def __init__(self, name: str = "", value: float = 0.0):
        self.value = value
        self.name = name


@st.cache_resource
def create_initial_criteria() -> list[Criterion]:
    return [
        Criterion("Цена", 0.35),
        Criterion("Качество", 0.65),
        Criterion("Удаленность", 0.1),
    ]


def create_criteria_view(criteria: list[Criterion]):
    st.header("Критерии")
    column_width_weights = [1, 8, 8, 1]
    with st.container():
        columns = st.columns(column_width_weights)
        with columns[1]:
            st.text("Название")
        with columns[2]:
            st.text("Значимость", help="Дробный вес от 0 до 1")
    for index, criterion in enumerate(criteria):
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[0]:
                st.text(f"{index + 1}.")
            with columns[1]:
                criterion.name = st.text_input("Название", key=f"criterion_name_{index}", value=criterion.name,
                                               label_visibility="collapsed")
            with columns[2]:
                criterion.value = st.number_input("Вес", key=f"criterion_value_{index}", value=criterion.value,
                                                  min_value=0.0, max_value=1.0, label_visibility="collapsed")
            with columns[3]:
                st.button(":x:", key=f"criterion_remove_{index}", help="Удалить критерий",
                          on_click=lambda: criteria.pop(index))
    st.button(":heavy_plus_sign:", key="criterion_add", help="Добавить критерий",
              on_click=lambda: criteria.append(Criterion()))
    st.dataframe(criteria)


def main():
    criteria = create_initial_criteria()
    create_criteria_view(criteria)


main()
