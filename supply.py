from typing import Optional

from pair import Pair


class Supply:
    MONTH_TEXT = "Месяц"

    def __init__(self, quantities: Optional[dict[str, Pair]] = None):
        self.quantities = quantities if quantities is not None else {}
