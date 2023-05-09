from month import Month


class Period:
    FIRST_MONTH_TEXT = "Начало"
    LAST_MONTH_TEXT = "Конец"

    OPTIONS = [month.localized_name for month in list(Month)]

    def __init__(self, first_month: Month, last_month: Month):
        self.first_month = first_month
        self.last_month = last_month

    @property
    def months(self) -> list[Month]:
        result = []
        month = self.first_month
        while month != self.last_month:
            result.append(month)
            month = month.next
        result.append(self.last_month)
        return result

    @property
    def length(self) -> int:
        """
        Number of months covered with this period, including its both ends.

        >>> Period(Month.JANUARY, Month.JANUARY).length
        1
        >>> Period(Month.JANUARY, Month.DECEMBER).length
        12
        >>> Period(Month.JANUARY, Month.FEBRUARY).length
        2
        >>> Period(Month.FEBRUARY, Month.JANUARY).length
        12
        """
        count = self.last_month.value - self.first_month.value + 1
        return count if count >= 1 else count + 12
