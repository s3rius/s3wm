from abc import abstractmethod

from pydantic import BaseModel
from Xlib.display import Display


class BaseAtomGroup(BaseModel):
    """
    Base class for atoms group.

    This is basically a BaseModel with one method that helps
    you intern all needed atoms from display.
    """

    @staticmethod
    @abstractmethod
    def init_atoms(display: Display) -> "BaseAtomGroup":
        """
        Intern all atoms from display.

        Since all properties can be obtained only using atoms
        you must implement this function to be able to manipulate
        with atom properties.

        :param display: Current display.
        :return: Current class.
        """
