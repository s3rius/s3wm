from typing import List, Optional

from loguru import logger

from s3wm_core.s3window import S3window


class Tab:
    """Tab abstraction. This abstraction used in tiles to organize windows."""

    gaps: int = 0

    def __init__(self) -> None:
        self.windows: List[S3window] = []
        self.focused_window: Optional[S3window] = None
        self.main_window_size = 50

    def focus(self) -> None:
        """Show all windows from tab and focus on the last one."""
        for window in self.windows:
            window.map()
        self.update_layout()
        self.focused_window = None
        if self.windows:
            self.windows[-1].focus()

    def lose_focus(self) -> None:
        """Hide all windows from the screen."""
        for window in self.windows:
            window.unmap()

    def focused_index(self) -> int:
        """
        Get array index of currently focused window.

        :return: index.
        """
        for index, window in enumerate(self.windows):
            if window == self.focused_window:
                return index
        return 0

    def focus_prev(self) -> None:
        """Focus on a previous window in array."""
        if not self.windows:
            return
        index = self.focused_index()
        index += 1
        if index == len(self.windows):
            index = 0
        self.focused_window = self.windows[index]
        self.focused_window.focus()

    def focus_next(self) -> None:
        """Focus on a next window in windows stack."""
        if not self.windows:
            return
        index = self.focused_index()
        self.focused_window = self.windows[index - 1]
        self.focused_window.focus()

    def pop_focused_window(self) -> Optional[S3window]:
        """
        Pop focused window from tab.

        :return: previously focused window.
        """
        if not self.windows:
            return None
        index = self.focused_index()
        target_window = self.windows.pop(index)
        target_window.unmap()
        self.focused_window = None
        self.update_layout()
        return target_window

    def add_window(self, window: S3window) -> None:
        """
        Add new window to tab.

        :param window: new window.
        """
        self.windows.append(window)
        self.focused_window = window
        window.focus()
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
        self.focused_window = None
        # If we have other windows on our tab we focus on the last one.
        if self.windows:
            self.windows[-1].focus()
            self.focused_window = self.windows[-1]
        self.update_layout()

    def change_main_window_size(self, diff: int) -> None:
        """
        Change width of a main window.

        :param diff: delta to current size.
        """
        if not self.windows or len(self.windows) == 1:
            return
        self.main_window_size = min(self.main_window_size + diff, 90)  # noqa: WPS432
        self.main_window_size = max(10, self.main_window_size)
        self.update_layout()

    def move_window_forward(self) -> None:
        """Move focused window backward in stack."""
        if not self.windows:
            return
        index = self.focused_index()
        second_index = index + 1
        if second_index >= len(self.windows):
            second_index = 0
        tmp = self.windows[index]
        self.windows[index] = self.windows[second_index]
        self.windows[second_index] = tmp
        self.update_layout()

    def move_window_backward(self) -> None:
        """Move focused window forward in stack."""
        if not self.windows:
            return
        index = self.focused_index()
        tmp = self.windows[index]
        self.windows[index] = self.windows[index - 1]
        self.windows[index - 1] = tmp
        self.update_layout()

    def update_layout(self) -> None:  # noqa: C901, WPS210, WPS231, WPS213
        """Place all windows on layout nicely."""
        logger.debug("Updating layout")
        logger.info(self.gaps)
        if not self.windows:
            return

        main_window_width = self.main_window_size
        main_width_gaps = 1

        if len(self.windows) == 1:
            main_window_width = 100
            main_width_gaps = 2

        main_window = self.windows[-1]
        main_window.resize(width=main_window_width, height=100, percents=True)
        main_window.move(
            x=self.gaps,
            y=self.gaps,
        )
        main_geom = main_window.geom
        if not main_geom:
            return
        main_window.resize(
            width=main_geom.width - (self.gaps * main_width_gaps),
            height=main_geom.height - (self.gaps * 2),
        )
        if len(self.windows) == 1:
            return
        main_geom = main_window.geom
        if not main_geom:
            return
        height_percent = 100 // (len(self.windows) - 1)
        windows_x = main_geom.x + main_geom.width + self.gaps
        windows_y = 0
        for window in reversed(self.windows):
            if window == main_window:
                continue
            window.resize(
                width=100 - self.main_window_size,  # : WPS432
                height=height_percent,
                percents=True,
            )
            win_geom = window.geom
            if not win_geom:
                continue
            window.resize(
                width=win_geom.width - (self.gaps * 2),
                height=win_geom.height - (self.gaps * 2),
            )
            window.move(x=windows_x, y=windows_y + self.gaps)
            windows_y += win_geom.height
