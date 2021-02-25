import logging
from argparse import ArgumentParser, Namespace
from enum import Enum
from importlib.metadata import version
from sys import stdout

from loguru import logger

from s3wm.s3wm import S3WM


class Loglevel(Enum):
    """Different log levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO  # noqa: WPS110
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self) -> str:
        return str(self.name)

    @staticmethod
    def from_string(level: str) -> "Loglevel":
        """
        Translate string to enum.

        :param level: level's string representation.
        :return: parsed enum if any.
        :raises ValueError: if can't find a value.
        """
        try:
            return Loglevel[level]
        except KeyError:
            raise ValueError("Unknown level")


def parse_arguments() -> Namespace:
    """
    Parse CLI arguments passed to s3wm.

    :return: namespace with parsed args.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        dest="version",
    )
    parser.add_argument(
        "--log-level",
        "-l",
        dest="log_level",
        type=Loglevel.from_string,
        choices=list(Loglevel),
        default=Loglevel.INFO,
    )
    return parser.parse_args()


def main() -> None:
    """Function to run the thing."""
    args = parse_arguments()
    if args.version:
        s3wm_version = version("s3wm")
        print(f"S3WM version: {s3wm_version}")  # noqa: WPS421
        return
    logger.remove()
    logger.add(stdout, level=args.log_level.value)
    wm = S3WM()
    wm.run()
