import streamlit as st
import math

import collection_utils as cu
import dataframe_utils as du

from pair_view import PairView
from problems import Problems
from supplier import Supplier
from product import Product
from period import Period
from supply import Supply
from state import State
from pair import Pair
from key import Key


class SupplierView:
    @staticmethod
    def create(supplier: Supplier, products: list[Product], period: Period, view_key: str) -> Problems:
        supplier.name = st.text_input(Supplier.NAME_TEXT, value=supplier.name, key=f"supplier_name_{view_key}").strip()
        column_width_weights = [len(products)] + [20] * len(products)
        st.markdown("#### Поставки")
        supplies_file_changed_key = Key(f"{view_key}.supplies.file.changed", default_value=False)
        supplies_file = st.file_uploader("Загрузить поставки", key=f"supplies_upload_{view_key}", type=["csv", "xlsx"],
                                         on_change=lambda: State.set(supplies_file_changed_key))
        if State.reset(supplies_file_changed_key) and supplies_file is not None:
            dataframe = du.parse_dataframe(supplies_file)
            uploaded_supplies = Supply.from_dataframe(dataframe, products)
            supplier.supplies.clear()
            supplier.supplies.extend(uploaded_supplies)
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
        cu.extend(supplier.supplies, until_length=period.length, with_value=Supply)
        for supply, month in zip(supplier.supplies, period.months):
            with st.container():
                columns = st.columns(column_width_weights)
                with columns[0]:
                    st.text(month.localized_name)
                for product_index, product in enumerate(products):
                    with columns[product_index + 1]:
                        quantity = cu.get_or_put(supply.quantities, key=product.name, default=Pair)
                        PairView.create(quantity)
        # Supplies are always available for downloading since there's no validation for them at all
        supplies_dataframe = Supply.to_dataframe(supplier.supplies, products, period)
        supplies_as_excel = du.convert_to_excel(supplies_dataframe)
        supplies_as_csv = du.convert_to_csv(supplies_dataframe)
        st.download_button("Скачать поставки (Excel)", supplies_as_excel, key=f"supplies_download_excel_{view_key}",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           file_name=Supply.EXCEL_FILE_NAME)
        st.download_button("Скачать поставки (CSV)", supplies_as_csv, key=f"supplies_download_csv_{view_key}",
                           file_name=Supply.CSV_FILE_NAME, mime="text/csv")
        column_width_weights = column_width_weights[1:]
        st.markdown("#### Цены товаров")
        with st.container():
            columns = st.columns(column_width_weights)
            for product_index, product in enumerate(products):
                with columns[product_index]:
                    st.text(product.name)
        with st.container():
            columns = st.columns(column_width_weights)
            for product_index in range(len(products)):
                with columns[product_index]:
                    inner_columns = st.columns(2)
                    with inner_columns[0]:
                        st.text(Pair.EXPECTED_TEXT)
                    with inner_columns[1]:
                        st.text(Pair.ACTUAL_TEXT)
        with st.container():
            columns = st.columns(column_width_weights)
            for product_index, product in enumerate(products):
                with columns[product_index]:
                    price = cu.get_or_put(supplier.prices, key=product.name, default=Pair)
                    PairView.create(price)
        return SupplierView._validate(supplier, products)

    @staticmethod
    def _validate(supplier: Supplier, products: list[Product]) -> Problems:
        problems = Problems()
        if supplier.name == "":
            problems.add_error("Не задано название поставщика")
        # Intentionally skipping the check of supplies in order to avoid being overflown with warnings
        for product in products:
            price = cu.get_or_put(supplier.prices, key=product.name, default=Pair)
            if math.isclose(price.expected, 0.0):
                problems.add_warning(f"{product.name}: не задана цена по договору")
            if math.isclose(price.actual, 0.0):
                problems.add_warning(f"{product.name}: не задана цена по факту")
        return problems
