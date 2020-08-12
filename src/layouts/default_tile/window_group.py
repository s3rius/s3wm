import logging
import uuid
from typing import List, Optional, Union

from src.s3wm_types import Coord, Direction, S3window
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)


class WindowGroup(object):
    def __init__(
        self,
        direction: Direction = Direction.RIGHT,
        inner: Optional[List[Union[S3window, "WindowGroup"]]] = None,
    ):
        self.id = uuid.uuid4()
        self.direction = direction
        self.nested_groups = []
        self.last_coords = None
        self.focus_window = None
        if inner:
            self.nested_groups = inner

    def add_window(self, window: Window):
        """
        Add window to WindowGroup.
        This window now will be managed by this Group.
        :param window: target window
        """
        self.nested_groups.append(S3window(window))
        self.focus_window = len(self.nested_groups) - 1

    def remove_window(self, window: Window) -> bool:
        """
        Remove window from layout and update focus of changed group.
        :param window: window to remove
        :return: True if window was deleted
        """
        logger.debug("Removing window")
        group = self.find_group_by_window(window)
        if group:
            index = group.nested_groups.index(S3window(window))
            group.nested_groups.pop(index)
            # Changing focus window in one of nested group or this group itself.
            if len(group.nested_groups) == 0:
                group.focus_window = None
            elif group.focus_window >= len(group.nested_groups) - 1:
                group.focus_window = len(group.nested_groups) - 1
            else:
                group.focus_window = index
            return True
        return False

    def cleanup(self):
        """
        Remove all empty groups from nested_groups.
        """
        for index, group in enumerate(self.nested_groups):
            if isinstance(group, WindowGroup):
                if len(group.nested_groups) == 0:
                    self.nested_groups.pop(index)
                    continue
                group.cleanup()

    def update_layout(
        self,
        screen_coords: Optional[Coord] = None,
        inner_gaps: Optional[int] = None,
        outer_gaps: Optional[int] = None,
    ):
        """
        Update layout by splitting remaining space on each WindowGroup
        recursively. Split will be done in any direction.

        :param screen_coords: Coordinates available for filling.
        :param inner_gaps: gaps between windows if any
        :param outer_gaps: gaps between edges of available space and windows
        """
        # WindowGroup has no children. No update needed.
        self.cleanup()
        if len(self.nested_groups) == 0:
            return
        if screen_coords is None:
            if not self.last_coords:
                logger.error("Can't updated layout no Coord was provided.")
                return
            screen_coords = self.last_coords
        self.last_coords = screen_coords

        chunks = screen_coords.split(
            len(self.nested_groups), self.direction, inner_gaps, outer_gaps
        )
        for i, group in enumerate(self.nested_groups):
            if isinstance(group, S3window):
                group.transform(chunks[i])
                continue
            group.update_layout(chunks[i], inner_gaps, None)

    def find_group_by_window(self, window: Window) -> Optional["WindowGroup"]:
        """
        Recursively find which group has target window under control.
        :param window: target window
        :return: found WindowGroup or None
        """
        if S3window(window) in self.nested_groups:
            logger.debug(f"Found window in group {self}")
            return self

        for group in filter(lambda x: isinstance(x, WindowGroup), self.nested_groups):
            if group.find_group_by_window(window):
                return group

    def focus(self, screen, screen_coords):
        """
        Focus on previously focused window or center of a screen.
        :param screen: current screen
        :param screen_coords: currently focused screen coordinates
        """
        if len(self.nested_groups) == 0:
            screen.root.warp_pointer(
                screen_coords.x + screen_coords.width // 2,
                screen_coords.y + screen_coords.height // 2,
            )
        if not self.focus_window:
            self.focus_window = 0
        focus_group = self.nested_groups[self.focus_window]
        if isinstance(focus_group, WindowGroup):
            focus_group.focus(screen, screen_coords)
        else:
            focus_group.focus()

    def unmap_all(self):
        for group in self.nested_groups:
            if isinstance(group, S3window):
                group.hide()
            elif isinstance(group, WindowGroup):
                group.unmap_all()
            else:
                logger.warning("Unknown window type.")

    def map_all(self):
        for group in self.nested_groups:
            if isinstance(group, S3window):
                group.show()
            elif isinstance(group, WindowGroup):
                group.map_all()
            else:
                logger.warning("Unknown window type.")
