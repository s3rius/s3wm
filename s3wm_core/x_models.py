from pydantic import BaseConfig, BaseModel


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
