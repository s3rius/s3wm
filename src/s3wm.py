import logging
import subprocess

import src.config as config
from src.keymap import get_key_action, init_keymap
from Xlib import X
from Xlib.display import Display
from Xlib.protocol.event import DestroyNotify, KeyPress

logger = logging.getLogger(__name__)


class S3WM:
    """
    Main window manager class.
    This class is a bunch of X11 callbacks.
    """

    def __init__(self):
        """
        Initialization process includes
        establishing connection to the display
        and initialization of a chosen layout.
        """
        self.active_window = None
        self.display = Display()
        self.layout = config.layout(self)

    def handle_map(self, map_event):
        """
        Map events called when new window is created.
        At this point we need to calculate the size of
        window and place it nicely at your workspace.
        :param map_event: X11 event for mapping
        """
        logger.debug("Mapping window")
        window = map_event.window
        window.map()
        self.layout.add_window(window, self.display.screen())
        mask = X.EnterWindowMask | X.LeaveWindowMask
        logger.info(f"{window.__class__}")
        window.change_attributes(event_mask=mask)

    def handle_keypress(self, key_event: KeyPress):
        """
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
            subprocess.Popen(action, shell=True)

    def handle_destroy(self, destroy_event: DestroyNotify):
        """
        This function will be triggered when window is destroyed.
        :param destroy_event:
        :return:
        """
        self.layout.remove_window(destroy_event.window, self.display.screen())

    def catch_events(self):
        """Configure the root window to receive all events needed for managing
        windows."""
        mask = (
            X.SubstructureRedirectMask
            | X.SubstructureNotifyMask
            | X.EnterWindowMask
            | X.LeaveWindowMask
            | X.FocusChangeMask
        )
        self.display.screen().root.change_attributes(event_mask=mask)

    def setup_root(self):
        """
        Setting up main window.
        This function will set all needed variables to
        this WindowManager.
        """
        root_window = self.display.screen().root
        wm_name = self.display.intern_atom("_NET_WM_NAME")
        utf_string = self.display.intern_atom("UTF8_STRING")
        # That thing needed only for Java applications.
        # Because Java can't handle custom window managers.
        root_window.change_text_property(wm_name, utf_string, "LG3D")
        self.display.sync()

    def run(self):
        display = self.display
        init_keymap(display)
        startup = getattr(
            config, "startup", lambda: logger.debug("No startup actions found")
        )
        self.catch_events()
        self.setup_root()
        startup()
        while True:
            event = display.next_event()
            logger.debug(event.__class__)
            if event.type in config.EVENT_HANDLER_MAP:
                logger.debug(f"Handling event: {event.type}")
                handler_name = config.EVENT_HANDLER_MAP[event.type]
                if not handler_name:
                    continue
                handler = getattr(self, handler_name)
                if handler:
                    handler(event)
                    print("#" * 100)
