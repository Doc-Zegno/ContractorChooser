from enum import IntEnum, unique


_LOCALIZED_NAMES = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]


@unique
class Month(IntEnum):
    JANUARY = 0
    FEBRUARY = 1
    MARCH = 2
    APRIL = 3
    MAY = 4
    JUNE = 5
    JULY = 6
    AUGUST = 7
    SEPTEMBER = 8
    OCTOBER = 9
    NOVEMBER = 10
    DECEMBER = 11

    @property
    def localized_name(self) -> str:
        return _LOCALIZED_NAMES[self.value]

    @staticmethod
    def parse(text: str) -> "Month":
        index = _LOCALIZED_NAMES.index(text)
        return Month(index)
