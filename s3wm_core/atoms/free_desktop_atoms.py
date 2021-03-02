from Xlib.display import Display

from s3wm_core.atoms.base import BaseAtomGroup


class WindowState(BaseAtomGroup):
    """
    Window states atoms for FreeDesktop.

    https://specifications.freedesktop.org/wm-spec/1.4/ar01s05.html#idm46789185844304
    """

    wm_state_type: int

    modal: int
    sticky: int
    maximized_vert: int
    maximized_horz: int
    shaded: int
    skip_taskbar: int
    skip_pager: int
    hidden: int
    fullscreen: int
    above: int
    below: int
    demands_attention: int

    @staticmethod
    def init_atoms(display: Display) -> "WindowState":
        return WindowState(
            wm_state_type=display.intern_atom("_NET_WM_STATE"),
            modal=display.intern_atom("_NET_WM_STATE_MODAL"),
            sticky=display.intern_atom("_NET_WM_STATE_MODAL"),
            maximized_vert=display.intern_atom("_NET_WM_STATE_MAXIMIZED_VERT"),
            maximized_horz=display.intern_atom("_NET_WM_STATE_MAXIMIZED_HORZ"),
            shaded=display.intern_atom("_NET_WM_STATE_SHADED"),
            skip_taskbar=display.intern_atom("_NET_WM_STATE_SKIP_TASKBAR"),
            skip_pager=display.intern_atom("_NET_WM_STATE_SKIP_PAGER"),
            hidden=display.intern_atom("_NET_WM_STATE_HIDDEN"),
            fullscreen=display.intern_atom("_NET_WM_STATE_FULLSCREEN"),
            above=display.intern_atom("_NET_WM_STATE_ABOVE"),
            below=display.intern_atom("_NET_WM_STATE_BELOW"),
            demands_attention=display.intern_atom("_NET_WM_STATE_DEMANDS_ATTENTION"),
        )


class WindowTypes(BaseAtomGroup):
    """
    Window types from FreeDesktop specification.

    https://specifications.freedesktop.org/wm-spec/wm-spec-latest.html#idm46291029767696
    """

    window_type: int

    desktop: int
    dock: int
    toolbar: int
    menu: int
    utility: int
    splash: int
    dialog: int
    dropdown: int
    popup: int
    tooltip: int
    notification: int
    combo: int
    dnd: int
    normal: int

    @staticmethod
    def init_atoms(display: Display) -> "WindowTypes":
        return WindowTypes(
            window_type=display.intern_atom("_NET_WM_WINDOW_TYPE"),
            desktop=display.intern_atom("_NET_WM_WINDOW_TYPE_DESKTOP"),
            dock=display.intern_atom("_NET_WM_WINDOW_TYPE_DOCK"),
            toolbar=display.intern_atom("_NET_WM_WINDOW_TYPE_TOOLBAR"),
            menu=display.intern_atom("_NET_WM_WINDOW_TYPE_MENU"),
            utility=display.intern_atom("_NET_WM_WINDOW_TYPE_UTILITY"),
            splash=display.intern_atom("_NET_WM_WINDOW_TYPE_SPLASH"),
            dialog=display.intern_atom("_NET_WM_WINDOW_TYPE_DIALOG"),
            dropdown=display.intern_atom("_NET_WM_WINDOW_TYPE_DROPDOWN_MENU"),
            popup=display.intern_atom("_NET_WM_WINDOW_TYPE_POPUP_MENU"),
            tooltip=display.intern_atom("_NET_WM_WINDOW_TYPE_TOOLTIP"),
            notification=display.intern_atom("_NET_WM_WINDOW_TYPE_NOTIFICATION"),
            combo=display.intern_atom("_NET_WM_WINDOW_TYPE_COMBO"),
            dnd=display.intern_atom("_NET_WM_WINDOW_TYPE_DND"),
            normal=display.intern_atom("_NET_WM_WINDOW_TYPE_NORMAL"),
        )


class FreeDesktopAtoms(BaseAtomGroup):
    net_wm_name: int
    net_wm_check: int
    net_wm_state_fullscreen: int
    net_active_window: int
    net_client_list: int

    window_types: WindowTypes
    window_state: WindowState

    @staticmethod
    def init_atoms(display: Display) -> "FreeDesktopAtoms":
        return FreeDesktopAtoms(
            net_wm_name=display.intern_atom("_NET_WM_NAME"),
            net_wm_check=display.intern_atom("_NET_SUPPORTING_WM_CHECK"),
            net_wm_state_fullscreen=display.intern_atom("_NET_WM_STATE_FULLSCREEN"),
            net_active_window=display.intern_atom("_NET_ACTIVE_WINDOW"),
            net_client_list=display.intern_atom("_NET_CLIENT_LIST"),
            # Window types
            window_types=WindowTypes.init_atoms(display),
            window_state=WindowState.init_atoms(display),
        )
