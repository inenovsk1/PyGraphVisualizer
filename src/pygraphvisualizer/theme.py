"""Colors used to show each State (Material Theme palette)."""

from pygraphvisualizer.board import State

type Color = tuple[int, int, int]

BACKGROUND: Color = (38, 49, 50)
GRID: Color = (96, 124, 139)

STATE_COLORS: dict[State, Color] = {
    State.EMPTY: BACKGROUND,
    State.BARRIER: (176, 190, 196),
    State.CLOSED: (255, 81, 81),
    State.OPEN: (105, 240, 173),
    State.START: (64, 196, 254),
    State.END: (255, 215, 63),
    State.PATH: (81, 45, 168),
}
