from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window

from s3wm_core.utils import get_screen_size
from s3wm_core.x_models import ScreenGeometry


class S3screen:
    """Screen abstraction for S3wm."""

    def __init__(self, screen: Screen):
        self.screen = screen

    @property
    def geom(self) -> ScreenGeometry:
        """
        Get screen parameters.

        :return: screen geometry.
        """
        width, height = get_screen_size(self.screen)
        return ScreenGeometry(
            width=width,
            height=height,
        )

    @property
    def root_window(self) -> Window:
        """
        Get root window.

        :return: root window.
        """
        return self.screen.root

    @property
    def width(self) -> int:
        """
        Screen width.

        Use geometry to support connected HDMI or DP.

        :return: Screen width in pixels.
        """
        return int(self.screen.width_in_pixels)

    @property
    def height(self) -> int:
        """
        Screen height.

        :return: Screen height in pixels.
        """
        return int(self.screen.height_in_pixels)
