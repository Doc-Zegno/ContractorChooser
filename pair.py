class Pair:
    EXPECTED_MNEMONIC = "Пд"
    ACTUAL_MNEMONIC = "Пф"

    EXPECTED_TEXT = "По договору"
    ACTUAL_TEXT = "По факту"

    def __init__(self, expected: float = 0.0, actual: float = 0.0):
        self.expected = expected
        self.actual = actual
