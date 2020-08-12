import logging
from typing import List

from src.layouts.default_tile.window_group import Direction, WindowGroup
from src.s3wm_types import AbstractLayoutManager, KeyCombination
from Xlib import X
from Xlib.display import Display
from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)


def workspace_switcher(ws_number):
    """
    This function used by layout to switch currently showed windows
    :param ws_number:
    """

    def switcher(wm):
        wm.layout.change_tag(ws_number, wm.display.screen())

    return switcher


def change_direction(new_direction: Direction):
    def changer(wm):
        wm.layout.change_direction(new_direction, wm.display())

    return changer


class TileLayout(AbstractLayoutManager):
    def __init__(self, wm):
        super().__init__(wm)
        self.ws_num = 0
        self.workspaces = [WindowGroup() for _ in range(9)]
        self.workspaces[0].screen = 0
        for i, screen in enumerate(self.screens):
            if i < len(self.workspaces):
                self.workspaces[i].screen = i

    def add_window(self, window: Window, display: Display):
        current_group = self.current_window_group(display)
        window.map()
        current_group.add_window(window)

    def update_layout(self, display: Display):
        pass

    def remove_window(self, window: Window, display: Display):
        pass

    def change_direction(self, direction: Direction, screen: Screen):
        pass

    def focus_in(self):
        pass

    def focus_out(self):
        pass

    def current_window_group(self, display: Display):
        pointer = display.screen().root.query_pointer()
        focused_window = pointer.child
        if focused_window == X.NONE:
            return None
        workspace = self.workspaces[self.ws_num]
        return workspace.find_group_by_window(focused_window)

    def current_screen(self, display: Display) -> int:
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

    def change_tag(self, ws_number, screen: Screen):
        pass

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
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
