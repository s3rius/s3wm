"""
Core functions and modules for S3WM.

It's usable for creating new layout managers and stuff.
"""
from s3wm_core.key_combination import KeyCombination
from s3wm_core.keymap import kill_wm
from s3wm_core.layout_base import AbstractLayoutManager
from s3wm_core.s3screen import S3screen
from s3wm_core.s3window import S3window
from s3wm_core.x_models import ScreenGeometry, WindowGeometry

__all__ = [
    "kill_wm",
    "S3window",
    "S3screen",
    "KeyCombination",
    "WindowGeometry",
    "ScreenGeometry",
    "AbstractLayoutManager",
]
