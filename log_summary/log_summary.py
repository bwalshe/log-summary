import re
import pandas as pd
import matplotlib.pyplot as plt
import click
from typing import Iterable, Optional, Sequence

from .defaults import *
from .exceptions import IncompatibleRegexPattern, NoMatchingLogs
from .types import LogMessage


class MessageParser:
    def __init__(self, pattern:str):
        self._pattern = re.compile(pattern)
        if self._pattern.groupindex.keys() != set(LogMessage._fields):
            raise IncompatibleRegexPattern(self._pattern)
    
    def _parse_line(self, line: str) -> Optional[LogMessage]:
        match = self._pattern.match(line)
        if match:
            return LogMessage(**match.groupdict())


    def parse(self, lines: Iterable[str]) -> Sequence[LogMessage]:
        for line in lines:
            message = self._parse_line(line)
            if message:
                yield message


def make_report(logfile: Iterable[str], image_path: str, 
        pattern: str = DEFAULT_PATTERN, levels=DEFAULT_LEVELS) -> None:
    
    parser = MessageParser(pattern)
    messages = parser.parse(logfile)
    messages = (m for m in messages if m.level in levels)

    df = pd.DataFrame(messages, columns=LogMessage._fields)
    if df.size == 0:
        raise NoMatchingLogs()

    df["time"] = pd.to_datetime(df["time"])
    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(image_path)