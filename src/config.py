import subprocess

from src.layouts.default_tile import TileLayout
from src.s3wm_types import KeyCombination
from src.utils import kill_focused_window
from Xlib import X

FRAME_WIDTH = 10


def quit_wm(wm):
    wm.display.close()
    exit(0)


def startup():
    """
    Function that will be called on startup
    :return:
    """
    subprocess.Popen("nitrogen --restore", shell=True)
    subprocess.Popen("systemctl --user start music_bg.service", shell=True)


# Default layout mode.
layout = TileLayout
layout.inner_gaps = 10
layout.outer_gaps = 40

# Keyboard global combinations.
# All combinations for layoutManager
combinations = [
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="Return",
        action="konsole",
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask, key="q", action=quit_wm
    ),
    KeyCombination(modifiers=KeyCombination.default_mod_key, key="e", action="thunar"),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key, key="d", action="dmenu_run"
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="c",
        action=kill_focused_window,
    ),
    *layout.get_keys(),
]

EVENT_HANDLER_MAP = {
    X.KeyPress: "handle_keypress",
    X.ButtonPress: None,
    X.MotionNotify: None,
    X.ButtonRelease: None,
    X.MapRequest: "handle_map",
    X.ConfigureRequest: None,
    X.UnmapNotify: None,
    X.EnterNotify: None,
    X.LeaveNotify: None,
    X.DestroyNotify: "handle_destroy",
    X.MapNotify: None,
}
