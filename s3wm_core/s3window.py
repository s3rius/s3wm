from typing import Any, Optional

from Xlib.X import CurrentTime, RevertToParent
from Xlib.xobject.drawable import Window

from s3wm_core.s3screen import S3screen
from s3wm_core.utils import get_window_geometry
from s3wm_core.x_models import WindowGeometry


class S3window(object):
    """Main window abstraction for S3WM."""

    def __init__(
        self,
        window: Window,
        screen: S3screen,
        parent: Optional[Window] = None,
    ):
        self.parent = parent
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

    def resize(self, width: int, height: int, percents: bool = False) -> None:
        """
        Resize window.

        If percents mode is on, width and height are treated as a percents,
        relative to the current screen geometry.

        :param width: new width
        :param height: new height
        :param percents: per cent mode is on or off.
        """
        win_width = width
        win_height = height
        if percents:
            screen_geom = self.screen.geom
            win_width = (screen_geom.width * width) // 100
            win_height = (screen_geom.height * height) // 100
        self.window.configure(
            width=win_width,
            height=win_height,
        )

    def move(self, x: int, y: int) -> None:  # noqa: WPS111
        """
        Move window on the screen.

        :param x: top left corner x coordinate.
        :param y: top left corner y coordinate.
        """
        self.window.configure(
            x=x,
            y=y,
        )

    def destroy(self) -> None:
        """Kill window from X11."""
        self.window.destroy()

    def __str__(self) -> str:
        return f"<S3Window {self.id}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, S3window):
            return False
        return self.id == other.id
