from typing import Optional

from supply import Supply
from pair import Pair


class Supplier:
    NAME_TEXT = "Название"

    def __init__(
            self,
            name: str = "",
            supplies: Optional[list[Supply]] = None,
            prices: Optional[dict[str, Pair]] = None
    ):
        self.supplies = supplies if supplies is not None else []
        self.prices = prices if prices is not None else {}
        self.name = name
