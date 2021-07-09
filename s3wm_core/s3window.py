from typing import Any, Optional

from loguru import logger
from Xlib.error import XError
from Xlib.X import BadWindow, CurrentTime, RevertToParent
from Xlib.xobject.drawable import Window

from s3wm_core.atoms import S3WMAtoms
from s3wm_core.s3screen import S3screen
from s3wm_core.utils import get_window_geometry
from s3wm_core.x_models import WindowGeometry, XWindowAttributes


class S3window(object):
    """Main window abstraction for S3WM."""

    _atoms: S3WMAtoms

    def __init__(
        self,
        window: Window,
        screen: S3screen,
        parent: Optional[Window] = None,
    ):
        self.parent = parent
        self.window = window
        self.screen = screen

    @property
    def id(self) -> int:
        """
        X11 resource ID allocated for this window.

        :return: unique window ID.
        """
        return int(self.window.id)

    @property
    def is_root(self) -> bool:
        """
        Property returns true if this window is root for display.

        :return: boolean
        """
        return bool(self.id == self.screen.root_window.id)

    @property
    def geom(self) -> Optional[WindowGeometry]:
        """
        Get window geometry.

        :return: Window geometry
        """
        return get_window_geometry(self.window)

    @property
    def attributes(self) -> Optional[XWindowAttributes]:
        """
        Return X11 window attributes.

        :return: window attributes.
        """
        try:
            attrs = self.window.get_attributes()
            return XWindowAttributes.from_orm(attrs)
        except XError as err:
            logger.debug(f"Can't get window attributes. Cause: {err}")
            return None

    def get_transient(self) -> Optional["S3window"]:
        """
        Get transient window for current.

        :return: transient window if any.
        """
        try:
            transient = self.window.get_wm_transient_for()
            if not transient:
                return None
            return S3window(transient, self.screen)
        except BadWindow as bwerr:
            logger.debug(f"Can't get transient. Cause: {bwerr}")
        return None

    def map(self) -> None:
        """Maps window in X11."""
        self.window.map()

    def unmap(self) -> None:
        """Unmap window in X11."""
        self.window.unmap()

    def focus(self) -> None:
        """Set focus to window."""
        self.window.set_input_focus(
            RevertToParent,
            CurrentTime,
        )

    def check_window_type(self, window_type: int) -> bool:
        """
        Check whether window has requested some type.

        You can check whether window has requested type
        by using s3wm_core.atoms.free_desktop_atoms.WindowTypes atoms.

        :param window_type: window_type atom.
        :return: list of requested window types.
        """
        try:
            window_types = self.get_atom_prop(self._atoms.fd.window_types.window_type)
            if not window_types:
                return False
        except XError as err:
            logger.debug(f"Can't get window state. Cause: {err}")
            return False
        return window_type in window_types.value

    def check_window_state(self, state: int) -> bool:
        """
        Check window requested state.

        You can check whether window has requested particular window_state
        by using s3wm_core.atoms.free_desktop_atoms.WindowState atoms.

        :param state: window state to check.
        :return: whether the window state is equal to given state.
        """
        try:
            wm_state = self.get_atom_prop(self._atoms.fd.window_state.wm_state_type)
            if not wm_state:
                return False
        except XError as err:
            logger.debug(f"Can't get window state. Cause: {err}")
            return False
        return state in wm_state.value

    def resize(self, width: int, height: int, percents: bool = False) -> None:
        """
        Resize window.

        If percents mode is on, width and height are treated as a percents,
        relative to the current screen geometry.

        :param width: new width
        :param height: new height
        :param percents: per cent mode is on or off.
        """
        win_width = width
        win_height = height
        if percents:
            screen_geom = self.screen.geom
            win_width = (screen_geom.width * width) // 100
            win_height = (screen_geom.height * height) // 100
        self.window.configure(
            width=win_width,
            height=win_height,
        )

    def move(self, x: int, y: int) -> None:  # noqa: WPS111
        """
        Move window on the screen.

        :param x: top left corner x coordinate.
        :param y: top left corner y coordinate.
        """
        self.window.configure(
            x=x,
            y=y,
        )

    def destroy(self) -> None:
        """Kill window from X11."""
        self.window.destroy()

    def get_atom_prop(
        self,
        atom: int,
        atom_type: Optional[int] = None,
    ) -> Optional[Any]:
        """
        Obtain atom property from the window object.

        :param atom: atom property to obtain.
        :param atom_type: type of property.
            If None, type_atom is used.
        :return: None or GetAtomResponse.
        """
        if atom_type is None:
            atom_type = self._atoms.x11.type_atom
        try:
            return self.window.get_full_property(
                atom,
                atom_type,
            )
        except XError as err:
            logger.exception(err)
            return None

    def __str__(self) -> str:
        return f"<S3Window {self.id}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, S3window):
            return False
        return self.id == other.id
