import streamlit as st

import collection_utils as cu

from pair_view import PairView
from problems import Problems
from supplier import Supplier
from product import Product
from period import Period
from supply import Supply
from pair import Pair


class SupplierView:
    @staticmethod
    def create(supplier: Supplier, products: list[Product], period: Period, view_key: str) -> Problems:
        supplier.name = st.text_input(Supplier.NAME_TEXT, value=supplier.name, key=f"supplier_name_{view_key}").strip()
        column_width_weights = [len(products)] + [20] * len(products)
        with st.container():
            columns = st.columns(column_width_weights)
            for product_index, product in enumerate(products):
                with columns[product_index + 1]:
                    st.text(product.name)
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[0]:
                st.text("Месяц")
            for product_index in range(len(products)):
                with columns[product_index + 1]:
                    inner_columns = st.columns(2)
                    with inner_columns[0]:
                        st.text(Pair.EXPECTED_TEXT)
                    with inner_columns[1]:
                        st.text(Pair.ACTUAL_TEXT)
        for month_index, month in enumerate(period.months):
            with st.container():
                supply = cu.get(supplier.supplies, month_index, default=Supply())
                columns = st.columns(column_width_weights)
                with columns[0]:
                    st.text(month.localized_name)
                for product_index, product in enumerate(products):
                    with columns[product_index + 1]:
                        quantity = supply.quantities.get(product.name, Pair())
                        PairView.create(quantity, f"quantity_{month_index}_{product_index}")
        return SupplierView._validate(supplier)

    @staticmethod
    def _validate(supplier: Supplier) -> Problems:
        problems = Problems()
        if supplier.name == "":
            problems.add_error("Не задано название поставщика")
        # TODO: additional validation for each product
        return problems
