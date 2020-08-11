import logging
import re
import subprocess

logger = logging.getLogger(__name__)


def get_window_class(window):
    """Fetch the WM_CLASS window property of the window WINDOW and return
    the class part of the property.  Return empty string if class is not
    retrieved."""
    try:
        cmd, cls = window.get_wm_class()
    except Exception as e:
        logger.error(f"Can't get window class. Cause: {e}")
        return ""
    if cls is not None:
        return cls
    else:
        return ""


def get_window_geometry(window):
    """Obtain the geometry and attributes of the window WINDOW.  Return as
    a Xlib.protocol.rq.Struct object.  Valid attributes are x, y, width,
    height, root, depth, border_width, and sequence_number.  Return None
    if the geometry is not retrieved."""
    try:
        return window.get_geometry()
    except Exception as e:
        logger.error(f"Can't get window geometry. Cause: {e}")
        return None


def get_window_attribute(window):
    try:
        return window.get_attributes()
    except Exception as e:
        logger.error(f"Can't get window attributes. Cause: {e}")
        return None


def get_screen_size(screen):
    """Return the dimension (WIDTH, HEIGHT) of the current screen as a
    tuple in pixels.  If xrandr command exsits and either DP (DisplayPort)
    or HDMI output is active, return its dimensionn instead of the screen
    size of the current X11 display."""
    width, height = screen.width_in_pixels, screen.height_in_pixels
    output = subprocess.getoutput("xrandr --current")
    # pick the last line including DP- or HDMI-
    m = re.search(r"(DP-?\d|HDMI-?\d) connected (\d+)x(\d+)", output)
    if m:
        width, height = int(m.group(2)), int(m.group(3))
    logger.debug(f"get_screen_size -> w:{width} h:{height}")
    return width, height


def get_usable_screen_size(screen):
    """Return the dimension (WIDTH, HEIGHT) of the usable screen are
    (i.e., the area of the current screen excluding the are for displaying
    status monitor using, for example, xpymon."""
    width, height = get_screen_size(screen)
    logger.debug(f"get_usable_screen_size -> w:{width} h:{height}")
    return width, height
