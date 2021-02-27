from subprocess import Popen
from typing import List

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

from s3wm_core.keymap import get_key_action, init_keymap
from s3wm_core.s3screen import S3screen
from s3wm_core.s3window import S3window
from s3wm_core.x_models import XMapState, XWMState

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

    def __init__(self) -> None:
        """
        Initialize S3WM.

        Initialization process includes
        establishing connection to the display
        and initialization of a chosen layout.
        """
        from s3wm_core import wm_config  # noqa: WPS433

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

    def run(self) -> None:
        """Runs window manager."""
        display = self.display
        init_keymap(display)
        startup = getattr(
            self.config,
            "startup",
            lambda: logger.debug("No startup actions found"),
        )
        self._catch_events()
        self._setup_root()
        startup()
        self._reload_windows()
        while True:  # noqa: WPS457
            self._handle_next_event()

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
        attrs = window.attributes
        if not attrs:
            return
        if attrs.override_redirect:
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
            Popen(action, shell=True)

    def handle_destroy(self, destroy_event: DestroyNotify) -> None:
        """
        Called to destroy window.

        This function will be triggered when window is destroyed.
        :param destroy_event: X11 event.
        """
        window = S3window(destroy_event.window, S3screen(self.display.screen()))
        if window in self.windows:
            self.windows.remove(window)
        window.wm_state = XWMState.WithdrawnState
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
        window.wm_state = XWMState.WithdrawnState
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

    def _handle_next_event(self) -> None:  # noqa: C901, WPS231
        """
        Request next event from X11 and handle it.

        :raises KeyboardInterrupt: if something has interrupted the main process.
        """
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
                try:
                    event_handler(event)
                except KeyboardInterrupt:  # noqa: WPS329
                    raise
                except Exception as exc:
                    logger.exception(exc)
                logger.debug("event handled")

    def _catch_events(self) -> None:
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

    def _setup_root(self) -> None:
        """
        Setting up main window.

        This function will set all needed variables to
        this WindowManager.
        """
        logger.debug("Setting up root window")
        root_window = self.display.screen().root
        wm_name = self.display.intern_atom("_NET_WM_NAME")
        utf_string = self.display.intern_atom("UTF8_STRING")
        # That thing needed only for Java applications.
        # Because Java can't handle custom window managers.
        root_window.change_text_property(wm_name, utf_string, "LG3D")
        self.display.sync()

    def _manage_window(self, window: S3window) -> None:
        """
        Register window in s3wm.

        :param window: new window.
        """
        self.windows.append(window)
        window.wm_state = XWMState.NormalState
        window.map()
        self.layout.add_window(window)
        mask = X.EnterWindowMask | X.LeaveWindowMask
        window.window.change_attributes(event_mask=mask)

    def _reload_main_windows(self, children: List[S3window]) -> None:
        """
        Try to reload normal windows.

        :param children: windows in memory.
        """
        logger.debug("Reloading ordinary windows")
        for window in children:
            attrs = window.attributes
            if not attrs:
                continue
            wm_state = window.wm_state
            if wm_state is None:
                continue
            transient = window.get_transient()
            if transient:
                continue
            if (  # noqa: WPS337
                attrs.map_state == XMapState.IsViewable
                or wm_state == XWMState.IconicState
            ):
                self._manage_window(window)

    def _reload_transient(self, children: List[S3window]) -> None:
        """
        Try to redraw transient windows.

        :param children: windows in memory.
        """
        logger.debug("Reloading transient windows")
        for window in children:
            attrs = window.attributes
            if not attrs:
                continue
            wm_state = window.wm_state
            if not wm_state:
                continue
            transient = window.get_transient()
            if transient and (  # noqa: WPS337
                attrs.map_state == XMapState.IsViewable
                or wm_state == XWMState.IconicState
            ):
                self._manage_window(window)

    def _reload_windows(self) -> None:
        """Query root window for children and render them if we can."""
        response = self.display.screen().root.query_tree()
        screen = S3screen(self.display.screen())
        children = list(map(lambda win: S3window(win, screen), response.children))
        self._reload_main_windows(children)
        self._reload_transient(children)
