from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, Tuple, Union

from src.utils import get_window_geometry
from Xlib import XK, X
from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window


class KeyCombination:
    """
    Used to add global key combinations.
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


class S3window(object):
    """
    In future will be used as Window wrapper,
    with some additional functionality.
    """

    def __init__(self, window: Window):
        self.window = window

    def get_geom(self, as_dict: bool = False) -> Union[Dict, Tuple]:
        """
        Get window rectangle.
        :param as_dict: if True -> dict will be returned.
        :return: Window geometry
        """
        geom = get_window_geometry(self.window)
        if as_dict:
            return {
                "x": geom.x,
                "y": geom.y,
                "height": geom.height,
                "width": geom.width,
            }
        return geom.x, geom.y, geom.height, geom.width


class AbstractLayoutManager(ABC):
    gaps = 5

    def __init__(self, _wm):
        self.current_tag = 1

    @abstractmethod
    def add_window(self, window: Window, screen: Screen):
        """
        Add window to Layout manager.
        This method must put window under control of current LayoutManager.
        :param window: added window
        :param screen: current screen
        """
        raise NotImplementedError()

    @abstractmethod
    def update_layout(self, screen: Screen):
        """
        Place all windows according to rules defined here.
        :param screen: current screen
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_window(self, window: Window, screen: Screen):
        """
        Remove window from LayoutManager.

        :param window: window that was removed.
        :param screen: screen
        """
        raise NotImplementedError()

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        return []
