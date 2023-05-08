import streamlit as st

from problems import Problems
from supplier import Supplier
from product import Product
from period import Period
from pair import Pair


class SupplierView:
    @staticmethod
    def create(supplier: Supplier, products: list[Product], period: Period, view_key: str) -> Problems:
        supplier.name = st.text_input(Supplier.NAME_TEXT, value=supplier.name, key=f"supplier_name_{view_key}").strip()
        column_width_weights = [1, 20]
        with st.container():
            outer_columns = st.columns(column_width_weights)
            with outer_columns[1]:
                product_columns = st.columns(len(products))
                for product_index, product in enumerate(products):
                    with product_columns[product_index]:
                        st.text(product.name)
        with st.container():
            outer_columns = st.columns(column_width_weights)
            with outer_columns[0]:
                st.text("Месяц")
            with outer_columns[1]:
                pair_columns = st.columns(len(products) * 2)
                for product_index in range(len(products)):
                    with pair_columns[2 * product_index]:
                        st.text(Pair.EXPECTED_TEXT)
                    with pair_columns[2 * product_index + 1]:
                        st.text(Pair.ACTUAL_TEXT)
        for month_index, month in enumerate(period.months):
            with st.container():
                outer_columns = st.columns(column_width_weights)
                with outer_columns[0]:
                    st.text(month.localized_name)
                with outer_columns[1]:
                    pass  # TODO
        return SupplierView._validate(supplier)

    @staticmethod
    def _validate(supplier: Supplier) -> Problems:
        problems = Problems()
        if supplier.name == "":
            problems.add_error("Не задано название поставщика")
        # TODO: additional validation for each product
        return problems
