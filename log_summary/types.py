from typing import NamedTuple


class LogMessage(NamedTuple):
    time: str
    level: str
    message: str