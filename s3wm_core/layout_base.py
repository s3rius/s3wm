from abc import ABC, abstractmethod
from typing import Any, List

from Xlib.protocol.display import Screen

from s3wm_core.key_combination import KeyCombination
from s3wm_core.s3window import S3window


class AbstractLayoutManager(ABC):
    """Base class for Layout managers."""

    def __init__(self, _wm: Any) -> None:
        """Do whatever you want with data."""

    @abstractmethod
    def add_window(self, window: S3window) -> None:
        """
        Add window to Layout manager.

        This method must put window under control of current LayoutManager.
        :param window: added window
        """

    @abstractmethod
    def update_layout(self, screen: Screen) -> None:
        """
        Place all windows according to rules defined here.

        :param screen: current screen
        """

    @abstractmethod
    def remove_window(self, window: S3window) -> None:
        """
        Remove window from LayoutManager.

        :param window: window that was removed.
        """

    @classmethod
    def get_keys(cls) -> List[KeyCombination]:
        """Get Keys specific to your layout.

        This method need to return keyCombinations to
        manipulate your layout.

        :return: List of key combinations
        """
        return []
