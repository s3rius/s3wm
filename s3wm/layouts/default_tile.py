from Xlib.protocol.display import Screen

from s3wm_core.layout_base import AbstractLayoutManager
from s3wm_core.s3window import S3window


class DefaultTile(AbstractLayoutManager):
    """Default tile manager."""

    def add_window(self, window: S3window) -> None:
        """
        Add window to layout manager and adjust size and position.

        :param window: new window.
        """

    def update_layout(self, screen: Screen) -> None:
        """
        Update the whole layout layout.

        :param screen: current screen.
        """

    def remove_window(self, window: S3window) -> None:
        """
        Remove window from current layout.

        :param window: removed window.
        """
