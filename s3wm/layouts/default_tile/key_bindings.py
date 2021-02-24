from typing import Callable

from s3wm.s3wm import S3WM
from s3wm_core import S3screen


def change_tab(tab_index: int) -> Callable[[S3WM], None]:
    """
    Create function to change tab on layout.

    :param tab_index: index of a tab.
    :return: function to change tab on layout.
    """

    def change_layout_tab(wm: S3WM) -> None:
        """
        Actually change layout's tab.

        :param wm: WindowManager.
        """
        wm.layout.change_tab(tab_index)

    return change_layout_tab


def move_focus(prev: bool) -> Callable[[S3WM], None]:
    """
    Change currently focused window.

    This function moves focus backward or forward, depending on a "prev" parameter.

    :param prev: move focus on a previous window.
    :return: function to change focus.
    """

    def change_focus(wm: S3WM) -> None:
        """
        Actually change focus.

        :param wm: current window manager.
        """
        if prev:
            wm.layout.focus_prev()
        else:
            wm.layout.focus_next()

    return change_focus


def move_window_to_tab(tab_index: int) -> Callable[[S3WM], None]:
    """
    Generate function to move focused window.

    :param tab_index: tab on which to move window.
    :returns: function to move window.
    """

    def move_window(wm: S3WM) -> None:
        """
        Move currently focused window to another tab.

        :param wm: window manager.
        """
        wm.layout.move_focused_window(tab_index)

    return move_window


def kill_focused_window(wm: S3WM) -> None:
    """
    Kill window that user currently focused at.

    :param wm: window manager.
    """
    wm.layout.kill_focused_window()


def change_gaps(delta: int) -> Callable[[S3WM], None]:
    """
    Change gaps between windows.

    :param delta: delta to add to current gaps value.
    :returns: function to change gaps.
    """

    def gap_changer(wm: S3WM) -> None:
        """
        Actual function to update gaps.

        :param wm: window manager.
        """
        wm.layout.tab_class.gaps += delta
        if wm.layout.tab_class.gaps < 0:
            wm.layout.tab_class.gaps = 0
        wm.layout.update_layout(S3screen(wm.display.screen()))

    return gap_changer
