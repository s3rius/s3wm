"""Default WM configuration."""
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from loguru import logger
from Xlib import X

from s3wm.layouts import DefaultTile
from s3wm_core import KeyCombination, kill_wm


def startup() -> None:
    """
    Actions to run at startup.

    Function called on startup.
    Actions defined here will be called at WindowManager startup.
    """
    logger.debug("Calling startup!")


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


# Importing user_config bt absolute path.
module_name = "user_config"
conf_path = Path("~/.s3wm_conf.py").expanduser()

try:  # noqa: WPS229
    if not conf_path.exists():
        raise ImportError
    spec = spec_from_file_location(module_name, str(conf_path))
    module = module_from_spec(spec)
    if not spec.loader:
        raise ImportError
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    from user_config import *  # noqa: F401, F403, WPS347, WPS433
except ImportError:
    logger.error("Can't import user config. Initialized with default.")
