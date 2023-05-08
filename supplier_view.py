import streamlit as st

from problems import Problems
from supplier import Supplier
from product import Product
from period import Period


class SupplierView:
    @staticmethod
    def create(supplier: Supplier, products: list[Product], period: Period, view_key: str) -> Problems:
        supplier.name = st.text_input(Supplier.NAME_TEXT, value=supplier.name, key=f"supplier_name_{view_key}").strip()
        # TODO: input for supplies
        return SupplierView._validate(supplier)

    @staticmethod
    def _validate(supplier: Supplier) -> Problems:
        problems = Problems()
        if supplier.name == "":
            problems.add_error("Не задано название поставщика")
        # TODO: additional validation for each product
        return problems
