import streamlit as st

from problems import Problems
from product import Product


class ProductsView:
    @staticmethod
    def create(products: list[Product]) -> Problems:
        st.header("Товары")
        column_width_weights = [1, 50, 1]
        with st.container():
            columns = st.columns(column_width_weights)
            with columns[1]:
                st.text(Product.NAME_TEXT)
        for index, product in enumerate(products):
            with st.container():
                columns = st.columns(column_width_weights)
                with columns[0]:
                    st.text(f"{index + 1}.")
                with columns[1]:
                    product.name = st.text_input(Product.NAME_TEXT, key=f"product_name_{index}",
                                                 value=product.name, label_visibility="collapsed").strip()
                with columns[-1]:
                    def remove_product(i: int = index):
                        products.pop(i)

                    st.button(":x:", key=f"product_remove_{index}", help="Удалить товар",
                              on_click=remove_product)
        st.button(":heavy_plus_sign:", key="product_add", help="Добавить товар",
                  on_click=lambda: products.append(Product()))
        return ProductsView._validate_products(products)

    @staticmethod
    def _validate_products(products: list[Product]) -> Problems:
        problems = Problems()
        if len(products) == 0:
            problems.add_error("Не задано ни одного товара")
            return problems
        duplicates = set()
        names = set()
        for index, product in enumerate(products):
            if product.name == "":
                problems.add_error(f"Не задано название товара №{index + 1}")
            elif product.name in names:
                if product.name not in duplicates:
                    problems.add_error(f"Несколько товаров с одним и тем же названием: {product.name}")
                    duplicates.add(product.name)
            else:
                names.add(product.name)
        return problems
