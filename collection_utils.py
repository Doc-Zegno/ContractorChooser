from typing import TypeVar, Callable


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def get_or_put(values: dict[K, V], key: K, default: Callable[[], V]) -> V:
    """
    If the dictionary doesn't contain a required key, generate and insert new value.
    After that, return a value associated with this key.
    New values are evaluated lazily.

    >>> features = {"price": 100, "quality": 50}
    >>> get_or_put(features, "quality", default=lambda: -1)
    50
    >>> get_or_put(features, "availability", default=lambda: -1)
    -1
    >>> features["availability"]
    -1
    """
    if key not in values:
        values[key] = default()
    return values[key]


def extend(values: list[T], until_length: int, with_value: Callable[[], T]):
    """
    Extend the list using a value generator
    until a required length is reached.
    New values are evaluated lazily.

    >>> numbers = [1, 2, 3]
    >>> extend(numbers, until_length=5, with_value=lambda: -1)
    >>> numbers
    [1, 2, 3, -1, -1]
    """
    extra_length = until_length - len(values)
    if extra_length <= 0:
        return
    for _ in range(extra_length):
        values.append(with_value())
