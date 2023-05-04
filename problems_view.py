import streamlit as st

from problems import Problems


class ProblemsView:
    @staticmethod
    def create(problems: Problems):
        if problems.has_errors:
            st.error(ProblemsView._get_problems_text(problems.errors), icon="🚨")
        if problems.has_warnings:
            st.warning(ProblemsView._get_problems_text(problems.warnings), icon="⚠")

    @staticmethod
    def _get_problems_text(lines: list[str]) -> str:
        assert len(lines) > 0
        if len(lines) == 1:
            return lines[0]
        else:
            return "\n".join(map(lambda l: " * " + l, lines))
