"""
         _____
   _____|__  /_      __ ____ ___
  / ___/ /_ <| | /| / // __ `__ \
 (__  )___/ /| |/ |/ // / / / / /
/____//____/ |__/|__//_/ /_/ /_/

S3rius window manager.
Highly customizable, super simple.
"""
import logging

from src.s3wm import S3WM


def setup_logging():
    logging.basicConfig(
        format="[%(levelname)8s] %(msg)s {%(filename)s:%(lineno)s}", level=logging.DEBUG
    )


if __name__ == "__main__":
    setup_logging()
    wm = S3WM()
    wm.run()
