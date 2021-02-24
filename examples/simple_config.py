from Xlib import X

from s3wm.layouts import DefaultTile
from s3wm_core import KeyCombination, kill_wm

layout = DefaultTile  # Default tile layout.
layout.gaps = 10

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
    *layout.get_keys(),
]
