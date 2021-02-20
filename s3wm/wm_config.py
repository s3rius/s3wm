"""Default WM configuration."""

import subprocess
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

from frozendict import frozendict
from loguru import logger
from src.layouts.default_tile import DefaultTile
from src.s3wm_types import KeyCombination
from Xlib import X

FRAME_WIDTH = 10


def quit_wm(wm: Any) -> None:
    """Close WM process.

    :param wm: an S3WM instance. (Used Any to avoid circular deps)
    """
    wm.display.close()
    exit(0)  # noqa: WPS421


def startup() -> None:
    """
    Actions to run at startup.

    Function called on startup.
    Actions defined here will be called at WindowManager startup.
    """
    subprocess.Popen("nitrogen --restore", shell=True)
    subprocess.Popen("systemctl --user start music_bg.service", shell=True)


# Default layout mode.
layout = DefaultTile
layout.gaps = 20

# Keyboard global combinations.
# All combinations for layoutManager
combinations = [
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="Return",
        action="$TERM",
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="q",
        action=quit_wm,
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key,
        key="d",
        action="dmenu_run",
    ),
    *layout.get_keys(),
]


EVENT_HANDLER_MAP = frozendict(
    {
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
    },
)

try:  # noqa: WPS229
    conf_path = Path("~/.s3wm_conf.py").expanduser()
    spec = spec_from_file_location("user_config", str(conf_path))
    user_config = module_from_spec(spec)

    from user_config import *  # noqa: F401, F403, WPS347, WPS433
except ImportError:
    logger.error("Can't import user config. Initialized with default.")
