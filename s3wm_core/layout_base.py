from abc import ABC, abstractmethod
from typing import Any, List

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

    def focus_in(self, window: S3window) -> None:
        """
        Notify about focusing on some specific window.

        This function is used to be called when pointer is moved to some window.

        :param window: window that pointer focusing at.
        """

    def focus_out(self, window: S3window) -> None:
        """
        Notify about event when pointer has stopped focusing on some window.

        This function is used to be called when pointer has left some window.

        :param window: window that lost focus.
        """
