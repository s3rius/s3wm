import re
import subprocess
from typing import Optional, Tuple

from loguru import logger
from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window

from s3wm_core.x_models import WindowGeometry


def get_window_class(window: Window) -> str:
    """
    Get window wm_class.

    Fetch the WM_CLASS window property of the window WINDOW and return
    the class part of the property.  Return empty string if class is not
    retrieved.

    :param window: target window.
    :returns: window wm_class string.
    """
    try:
        cmd, window_cls = window.get_wm_class()
    except Exception as exc:
        logger.error(f"Can't get window class. Cause: {exc}")
        return ""
    if window_cls is not None:
        return str(window_cls)
    return ""


def get_window_geometry(window: Window) -> Optional[WindowGeometry]:
    """
    Obtain the geometry and attributes of the X11 window.

    :param window: target window.
    :returns: WindowGeomerty wrapper around X11 geometry type.
    """
    try:
        return WindowGeometry.from_orm(window.get_geometry())
    except Exception as exc:
        logger.exception(exc)
        logger.error(f"Can't get window geometry. Cause: {exc}")
        return None


def get_screen_size(screen: Screen) -> Tuple[int, int]:
    """
    Get current screen size.

    Return the dimension (WIDTH, HEIGHT) of the current screen as a
    tuple in pixels.  If xrandr command exists and either DP (DisplayPort)
    or HDMI output is active, return its dimensions instead of the current X11 display
    size.

    :param screen: current screen.
    :returns: Width and height of current screen.
    """
    width, height = screen.width_in_pixels, screen.height_in_pixels
    output = subprocess.getoutput("xrandr --current")
    # pick the last line including DP- or HDMI-
    match = re.search(r"(DP-?\d|HDMI-?\d) connected (\d+)x(\d+)", output)
    if match:
        width = int(match.group(2))
        height = int(match.group(3))
    logger.debug(f"get_screen_size -> w:{width} h:{height}")
    return width, height


def get_usable_screen_size(screen: Screen) -> Tuple[int, int]:
    """
    Get usable dimensions of the current screen.

    Return the dimension (WIDTH, HEIGHT) of the usable screen are
    (i.e., the area of the current screen excluding the are for displaying
    status monitor using, for example, xpymon.

    :param screen: current screen.
    :returns: Width and height of current screen.
    """
    width, height = get_screen_size(screen)
    logger.debug(f"get_usable_screen_size -> w:{width} h:{height}")
    return width, height
