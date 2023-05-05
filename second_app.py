from criteria_view import CriteriaView
from problems_view import ProblemsView
from criterion import Criterion
from state import State
from key import Key


class SecondApp:
    TITLE = "Выбор на основе фактических поставок"
    ID = "second.app"

    _INITIAL_CRITERIA = [
        Criterion("Объем", 0.3),
        Criterion("Цена", 0.4),
        Criterion("Ассортимент", 0.2),
        Criterion("Ритмичность", 0.1),
    ]

    _CRITERIA_KEY = Key(f"{ID}.criteria", default_value=_INITIAL_CRITERIA)

    @staticmethod
    def create():
        criteria = State.get(SecondApp._CRITERIA_KEY)
        criteria_problems = CriteriaView.create(criteria, view_key=SecondApp.ID, disable_name=True)
        ProblemsView.create(criteria_problems)
