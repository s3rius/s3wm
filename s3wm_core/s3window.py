from typing import Optional

from Xlib.xobject.drawable import Window

from s3wm_core.utils import get_window_geometry
from s3wm_core.x_models import WindowGeometry


class S3window(object):
    """Main window abstraction for S3WM."""

    def __init__(self, window: Window):
        self.window = window

    @property
    def get_geom(self) -> Optional[WindowGeometry]:
        """
        Get window geometry.

        :return: Window geometry
        """
        return get_window_geometry(self.window)
