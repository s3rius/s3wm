from typing import Optional

from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window

from s3wm_core.utils import get_window_geometry
from s3wm_core.x_models import WindowGeometry


class S3window(object):
    """Main window abstraction for S3WM."""

    def __init__(self, window: Window, screen: Screen):
        self.window = window
        self.screen = screen

    @property
    def geom(self) -> Optional[WindowGeometry]:
        """
        Get window geometry.

        :return: Window geometry
        """
        return get_window_geometry(self.window)

    def map(self) -> None:
        """Maps window to X11."""
        self.window.map()
