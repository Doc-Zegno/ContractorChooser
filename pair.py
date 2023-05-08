class Pair:
    EXPECTED_TEXT = "По договору"
    ACTUAL_TEXT = "По факту"

    def __init__(self, expected: float, actual: float):
        self.expected = expected
        self.actual = actual
