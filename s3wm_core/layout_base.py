from abc import ABC, abstractmethod
from typing import Any, List

from Xlib.protocol.display import Screen
from Xlib.xobject.drawable import Window

from s3wm_core.key_combination import KeyCombination


class AbstractLayoutManager(ABC):
    """Base class for Layout managers."""

    gaps = 5

    def __init__(self, _wm: Any) -> None:
        self.current_tag = 1

    @abstractmethod
    def add_window(self, window: Window, screen: Screen) -> None:
        """
        Add window to Layout manager.

        This method must put window under control of current LayoutManager.
        :param window: added window
        :param screen: current screen
        """

    @abstractmethod
    def update_layout(self, screen: Screen) -> None:
        """
        Place all windows according to rules defined here.

        :param screen: current screen
        """

    @abstractmethod
    def remove_window(self, window: Window, screen: Screen) -> None:
        """
        Remove window from LayoutManager.

        :param window: window that was removed.
        :param screen: screen
        """

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        """Get Keys specific to your layout.

        This method need to return keyCombinations to
        manipulate your layout.

        :return: List of key combinations
        """
        return []
