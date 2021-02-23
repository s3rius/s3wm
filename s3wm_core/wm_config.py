"""Default WM configuration."""
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from frozendict import frozendict
from loguru import logger
from Xlib import X

from s3wm.layouts.default_tile import DefaultTile
from s3wm_core.key_combination import KeyCombination
from s3wm_core.keymap import kill_wm

FRAME_WIDTH = 10


def startup() -> None:
    """
    Actions to run at startup.

    Function called on startup.
    Actions defined here will be called at WindowManager startup.
    """
    subprocess.Popen("nitrogen --restore", shell=True)


# Default layout mode.
layout = DefaultTile
layout.gaps = 10

# Keyboard global combinations.
# All combinations for layoutManager
combinations = [
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="Return",
        action="xterm",
    ),
    KeyCombination(
        modifiers=KeyCombination.default_mod_key | X.ShiftMask,
        key="q",
        action=kill_wm,
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

module_name = "user_config"
conf_path = Path("~/.s3wm_conf.py").expanduser()

try:  # noqa: WPS229
    if not conf_path.exists():
        raise ImportError
    spec = spec_from_file_location("user_config", str(conf_path))
    module = module_from_spec(spec)
    if not spec.loader:
        raise ImportError
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    from user_config import *  # noqa: F401, F403, WPS347, WPS433
except ImportError:
    logger.error("Can't import user config. Initialized with default.")
