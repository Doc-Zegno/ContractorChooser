from contractors_view import ContractorsView
from criteria_view import CriteriaView
from problems_view import ProblemsView
from result_view import ResultView
from state import State


class FirstApp:
    TITLE = "Выбор на основе экспертных оценок"

    @staticmethod
    def create():
        criteria = State.get_criteria()
        criteria_problems = CriteriaView.create(criteria)
        ProblemsView.create(criteria_problems)
        contractors = State.get_contractors()
        contractors_problems = ContractorsView.create(criteria_problems.has_errors, criteria, contractors)
        ProblemsView.create(contractors_problems)
        has_problems = criteria_problems.has_issues or contractors_problems.has_issues
        ResultView.create(has_problems, criteria, contractors)
