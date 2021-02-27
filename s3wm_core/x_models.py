from enum import Enum, unique
from typing import Union

from pydantic import BaseConfig, BaseModel
from Xlib.xobject.colormap import Colormap


class WindowGeometry(BaseModel):
    """X11 window geometry abstraction."""

    x: int  # noqa: WPS111
    y: int  # noqa: WPS111
    width: int
    height: int
    border_width: int
    depth: int
    sequence_number: int

    class Config(BaseConfig):
        """Model config."""

        orm_mode = True


class ScreenGeometry(BaseModel):
    """Screen geometry parameters."""

    width: int
    height: int

    class Config(BaseConfig):
        """Model config."""

        orm_mode = True


@unique
class XMapState(Enum):
    """Window map state."""

    IsUnmapped = 0  # window is unmapped
    IsUnviewable = 1  # You can't view this window
    IsViewable = 2  # This window can be viewable


@unique
class XWMState(Enum):
    """Window WM State."""

    WithdrawnState = 0  # windows that are not mapped
    NormalState = 1  # most applications want to start this way
    IconicState = 3  # application wants to start as an icon


class XWindowAttributes(BaseModel):
    """X11 window attributes."""

    backing_store: int
    sequence_number: int
    visual: int
    bit_gravity: int
    win_gravity: int
    backing_bit_planes: int
    backing_pixel: int
    save_under: int
    map_is_installed: int
    map_state: XMapState
    override_redirect: bool
    colormap: Union[int, Colormap]
    all_event_masks: int
    your_event_mask: int
    do_not_propagate_mask: int

    class Config(BaseConfig):
        """Model config."""

        orm_mode = True
        arbitrary_types_allowed = True
