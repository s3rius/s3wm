import logging
from typing import List

from src.layouts.default_tile.window_group import WindowGroup
from src.s3wm_types import AbstractLayoutManager, KeyCombination
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


class TileLayout(AbstractLayoutManager):
    def __init__(self, wm):
        super().__init__(wm)
        self.workspace = 1
        self.focused_screen = 0
        self.workspaces = [WindowGroup() for _ in range(9)]
        self.workspaces[0].screen = 1
        for i, screen in enumerate(self.screens):
            if i < len(self.workspaces):
                self.workspaces[i].screen = i

    def add_window(self, window: Window, screen: Screen):
        pass

    def update_layout(self, screen: Screen):
        pass

    def remove_window(self, window: Window, screen: Screen):
        pass

    def change_tag(self, ws_number, screen):
        pass

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        keys = super(TileLayout, cls).get_keys()
        for i in range(1, 9 + 1):
            keys.append(
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key=str(i),
                    action=workspace_switcher(i),
                ),
            )
        return keys
