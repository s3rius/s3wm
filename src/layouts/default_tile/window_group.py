import logging
from enum import Enum
from typing import List, Optional, Union

from src.s3wm_types import S3window
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"


class WindowGroup(object):
    def __init__(
        self,
        direction: Direction = Direction.RIGHT,
        inner: Optional[List[Union[S3window, "WindowGroup"]]] = None,
    ):
        self.direction = direction
        self.screen = None
        self.nested_groups = []
        if inner:
            self.nested_groups = inner

    def add_window(self, window: Window):
        self.nested_groups.append(S3window(window))

    def remove_window(self, window: Window):
        pass

    def update_layout(self, screen):
        pass

    def find_group_by_window(self, window) -> Optional["WindowGroup"]:
        try:
            self.nested_groups.index(window)
            return self
        except ValueError:
            for group in filter(
                lambda x: isinstance(x, WindowGroup), self.nested_groups
            ):
                if group.find_group_by_window(window):
                    return group

    def unmap_all(self):
        for group in self.nested_groups:
            if isinstance(group, S3window):
                group.hide()
            elif isinstance(group, WindowGroup):
                group.unmap_all()
            else:
                logger.warning("Unknown window type.")
