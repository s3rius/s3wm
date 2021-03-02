from Xlib.display import Display

from s3wm_core.atoms.base import BaseAtomGroup
from s3wm_core.atoms.free_desktop_atoms import FreeDesktopAtoms
from s3wm_core.atoms.x11_atoms import X11Atoms


class S3HelperAtoms(BaseAtomGroup):
    """S3WM window properties."""

    workspace_num: int
    screen_num: int
    is_visible: int

    @staticmethod
    def init_atoms(display: Display) -> "S3HelperAtoms":
        """
        Intern all atoms from display.

        :param display: current display.
        :return: This class.
        """
        return S3HelperAtoms(
            workspace_num=display.intern_atom("_S3WM_WORKSPACE_NUM"),
            screen_num=display.intern_atom("_S3WM_SCREEN_NUM"),
            is_visible=display.intern_atom("_S3WM_IS_VISIBLE"),
        )


class S3WMAtoms(BaseAtomGroup):
    """All usable atoms."""

    x11: X11Atoms
    fd: FreeDesktopAtoms
    s3: S3HelperAtoms

    @staticmethod
    def init_atoms(display: Display) -> "S3WMAtoms":
        return S3WMAtoms(
            x11=X11Atoms.init_atoms(display),
            fd=FreeDesktopAtoms.init_atoms(display),
            s3=S3HelperAtoms.init_atoms(display),
        )
