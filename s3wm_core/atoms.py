from pydantic import BaseModel
from Xlib import Xatom
from Xlib.display import Display


class S3Atoms(BaseModel):
    # Types atoms
    type_atom: int = Xatom.ATOM
    type_utf8_string: int
    type_window: int = Xatom.WINDOW
    type_integer: int = Xatom.INTEGER

    # Freedesktop property atoms
    net_window_type_dialog: int
    net_window_type: int
    net_wm_name: int
    net_wm_state_fullscreen: int
    net_active_window: int
    net_client_list: int


def init_atoms(display: Display) -> S3Atoms:
    """
    Intern all atoms from X11 and save it in S3WMAtoms model.

    :param display: connected display.
    :return: Atoms.
    """
    return S3Atoms(
        type_utf8_string=display.intern_atom("UTF8_STRING"),
        net_window_type_dialog=display.intern_atom("_NET_WM_WINDOW_TYPE_DIALOG"),
        net_window_type=display.intern_atom("_NET_WM_WINDOW_TYPE"),
        net_wm_name=display.intern_atom("_NET_WM_NAME"),
        net_wm_state_fullscreen=display.intern_atom("_NET_WM_STATE_FULLSCREEN"),
        net_active_window=display.intern_atom("_NET_ACTIVE_WINDOW"),
        net_client_list=display.intern_atom("_NET_CLIENT_LIST"),
    )
