from Xlib.protocol.display import Screen

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
        return ScreenGeometry.from_orm(get_screen_size(self.screen))
