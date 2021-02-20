from typing import Any, Callable, Optional, Union

from Xlib import XK, X


class KeyCombination:
    """Used to add global key combinations."""

    default_mod_key = X.Mod4Mask

    def __init__(  # noqa: WPS234
        self,
        modifiers: int = X.NONE,
        key: Optional[Union[str, int]] = None,
        action: Optional[Union[Callable[..., Any], str]] = None,
    ) -> None:
        self.modifiers = modifiers  # Event masks such as Mod4Mask
        self.key = key  # Key of event
        if isinstance(key, str):
            self.key = XK.string_to_keysym(key)
        self.action = action  # Action to perform when event pressed

    def __repr__(self) -> str:
        return f"{{key:{self.key} mod:{self.modifiers}"
