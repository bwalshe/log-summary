#!/usr/bin/python3

import re
import pandas as pd
import matplotlib.pyplot as plt
import click


DEFAULT_PATTERN = r"(?P<time>[\d\.]+ [\d\.:]+) .+ <(?P<level>\w+)> (?P<message>.+)$"
DEFAULT_LEVELS = ["Error", "Warning"]
DEFAULT_IMAGE = "event_times.png"


def make_report(logfile, image_path, pattern=DEFAULT_PATTERN, levels=DEFAULT_LEVELS):
    pattern = re.compile(pattern)
    messages = (pattern.match(line) for line in logfile)
    messages = (message.groups() for message in messages if message and (message["level"] in levels))

    df = pd.DataFrame(messages, columns=["time", "level", "message"])
    df["time"] = pd.to_datetime(df["time"])

    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(image_path)


@click.command()
@click.argument('log_path')
@click.option("--pattern", "-p", default=DEFAULT_PATTERN, type=str,  help="Regex pattern to extract the <time> <level> and <message> from a log line")
@click.option("--levels", "-l", type=str, default=",".join(DEFAULT_LEVELS), help="Comma seperated list of log levels to use")
@click.option("--image", default=DEFAULT_IMAGE, help="Name of the image file to create")
def run(log_path, image, pattern, levels):
    "Read lines from LOG_PATH which match the given regex pattern, and count the types of message seen."
    levels = levels.split(",")
    with open(log_path) as logfile:
        make_report(logfile, image, pattern, levels)


if __name__ == "__main__":
    run()
