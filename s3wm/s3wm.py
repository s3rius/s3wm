from argparse import Namespace
from subprocess import Popen
from typing import List, Optional

from frozendict import frozendict
from loguru import logger
from Xlib import X
from Xlib.display import Display
from Xlib.protocol.event import (
    DestroyNotify,
    EnterNotify,
    KeyPress,
    LeaveNotify,
    MapRequest,
    UnmapNotify,
)
from Xlib.Xcursorfont import left_ptr
from Xlib.xobject.drawable import Window

from s3wm_core.atoms import S3WMAtoms
from s3wm_core.keymap import get_key_action, init_keymap
from s3wm_core.s3screen import S3screen
from s3wm_core.s3window import S3window

EVENT_HANDLER_MAP = frozendict(
    {
        X.KeyPress: "handle_keypress",
        X.ButtonPress: None,
        X.MotionNotify: None,
        X.ButtonRelease: None,
        X.MapRequest: "handle_map",
        X.ConfigureRequest: None,
        X.UnmapNotify: "handle_unmap",
        X.EnterNotify: "handle_focus_in",
        X.LeaveNotify: "handle_focus_out",
        X.DestroyNotify: "handle_destroy",
        X.MapNotify: None,
    },
)


class S3WM:
    """
    Main window manager class.

    This class is a bunch of X11 callbacks and setup functions.
    Main
    """

    def __init__(self, cli_args: Optional[Namespace] = None) -> None:
        """
        Initialize S3WM.

        Initialization process includes
        establishing connection to the display
        and initialization of a chosen layout.
        """
        from s3wm_core import wm_config  # noqa: WPS433

        if cli_args is None:
            cli_args = Namespace()
        self.cli_args = cli_args
        self.display = Display()
        self.config = wm_config
        self.layout = wm_config.layout(self)
        self.windows: List[S3window] = []  # made for dynamic layout switching.
        font = self.display.open_font("cursor")
        cursor = font.create_glyph_cursor(  # noqa: WPS317
            font,
            left_ptr,
            left_ptr + 1,
            (0, 0, 0),
            (65535, 65535, 65535),
        )
        self.display.screen().root.change_attributes(cursor=cursor)
        self.atoms = S3WMAtoms.init_atoms(self.display)
        S3window._atoms = self.atoms  # noqa: WPS437

    def run(self) -> None:
        """Runs window manager."""
        display = self.display
        init_keymap(display)
        startup = getattr(
            self.config,
            "startup",
            lambda: logger.debug("No startup actions found"),
        )
        self._set_up_listeners()
        self._setup_root_window()
        startup()
        while True:
            try:
                self._handle_next_event()
            except KeyboardInterrupt:
                logger.info("Graceful Exiting")
                break
            except Exception as exc:
                logger.exception(exc)

    def handle_map(self, map_event: MapRequest) -> None:
        """
        Map window to layout.

        Map events called when new window is created.
        At this point we need to calculate the size of
        window and place it nicely at your workspace.

        :param map_event: X11 event for mapping
        """
        logger.debug("Map request")
        window = S3window(map_event.window, S3screen(self.display.screen()))

        if window.check_window_state(self.atoms.fd.window_state.fullscreen):
            window.move(0, 0)
            window.resize(100, 100, percents=True)
            window.map()
            return

        if window.check_window_state(self.atoms.fd.window_state.modal):
            screen_geom = window.screen.geom
            if window.geom:
                window.move(
                    screen_geom.width - (window.geom.width // 2),
                    screen_geom.height - (window.geom.height // 2),
                )
            window.map()
            return

        self._manage_window(window)

    def handle_keypress(self, key_event: KeyPress) -> None:
        """
        Run command on keypress.

        This event called when user using defined key combination and run task
        assigned to this combination.

        :param key_event: Key combination.
        """
        action = get_key_action(key_event)
        if not action:
            return
        if callable(action):
            logger.debug("Found python function")
            action(self)
        else:
            logger.debug(f"Running os command: '{action}'")
            Popen(action, start_new_session=True)

    def handle_destroy(self, destroy_event: DestroyNotify) -> None:
        """
        Called to destroy window.

        This function will be triggered when window is destroyed.
        :param destroy_event: X11 event.
        """
        window = S3window(destroy_event.window, S3screen(self.display.screen()))
        if window in self.windows:
            self.windows.remove(window)
        self.layout.remove_window(window)

    def handle_unmap(self, unmap_event: UnmapNotify) -> None:
        """
        Called to unmap window and remove it from the screen.

        This function will be triggered when window is unmapped.
        :param unmap_event: X11 event.
        """
        window = S3window(unmap_event.window, S3screen(self.display.screen()))
        if window in self.windows:
            self.windows.remove(window)
        self.layout.remove_window(window)
        window.unmap()

    def handle_focus_in(self, enter_event: EnterNotify) -> None:
        """
        Called when window gets focus.

        :param enter_event: X11 event.
        """
        window = S3window(enter_event.window, S3screen(self.display.screen()))
        if window.is_root:
            return
        self.layout.focus_in(window)

    def handle_focus_out(self, leave_event: LeaveNotify) -> None:
        """
        Called when window lose focus.

        :param leave_event: X11 event.
        """
        window = S3window(leave_event.window, S3screen(self.display.screen()))
        if window.is_root:
            return
        self.layout.focus_out(window)

    def _handle_next_event(self) -> None:  # , WPS231
        """Request next event from X11 and handle it."""
        event = self.display.next_event()
        logger.debug(f"Received event: {event.__class__}")
        if event.type in EVENT_HANDLER_MAP:
            handler_name = EVENT_HANDLER_MAP.get(event.type)
            if not handler_name:
                return
            event_handler = getattr(self, handler_name)
            if event_handler:
                logger.debug(f"Found event_handler: {handler_name}")
                logger.debug(f"Event info: {event}")
                event_handler(event)
                logger.debug("event handled")

    def _set_up_listeners(self) -> None:
        """
        Setup event catching.

        Configure the root window to receive all events
        needed for managing windows.
        """
        mask = (
            X.SubstructureRedirectMask
            | X.StructureNotifyMask
            | X.UnmapNotify
            | X.EnterWindowMask
            | X.LeaveWindowMask
            | X.FocusChangeMask
        )
        self.display.screen().root.change_attributes(event_mask=mask)

    def _setup_root_window(self) -> None:
        """
        Setting up main window.

        This function will set all needed variables to
        the Root window.
        """
        logger.debug("Setting up root window")

        if not hasattr(self.cli_args, "wm_name"):  # noqa: WPS421
            return

        root_window: Window = self.display.screen().root
        root_window.change_property(
            self.atoms.fd.net_wm_check,
            self.atoms.x11.type_window,
            format=32,  # noqa: WPS432
            data=[root_window.id],
        )
        root_window.change_text_property(
            self.atoms.fd.net_wm_name,
            self.atoms.x11.type_utf8_string,
            self.cli_args.wm_name,
        )
        self.display.sync()

    def _manage_window(self, window: S3window) -> None:
        """
        Register window in s3wm.

        :param window: new window.
        """
        self.windows.append(window)
        window.map()
        self.layout.add_window(window)
        mask = X.EnterWindowMask | X.LeaveWindowMask
        window.window.change_attributes(event_mask=mask)
