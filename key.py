from typing import Generic, TypeVar


TValue = TypeVar("TValue")


class Key(Generic[TValue]):
    def __init__(self, name: str, default_value: TValue):
        self._default_value = default_value
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_value(self) -> TValue:
        return self._default_value
