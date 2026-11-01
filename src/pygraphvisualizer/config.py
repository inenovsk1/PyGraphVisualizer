"""The Config a user chooses in the Menu: Board size, Algorithm and Speed. No pygame."""

from dataclasses import dataclass
from enum import Enum

MIN_BOARD_SIZE = 2
MAX_BOARD_SIZE = 200


@dataclass(frozen=True, slots=True)
class _Level:
    label: str
    steps_per_frame: float
    path_pixels_per_frame: float


class Speed(Enum):
    """How fast a Search and its Path are shown.

    ``steps_per_frame`` is how many Steps of the Search are consumed each frame (a
    fraction means a Step every few frames). ``path_pixels_per_frame`` is how far the
    Path animation's circle grows each frame.
    """

    SLOW = _Level("Slow", 0.25, 0.5)
    NORMAL = _Level("Normal", 1, 1)
    FAST = _Level("Fast", 4, 3)
    XFAST = _Level("xFast", 16, 8)
    ULTRA = _Level("Ultra", 32, 16)

    @property
    def label(self) -> str:
        return self.value.label

    @property
    def steps_per_frame(self) -> float:
        return self.value.steps_per_frame

    @property
    def path_pixels_per_frame(self) -> float:
        return self.value.path_pixels_per_frame


@dataclass(frozen=True, slots=True)
class Config:
    board_size: int
    algo: str
    speed: Speed


DEFAULT_CONFIG = Config(board_size=30, algo="BFS", speed=Speed.NORMAL)


def parse_board_size(text: str) -> int:
    """Turn typed text into a Board size, or raise ValueError saying why it is not allowed."""
    try:
        size = int(text)
    except ValueError:
        raise ValueError(f"{text.strip()!r} is not an integer") from None
    if not MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE:
        raise ValueError(f"must be between {MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}, got {size}")
    return size
