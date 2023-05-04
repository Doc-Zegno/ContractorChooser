from typing import TypeVar
import streamlit as st

from key import Key


TValue = TypeVar("TValue")


class State:
    _KEY_COUNTER_TEXT = "key_counter"
    _IS_CRITERIA_FILE_CHANGED_TEXT = "is_criteria_file_changed"
    _IS_CONTRACTORS_FILE_CHANGED_TEXT = "is_contractors_file_changed"

    @staticmethod
    def get(key: Key[TValue]) -> TValue:
        return State._get(key.name, key.default_value)

    @staticmethod
    def _get(value_name: str, default_value):
        if value_name not in st.session_state:
            st.session_state[value_name] = default_value
        return st.session_state[value_name]

    @staticmethod
    def generate_key() -> str:
        """
        Generate a string which can be used as a key for any widget.
        Guaranteed to be unique, also changes every time
        the application page is refreshed.
        """
        if State._KEY_COUNTER_TEXT not in st.session_state:
            st.session_state[State._KEY_COUNTER_TEXT] = 0
        index = st.session_state[State._KEY_COUNTER_TEXT]
        st.session_state[State._KEY_COUNTER_TEXT] += 1
        return f"generated_key_{index}"

    @staticmethod
    def set_criteria_file_changed():
        State._set(State._IS_CRITERIA_FILE_CHANGED_TEXT)

    @staticmethod
    def reset_criteria_file_changed() -> bool:
        """
        Atomically check whether the uploaded criteria file has recently changed
        and reset this status flag back to False, so the subsequent
        checks will fail until the next change of file.

        :return: True if uploaded criteria file has changed since the previous reset.
        """
        return State._reset(State._IS_CRITERIA_FILE_CHANGED_TEXT)

    @staticmethod
    def set_contractors_file_changed():
        State._set(State._IS_CONTRACTORS_FILE_CHANGED_TEXT)

    @staticmethod
    def reset_contractors_file_changed():
        """
        Atomically check whether the uploaded contractors file has recently changed
        and reset this status flag back to False, so the subsequent
        checks will fail until the next change of file.

        :return: True if uploaded contractors file has changed since the previous reset.
        """
        return State._reset(State._IS_CONTRACTORS_FILE_CHANGED_TEXT)

    @staticmethod
    def _set(flag_name: str):
        st.session_state[flag_name] = True

    @staticmethod
    def _reset(flag_name: str) -> bool:
        if flag_name not in st.session_state:
            return False
        has_flag_been_set = st.session_state[flag_name]
        st.session_state[flag_name] = False
        return has_flag_been_set
