from collections import defaultdict
from typing import DefaultDict, List

from Xlib.protocol.display import Screen
from Xlib.X import ShiftMask

from s3wm.layouts.default_tile.key_bindings import (
    change_tab,
    kill_focused_window,
    move_focus,
    move_window_to_tab,
)
from s3wm.layouts.default_tile.tab import Tab
from s3wm.s3wm import S3WM
from s3wm_core.key_combination import KeyCombination
from s3wm_core.layout_base import AbstractLayoutManager
from s3wm_core.s3window import S3window


class DefaultTile(AbstractLayoutManager):
    """Default tile manager."""

    gaps: int = 0

    def __init__(self, wm: S3WM) -> None:
        """
        Initialize Layout.

        :param wm: S3WM instance.
        """
        super().__init__(wm)
        Tab.gaps = self.gaps
        self.tabs: DefaultDict[int, Tab] = defaultdict(Tab)
        self.current_tab = 0
        self.tabs[self.current_tab].focus()

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
        self.tabs[self.current_tab].focus()

    def focus_next(self) -> None:
        """Focus next window on the current tab."""
        self.tabs[self.current_tab].focus_next()

    def focus_prev(self) -> None:
        """Focus previous window on the current tab."""
        self.tabs[self.current_tab].focus_prev()

    def move_focused_window(self, tab_index: int) -> None:
        """
        Move currently focused window to another tab.

        :param tab_index: to which tab do we need to move.
        """
        window = self.tabs[self.current_tab].pop_focused_window()
        self.tabs[tab_index].add_window(window)

    def kill_focused_window(self) -> None:
        """Kill focused window."""
        window = self.tabs[self.current_tab].pop_focused_window()
        window.destroy()

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
            keys.append(
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key | ShiftMask,
                    key=str(index),
                    action=move_window_to_tab(index - 1),
                ),
            )

        keys.extend(
            [
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key="j",
                    action=move_focus(prev=False),
                ),
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key="k",
                    action=move_focus(prev=True),
                ),
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key | ShiftMask,
                    key="c",
                    action=kill_focused_window,
                ),
            ],
        )

        return keys
