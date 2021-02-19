import logging

from loguru import logger

from s3wm.s3wm import S3WM


def main() -> None:
    """Function to run the thing."""
    logger.add("/var/log/s3wm.log", level=logging.DEBUG, catch=True)
    wm = S3WM()
    wm.run()
