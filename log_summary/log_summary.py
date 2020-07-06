import re
import pandas as pd
import matplotlib.pyplot as plt
import click

from .defaults import *


FIELDS = ("time", "level", "message")


class IncompatibleRegexPattern(Exception):
    def __init__(self, pattern):
        self.fields = tuple(pattern.groupindex.keys())

    def __str__(self):
        return f"Expected regex patern with groups named {FIELDS} but instead received a pattern with groups {self.fields}"


class NoMatchingLogs(Exception):
    def __str__(self):
        return "There were no logs found matching the regex pattern and log levels specified"


def make_report(logfile, image_path, pattern=DEFAULT_PATTERN, levels=DEFAULT_LEVELS):
    pattern = re.compile(pattern)
    if pattern.groupindex.keys() != set(FIELDS):
        raise IncompatibleRegexPattern(pattern)
    messages = (pattern.match(line) for line in logfile)
    messages = (message.groupdict() for message in messages if message and (message["level"] in levels))

    df = pd.DataFrame(messages, columns=FIELDS)
    if df.size == 0:
        raise NoMatchingLogs()

    df["time"] = pd.to_datetime(df["time"])

    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(image_path)