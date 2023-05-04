from contractors_view import ContractorsView
from criteria_view import CriteriaView
from problems_view import ProblemsView
from result_view import ResultView
from contractor import Contractor
from criterion import Criterion
from state import State
from key import Key


class FirstApp:
    TITLE = "Выбор на основе экспертных оценок"
    ID = "first.app"

    _INITIAL_CONTRACTORS = [
        Contractor("Рога и Копыта", {"Цена": 3, "Качество": 4, "Удаленность": 2})
    ]

    _INITIAL_CRITERIA = [
        Criterion("Цена", 0.35),
        Criterion("Качество", 0.55),
        Criterion("Удаленность", 0.1),
    ]

    _CONTRACTORS_KEY = Key(f"{ID}.contractors", default_value=_INITIAL_CONTRACTORS)
    _CRITERIA_KEY = Key(f"{ID}.criteria", default_value=_INITIAL_CRITERIA)

    @staticmethod
    def create():
        criteria = State.get(FirstApp._CRITERIA_KEY)
        criteria_problems = CriteriaView.create(criteria, view_key=FirstApp.ID)
        ProblemsView.create(criteria_problems)
        contractors = State.get(FirstApp._CONTRACTORS_KEY)
        contractors_problems = ContractorsView.create(criteria_problems.has_errors, criteria, contractors)
        ProblemsView.create(contractors_problems)
        has_problems = criteria_problems.has_issues or contractors_problems.has_issues
        ResultView.create(has_problems, criteria, contractors)
