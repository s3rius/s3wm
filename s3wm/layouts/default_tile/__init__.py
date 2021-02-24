"""Default tile layout. Similar to DWM's default."""
from s3wm.layouts.default_tile.key_bindings import (
    change_gaps,
    change_tab,
    kill_focused_window,
    move_focus,
    move_window_to_tab,
)
from s3wm.layouts.default_tile.layout import DefaultTile

__all__ = [
    "DefaultTile",
    "kill_focused_window",
    "move_focus",
    "move_window_to_tab",
    "change_tab",
    "change_gaps",
]
