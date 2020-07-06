from typing import Pattern

from .types import LogMessage

class IncompatibleRegexPattern(Exception):
    def __init__(self, pattern: Pattern):
        self.fields = tuple(pattern.groupindex.keys())

    def __str__(self) -> str:
        return f"Expected regex patern with groups named {LogMessage._fields} " \
            f"but instead received a pattern with groups {self.fields}"


class NoMatchingLogs(Exception):
    def __str__(self) -> str:
        return "There were no logs found matching the regex pattern and log " \
            "levels specified"