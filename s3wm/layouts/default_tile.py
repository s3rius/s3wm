from collections import defaultdict
from typing import Callable, DefaultDict, List

from Xlib.protocol.display import Screen

from s3wm.layouts.tab import Tab
from s3wm.s3wm import S3WM
from s3wm_core.key_combination import KeyCombination
from s3wm_core.layout_base import AbstractLayoutManager
from s3wm_core.s3window import S3window


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


class DefaultTile(AbstractLayoutManager):
    """Default tile manager."""

    def __init__(self, wm: S3WM) -> None:
        """
        Initialize Layout.

        :param wm: S3WM instance.
        """
        super().__init__(wm)
        self.tabs: DefaultDict[int, Tab] = defaultdict(Tab)
        self.current_tab = 0
        self.tabs[self.current_tab].set_focus()

    def add_window(self, window: S3window) -> None:
        """
        Add window to layout manager and adjust size and position.

        :param window: new window.
        """
        self.tabs[self.current_tab].add_window(window)
        window.focus()

    def update_layout(self, screen: Screen) -> None:
        """
        Update the whole layout layout.

        :param screen: current screen.
        """
        self.tabs[self.current_tab].update_layout()

    def remove_window(self, window: S3window) -> None:
        """
        Remove window from current layout.

        :param window: removed window.
        """
        self.tabs[self.current_tab].remove_window(window)
        self.update_layout(window.screen)

    def change_tab(self, tab_number: int) -> None:
        """
        Select tab to show on screen.

        :param tab_number: tab index
        """
        if tab_number == self.current_tab:
            return
        self.tabs[self.current_tab].lose_focus()
        self.current_tab = tab_number
        self.tabs[self.current_tab].set_focus()

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        """Get Keys specific to your layout.

        This method need to return keyCombinations to
        manipulate your layout.

        :return: List of key combinations
        """
        keys = super().get_keys()
        for index in range(1, 9 + 1):
            keys.append(
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key=str(index),
                    action=change_tab(index - 1),
                ),
            )

        return keys
