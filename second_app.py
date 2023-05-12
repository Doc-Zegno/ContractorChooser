from suppliers_view import SuppliersView
from criteria_view import CriteriaView
from products_view import ProductsView
from problems_view import ProblemsView
from period_view import PeriodView
from criterion import Criterion
from supplier import Supplier
from product import Product
from period import Period
from month import Month
from state import State
from key import Key


class SecondApp:
    TITLE = "Выбор на основе фактических поставок"
    ID = "second.app"

    _INITIAL_SUPPLIERS = [
        Supplier("Рога и Копыта"),
        Supplier("Геркулес"),
    ]

    _INITIAL_CRITERIA = [
        Criterion("Объем", 0.3),
        Criterion("Цена", 0.4),
        Criterion("Ассортимент", 0.2),
        Criterion("Ритмичность", 0.1),
    ]

    _INITIAL_PRODUCTS = [
        Product("А"),
        Product("Б"),
        Product("В"),
        Product("Г"),
    ]

    _INITIAL_PERIOD = Period(Month.JANUARY, Month.DECEMBER)

    _SUPPLIERS_KEY = Key(f"{ID}.suppliers", default_value=_INITIAL_SUPPLIERS)
    _CRITERIA_KEY = Key(f"{ID}.criteria", default_value=_INITIAL_CRITERIA)
    _PRODUCTS_KEY = Key(f"{ID}.products", default_value=_INITIAL_PRODUCTS)
    _PERIOD_KEY = Key(f"{ID}.period", default_value=_INITIAL_PERIOD)

    @staticmethod
    def create():
        criteria = State.get(SecondApp._CRITERIA_KEY)
        criteria_problems = CriteriaView.create(criteria, view_key=SecondApp.ID,
                                                disable_name=True, disable_upload=True, disable_add_remove=True)
        ProblemsView.create(criteria_problems)
        products = State.get(SecondApp._PRODUCTS_KEY)
        products_problems = ProductsView.create(products)
        ProblemsView.create(products_problems)
        period = State.get(SecondApp._PERIOD_KEY)
        period_problems = PeriodView.create(period)
        ProblemsView.create(period_problems)
        suppliers = State.get(SecondApp._SUPPLIERS_KEY)
        suppliers_problems = SuppliersView.create(suppliers, products, period,
                                                  has_errors=products_problems.has_errors or period_problems.has_errors)
        ProblemsView.create(suppliers_problems)
