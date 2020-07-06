import click

from .defaults import DEFAULT_PATTERN, DEFAULT_IMAGE, DEFAULT_LEVELS
from .log_summary import make_report


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
