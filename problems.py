class Problems:
    def __init__(self):
        self._warnings = []
        self._errors = []

    def add_warning(self, warning: str):
        self._warnings.append(warning)

    def add_error(self, error: str):
        self._errors.append(error)

    @property
    def warnings(self) -> list[str]:
        return self._warnings

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def has_warnings(self) -> bool:
        return len(self._warnings) > 0

    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def has_issues(self) -> bool:
        return self.has_errors or self.has_warnings
