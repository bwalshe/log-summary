import re
import pandas as pd
import matplotlib.pyplot as plt
import click
from typing import NamedTuple, Pattern, Iterable

from .defaults import *

class LogMessage(NamedTuple):
    time: str
    level: str
    message: str


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


def make_report(logfile: Iterable[str], image_path: str, 
        pattern: str = DEFAULT_PATTERN, levels=DEFAULT_LEVELS) -> None:
    pattern = re.compile(pattern)
    if pattern.groupindex.keys() != set(LogMessage._fields):
        raise IncompatibleRegexPattern(pattern)
    messages = (pattern.match(line) for line in logfile)
    messages = (message.groupdict() for message in messages if message and (message["level"] in levels))

    df = pd.DataFrame(messages, columns=LogMessage._fields)
    if df.size == 0:
        raise NoMatchingLogs()

    df["time"] = pd.to_datetime(df["time"])
    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(image_path)