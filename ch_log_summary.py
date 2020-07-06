#!/usr/bin/python3

import re
import pandas as pd
import matplotlib.pyplot as plt


LOG_LOCACTION = "/var/log/clickhouse-server/clickhouse-server.log"
PATTERN = re.compile(r"(?P<time>[\d\.]+ [\d\.:]+) .+ <(?P<level>\w+)> (?P<message>.+)$")
LEVELS = ("Error", "Warning")
OUTPUT = "event_times.png"


with open(LOG_LOCACTION) as logfile:
    messages = (PATTERN.match(line) for line in logfile)
    messages = (message.groups() for message in messages if message and (message["level"] in LEVELS))

    df = pd.DataFrame(messages, columns=["time", "level", "message"])
    df["time"] = pd.to_datetime(df["time"])

    print(df.groupby("level").count())
    df["time"].hist(by=df["level"])
    plt.savefig(OUTPUT)
