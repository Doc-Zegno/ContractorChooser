from typing import TypeVar


T = TypeVar("T")


def get(values: list[T], index: int, default: T) -> T:
    """
    Return an element at the specified index if it exists
    and a default value otherwise.
    """
    return values[index] if index < len(values) else default
