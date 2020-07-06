import re
import pandas as pd
import matplotlib.pyplot as plt
import click

from .defaults import *


def make_report(logfile, image_path, pattern=DEFAULT_PATTERN, levels=DEFAULT_LEVELS):
    pattern = re.compile(pattern)
    messages = (pattern.match(line) for line in logfile)
    messages = (message.groups() for message in messages if message and (message["level"] in levels))

    df = pd.DataFrame(messages, columns=["time", "level", "message"])
    df["time"] = pd.to_datetime(df["time"])

    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(image_path)