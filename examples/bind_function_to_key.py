from subprocess import Popen

import requests
from Xlib import X

from s3wm.layouts import DefaultTile
from s3wm.s3wm import S3WM
from s3wm_core import KeyCombination, kill_wm

layout = DefaultTile  # Default tile layout.
layout.gaps = 10


def send_request_to_httpbin(_: S3WM) -> None:
    """Send request to server and notify about the state."""
    # Send response.
    response = requests.get("https://httpbin.org/get")
    message = "HTTPBIN is down."
    if response.ok:
        message = "HTTPBIN is alive."

    # Send notification about status
    Popen(
        f'notify-send -u critical -a "HTTPBIN status" "HTTPBIN status" "{message}"',
        shell=True,
    )


combinations = [
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="Return",
        action="konsole",  # This is a bash command.
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="q",
        action=kill_wm,  # This action kills current window manager.
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="h",
        action=send_request_to_httpbin,
    ),
    *layout.get_keys(),
]
