from typing import Any, Optional

from Xlib.protocol.display import Screen
from Xlib.X import CurrentTime, RevertToParent
from Xlib.xobject.drawable import Window

from s3wm_core.utils import get_window_geometry
from s3wm_core.x_models import WindowGeometry


class S3window(object):
    """Main window abstraction for S3WM."""

    def __init__(self, window: Window, screen: Screen):
        self.window = window
        self.screen = screen

    @property
    def id(self) -> int:
        """
        X11 resource ID allocated for this window.

        :return: unique window ID.
        """
        return int(self.window.id)

    @property
    def geom(self) -> Optional[WindowGeometry]:
        """
        Get window geometry.

        :return: Window geometry
        """
        return get_window_geometry(self.window)

    def map(self) -> None:
        """Maps window in X11."""
        self.window.map()

    def unmap(self) -> None:
        """Unmap window in X11."""
        self.window.unmap()

    def focus(self) -> None:
        """Set focus to window."""
        self.window.warp_pointer(15, 15)  # noqa: WPS432
        self.window.set_input_focus(
            RevertToParent,
            CurrentTime,
        )

    def __str__(self) -> str:
        return f"<S3Window {self.id}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, S3window):
            return False
        return self.id == other.id
