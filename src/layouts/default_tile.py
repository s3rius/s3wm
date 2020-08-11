import logging
from collections import defaultdict

from src.s3wm_types import AbstractLayoutManager, KeyCombination
from src.utils import get_screen_size, get_usable_screen_size, get_window_geometry
from Xlib import X

logger = logging.getLogger(__name__)


def workspace_switcher(ws_number):
    """
    This function used by layout to switch currently showed windows
    :param ws_number:
    """

    def switcher(wm):
        wm.layout.change_tag(ws_number, wm.display.screen())

    return switcher


def toggle_fullscreen(wm):
    wm.layout.toggle_fullscreen(wm.display)


def geometry_sort_key(window):
    geom = get_window_geometry(window)
    if geom is None:
        return 100000000
    else:
        return geom.x + geom.y * 1000


class DefaultTile(AbstractLayoutManager):
    """
    Default tile layout is almost like i3-gaps default tile configuration.
    It has workspaces and simple layout logic.
    Also you can switch between layout direction.
    """

    gaps = 5

    def __init__(self, wm):
        super().__init__(wm)
        self.windows = defaultdict(list)
        self.focuses = defaultdict(int)
        self.current_tag = self.current_tag

    def add_window(self, window, screen):
        self.windows[self.current_tag].append(window)
        window.map()
        self.update_layout(screen)
        self.update_focus(window)

    def update_focus(self, window=None):
        if window:
            window.raise_window()
            window.warp_pointer(15, 15)
            window.set_input_focus(X.RevertToParent, 0)
            return
        windows = sorted(self.windows[self.current_tag], key=geometry_sort_key)
        try:
            i = windows.index(window)
            next_window = windows[(i + 1) % len(windows)]
        except ValueError:
            if windows:
                next_window = windows[0]
            else:
                return
        next_window.raise_window()
        next_window.warp_pointer(15, 15)
        next_window.set_input_focus(X.RevertToParent, 0)

    def update_layout(self, screen):
        width, height = get_usable_screen_size(screen)
        width -= self.gaps
        height -= self.gaps
        windows = self.windows[self.current_tag]
        if not windows:
            return
        window_size = (width // len(windows)) - self.gaps
        logger.debug(f"Optimal window size: {window_size}")
        configure_params = {
            "x": self.gaps,
            "y": self.gaps,
            "width": window_size,
            "height": height - self.gaps,
        }
        for window in windows:
            window.configure(**configure_params)
            configure_params["x"] += window_size + self.gaps

    def remove_window(self, window, screen):
        if window in self.windows[self.current_tag]:
            self.windows[self.current_tag].remove(window)
        self.update_layout(screen)
        self.update_focus()

    def change_tag(self, tag: int, _screen):
        """
        Update current workspace.
        :param tag: new workspace tag
        :param _screen: current screen
        """
        if tag == self.current_tag:
            return
        for window in self.windows[self.current_tag]:
            window.unmap()
        for window in self.windows[tag]:
            window.map()
        self.current_tag = tag

    def toggle_fullscreen(self, display):
        """
        Updates currently focused window.
        Makes it fit the display.
        If currently focused window geometry already matches the display geometry
        Then window will be mapped to normal size.
        :param display current display.
        """
        logger.debug("Trying to perform fullscreen")
        response = display.get_input_focus()
        window = response.focus
        if window == X.NONE:
            logger.debug("No focused window found")
            self.update_focus()
        response = display.get_input_focus()
        window = response.focus
        geometry = get_window_geometry(window)
        if not geometry:
            logger.error("Can't find window geometry")
            return
        window_geom = {"height": geometry.height, "width": geometry.width}
        logger.debug(f"Current window geometry: {window_geom}")
        screen_width, screen_height = get_screen_size(display.screen())
        if (
            screen_width == geometry.width
            and screen_height == geometry.height
            and geometry.x == 0
            and geometry.y == 0
        ):
            logger.debug("Found fullscreen window")
            for window in self.windows[self.current_tag]:
                window.map()
            self.update_layout(display.screen())
            return

        logger.debug("Hiding all other windows at workspace")
        for ws_window in self.windows[self.current_tag]:
            ws_window.unmap()

        window.map()
        window.configure(x=0, y=0, height=screen_height, width=screen_width)
        window.raise_window()
        window.warp_pointer(15, 15)
        window.set_input_focus(X.RevertToParent, 0)

    @classmethod
    def get_keys(cls):
        keys = super(DefaultTile, cls).get_keys()
        for i in range(1, 9 + 1):
            keys.append(
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key=str(i),
                    action=workspace_switcher(i),
                ),
            )
        keys.extend(
            [
                KeyCombination(
                    modifiers=KeyCombination.default_mod_key,
                    key="f",
                    action=toggle_fullscreen,
                )
            ]
        )
        return keys
