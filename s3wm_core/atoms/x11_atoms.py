from pydantic import BaseModel
from Xlib import Xatom
from Xlib.display import Display


class X11Atoms(BaseModel):
    # Types atoms
    type_atom: int = Xatom.ATOM
    type_utf8_string: int
    type_window: int = Xatom.WINDOW
    type_integer: int = Xatom.INTEGER

    # Freedesktop property atoms

    @staticmethod
    def init_atoms(display: Display) -> "X11Atoms":
        """
        Intern all atoms from X11 and save it in S3WMAtoms model.

        :param display: connected display.
        :return: Atoms.
        """
        return X11Atoms(
            type_utf8_string=display.intern_atom("UTF8_STRING"),
        )
