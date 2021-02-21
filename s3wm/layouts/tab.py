from typing import List

from s3wm_core.s3window import S3window


class Tab:
    """Tab abstraction. This abstraction used in tiles to organize windows."""

    def __init__(self) -> None:
        self.windows: List[S3window] = []

    def set_focus(self) -> None:
        """Show all windows from tab and focus on the last one."""
        for window in self.windows:
            window.map()
        self.update_layout()
        if self.windows:
            self.windows[-1].focus()

    def lose_focus(self) -> None:
        """Hide all windows from the screen."""
        for window in self.windows:
            window.unmap()

    def add_window(self, window: S3window) -> None:
        """
        Add new window to tab.

        :param window: new window.
        """
        self.windows.append(window)
        self.update_layout()

    def remove_window(self, window: S3window) -> None:
        """
        Remove window from tab.

        :param window: removed window.
        """
        # Trying to remove window from windows list.
        for index, tab_window in enumerate(self.windows):
            if tab_window == window:
                # If we have such window we can unmap it.
                self.windows.pop(index)
                window.unmap()
        self.update_layout()
        # If we have other windows on our tab we focus on the last one.
        if self.windows:
            self.windows[-1].focus()

    def update_layout(self) -> None:
        """Place all windows on layout nicely."""
