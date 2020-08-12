import logging
from collections import defaultdict
from copy import copy
from typing import List, Optional

from src.layouts.default_tile.window_group import Direction, WindowGroup
from src.s3wm_types import AbstractLayoutManager, KeyCombination
from Xlib.display import Display
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)


def workspace_switcher(ws_number):
    """
    This function used by layout to switch currently showed windows
    :param ws_number:
    """

    def switcher(wm):
        wm.layout.change_tag(ws_number, wm.display)

    return switcher


def change_direction(new_direction: Direction):
    def changer(wm):
        wm.layout.change_direction(new_direction, wm.display)

    return changer


class TileLayout(AbstractLayoutManager):
    def __init__(self, wm):
        super().__init__(wm)
        self.ws_num = 0
        self.focused_win = None
        self.workspaces = defaultdict(WindowGroup)
        # Each int in this array represents workspace
        # associated with screen.
        self.screen_ws_map = [i for i in range(self.screen_count)]

    def add_window(self, window: Window, display: Display):
        """
        Add window to Layout manager.
        This function adds window to specific group
        and updates focus of current workspace.
        :param window: new window
        :param display: current working display
        """
        current_group = self.get_current_window_group(display)
        current_group.add_window(window)
        self.update_layout(display)
        self.focused_win = window
        screen_num = self.get_current_screen_num(display)
        screen_coords = self.screens[screen_num]
        current_group.focus(display.screen(), screen_coords)

    def update_layout(self, display: Display):
        """
        Reorganize windows on workspace to fin nicely at screen
        according to tiling rules.
        :param display: current display
        """
        screen_num = self.get_current_screen_num(display)
        working_group = self.get_current_window_group(display)
        screen_coords = copy(self.screens[screen_num])
        working_group.update_layout(
            screen_coords=screen_coords,
            inner_gaps=self.inner_gaps,
            outer_gaps=self.outer_gaps,
        )

    def remove_window(self, window: Window, display: Display):
        """
        Remove window from workspace and update it's layout.
        :param window: removed window
        :param display: current display
        """
        for group in self.workspaces.values():
            if group.remove_window(window):
                group.update_layout(
                    inner_gaps=self.inner_gaps, outer_gaps=self.outer_gaps
                )

    def get_current_window_group(
        self, display: Display, window: Optional[Window] = None
    ) -> WindowGroup:
        """
        Get workspace|WindowGroup that currently in focus.
        If window is provided then this function will return
        a WindowGroup That is a parent of this window.
        :param display: current display
        :param window: target window
        """
        screen = self.get_current_screen_num(display)
        logger.debug(f"Currently focusing on screen {screen}")
        if window:
            return self.workspaces[self.screen_ws_map[screen]].find_group_by_window(
                window
            )
        if self.focused_win:
            logger.debug("Found focused window")
            group = self.workspaces[self.screen_ws_map[screen]].find_group_by_window(
                self.focused_win
            )
            # Can be None if focused_win was deleted
            if group:
                self.focused_win = None
                return group
        return self.workspaces[self.screen_ws_map[screen]]

    def update_current_layout(self, display):
        """
        Update current layout on screen.
        To fit nicely according to tiling layout rules.
        :param display: current display
        """
        display_num = self.get_current_screen_num(display)
        workspace = self.workspaces[self.screen_ws_map[display_num]]
        workspace.update_layout(
            screen_coords=self.screens[display_num],
            inner_gaps=self.inner_gaps,
            outer_gaps=self.outer_gaps,
        )

    def get_current_screen_num(self, display: Display) -> int:
        """
        Get screen number that currently in focus.
        :param display: current display
        :return:
        """
        pointer = display.screen().root.query_pointer()
        pos_x, pos_y = pointer.root_x, pointer.root_y
        for i, screen in enumerate(self.screens):
            if (
                screen.x < pos_x <= screen.width + screen.x
                and screen.y < pos_y <= screen.height + screen.y
            ):
                return i
        # TODO: Find nearest screen instead of returning first.
        return 0

    def change_tag(self, ws_number: int, display: Display):
        """
        Change current focused workspace to another.
        :param ws_number: new workspace to focus at
        :param display: current display
        :return:
        """
        screen_num = self.get_current_screen_num(display)
        screen_coords = self.screens[screen_num]
        if ws_number in self.screen_ws_map:
            self.workspaces[ws_number].focus(display.screen(), screen_coords)
        else:
            self.workspaces[self.screen_ws_map[screen_num]].unmap_all()
            self.screen_ws_map[screen_num] = ws_number
            self.workspaces[ws_number].map_all()
            self.workspaces[ws_number].focus(display.screen(), screen_coords)

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        """
        Get keys to communicate with this LayoutManager
        :return: List of key combinations
        """
        keys = super(TileLayout, cls).get_keys()
        for i in range(1, 9 + 1):
            keys.append(
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key=str(i - 1),
                    action=workspace_switcher(i),
                ),
            )
        keys.extend(
            [
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key="h",
                    action=change_direction(Direction.RIGHT),
                ),
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key="v",
                    action=change_direction(Direction.DOWN),
                ),
            ]
        )
        return keys
