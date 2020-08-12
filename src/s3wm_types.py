import logging
from abc import ABC, abstractmethod
from copy import copy
from enum import Enum
from typing import Any, Callable, List, Optional, Union

from src.utils import get_window_geometry
from Xlib import XK, X
from Xlib.display import Display
from Xlib.xobject.drawable import Window

logger = logging.getLogger(__name__)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"


class KeyCombination:
    """
    Used to add global key combinations.
    Key combinations handled in main S3WM object.
    """

    default_mod_key = X.Mod4Mask

    def __init__(
        self,
        modifiers=X.NONE,
        key: Optional[Union[str, int]] = None,
        action: Optional[Union[Callable, str]] = None,
    ):
        self.modifiers = modifiers  # Event masks such as Mod4Mask
        self.key = key  # Key of event
        if isinstance(key, str):
            self.key = XK.string_to_keysym(key)
        self.action = action  # Action to perform when event pressed

    def __repr__(self):
        return f"{{key:{self.key} mod:{self.modifiers}->{self.action}}}"


class Coord(object):
    """
    Wrapper to work with coordinates and geometry.

          x
    0  ║  ┌──width──┐
     ══╬══╬═════════╬════▶
       ║  |         |
    y ┌╬--┌─────────┐
      |║  |  Coord  |
height|║  | target  |
      |║  |         |
      └╬-─└─────────┘
       ║
       ▼
    """

    def __init__(self, obj: Any):
        self.x = obj.x
        self.y = obj.y
        self.width = obj.width
        self.height = obj.height

    def as_dict(self):
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    def split(
        self,
        n: int,
        direction: Direction,
        inner_gaps: Optional[int] = None,
        outer_gaps: Optional[int] = None,
    ) -> List["Coord"]:
        """
        Split layout by n chunks with equal width and height.
        If outer or inner gaps specified it will add spaces between chunks
        or at the edges of the current Coord object.

        This is an example of Horizontal split
        ┌────────────────────────────────────────┐
        |             outer                      |
        |  ┌────────┐   ┌────────┐   ┌────────┐  |
        | o|chunk 1 | i |chunk 2 | i |chunk 3 | o|
        | u|        | n |        | n |        | u|
        | t|        | n |        | n |        | t|
        | e|        | e |        | e |        | e|
        | r|        | r |        | r |        | r|
        |  |        |   |        |   |        |  |
        |  └────────┘   └────────┘   └────────┘  |
        |             outer                      |
        └────────────────────────────────────────┘


        :param n: number of chunks
        :param direction: Split direction (horizontal or vertical)
        :param inner_gaps: used as gap between chunks
        :param outer_gaps: create gap on the edge of the "Coord" object
        :return:
        """
        logger.debug("Started splitting")
        main_coords = copy(self)
        outer_gaps = outer_gaps or 0
        inner_gaps = inner_gaps or 0
        main_coords.x += outer_gaps
        main_coords.y += outer_gaps
        main_coords.width -= outer_gaps * 2
        main_coords.height -= outer_gaps * 2
        if direction in [Direction.LEFT, Direction.RIGHT]:
            logger.debug("Performing horizontal split")
            update_attr = "x"
            window_chunk_size = (main_coords.width // n) - inner_gaps
            main_coords.width = window_chunk_size
        else:
            logger.debug("Performing vertical split")
            update_attr = "y"
            window_chunk_size = (main_coords.height // n) - inner_gaps
            main_coords.height = window_chunk_size

        result_chunks = []
        acc = getattr(main_coords, update_attr)
        for i in range(n):
            chunk = copy(main_coords)
            setattr(chunk, update_attr, acc)
            acc += window_chunk_size + inner_gaps
            result_chunks.append(chunk)
        return result_chunks


class S3window(object):
    """
    Special Window wrapper with a bunch of helper methods,
    with some additional functionality.
    """

    def __init__(self, window: Window):
        self.window = window

    def __eq__(self, other):
        """
        Test that windows is equals.
        :param other:
        :return:
        """
        if isinstance(other, Window):
            return other == self.window
        elif isinstance(other, S3window):
            return other.window == self.window
        return False

    def get_geom(self) -> Coord:
        """
        Get window rectangle.
        :return: Window geometry
        """
        geom = get_window_geometry(self.window)
        return Coord(geom)

    def is_ok(self):
        pass

    def transform(self, coords: Coord):
        """
        Move and resize window according to Coord object
        :param coords: transform to apply
        """
        self.window.configure(**coords.as_dict())

    def focus(self):
        """
        Focus on this window
        """
        self.window.raise_window()
        self.window.warp_pointer(15, 15)
        self.window.set_input_focus(X.RevertToParent, 0)

    def hide(self):
        self.window.unmap()

    def show(self):
        self.window.map()


class AbstractLayoutManager(ABC):
    outer_gaps = 10
    inner_gaps = 5

    def __init__(self, wm):
        xinerama_info = wm.display.xinerama_query_screens()
        self.screen_count = xinerama_info.number
        self.screens: List[Coord] = list(map(Coord, xinerama_info.screens))
        logger.debug(f"Found {self.screen_count} screens")

    @abstractmethod
    def add_window(self, window: Window, display: Display):
        """
        Add window to Layout manager.
        This method must put window under control of current LayoutManager.
        :param window: added window
        :param display: current screen
        """
        pass

    @abstractmethod
    def update_layout(self, display: Display):
        """
        Place all windows according to rules defined here.
        :param display: current display
        """
        pass

    @abstractmethod
    def remove_window(self, window: Window, display: Display):
        """
        Remove window from LayoutManager.

        :param window: window that was removed.
        :param display: screen
        """
        pass

    # @abstractmethod
    # def focus_in(self):
    #     pass
    #
    # @abstractmethod
    # def focus_out(self):
    #     pass

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        return []
