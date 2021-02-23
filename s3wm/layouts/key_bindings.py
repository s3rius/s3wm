from typing import Callable

from s3wm.s3wm import S3WM


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
