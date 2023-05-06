from month import Month


class Period:
    FIRST_MONTH_TEXT = "Начало"
    LAST_MONTH_TEXT = "Конец"

    OPTIONS = [month.localized_name for month in list(Month)]

    def __init__(self, first_month: Month, last_month: Month):
        self.first_month = first_month
        self.last_month = last_month
