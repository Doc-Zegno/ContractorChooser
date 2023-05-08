import streamlit as st

from supplier_view import SupplierView
from problems_view import ProblemsView
from problems import Problems
from supplier import Supplier
from product import Product
from period import Period


class SuppliersView:
    @staticmethod
    def create(suppliers: list[Supplier], products: list[Product], period: Period, has_errors: bool) -> Problems:
        st.header("Поставщики")
        if has_errors:
            problems = Problems()
            problems.add_error("Невозможно задать поставщиков, пока не исправлены ошибки выше")
            return problems
        has_issues = False
        for supplier_index, supplier in enumerate(suppliers):
            with st.container():
                columns = st.columns([1, 7])
                with columns[0]:
                    st.markdown(f"### Поставщик №{supplier_index + 1}")
                with columns[1]:
                    def remove_supplier(i: int = supplier_index):
                        suppliers.pop(i)

                    st.button(":x:", key=f"supplier_remove_{supplier_index}", help="Удалить поставщика",
                              on_click=remove_supplier)
            problems = SupplierView.create(supplier, products, period, view_key=f"supplier_{supplier_index}")
            has_issues = has_issues or problems.has_issues
            ProblemsView.create(problems)
        st.button(":heavy_plus_sign:", key="supplier_add", help="Добавить поставщика",
                  on_click=lambda: suppliers.append(Supplier()))
        return SuppliersView._validate(suppliers, has_issues)

    @staticmethod
    def _validate(suppliers: list[Supplier], has_issues: bool) -> Problems:
        problems = Problems()
        if len(suppliers) == 0:
            problems.add_error("Не задано ни одного поставщика")
        if has_issues:
            problems.add_error("При заполнении данных поставщиков допущены ошибки")
        return problems
