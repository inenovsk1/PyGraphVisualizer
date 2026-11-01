"""The Board: an N x N field of Nodes, each with a State."""

import enum
from collections.abc import Iterator
from typing import NamedTuple


class State(enum.Enum):
    """What a Node currently is."""

    EMPTY = enum.auto()
    START = enum.auto()
    END = enum.auto()
    BARRIER = enum.auto()
    OPEN = enum.auto()
    CLOSED = enum.auto()
    PATH = enum.auto()


# States a Search is allowed to paint, and the only ones it may paint over.
_SEARCH_STATES = frozenset({State.OPEN, State.CLOSED, State.PATH})
_PAINTABLE = frozenset({State.EMPTY, *_SEARCH_STATES})


class Node(NamedTuple):
    """A single square on the Board, identified by its column ``x`` and row ``y``."""

    x: int
    y: int


class Board:
    """The square field the user draws on and an Algorithm searches."""

    def __init__(self, size: int) -> None:
        self.size = size
        self._states: dict[Node, State] = {node: State.EMPTY for node in self._all_nodes()}
        self.start: Node | None = None
        self.end: Node | None = None

    def _all_nodes(self) -> Iterator[Node]:
        for x in range(self.size):
            for y in range(self.size):
                yield Node(x, y)

    def __contains__(self, node: object) -> bool:
        return node in self._states

    @property
    def ready(self) -> bool:
        """Whether both Start and End are placed, so a Search can run."""
        return self.start is not None and self.end is not None

    def nodes(self) -> Iterator[Node]:
        return iter(self._states)

    def state(self, node: Node) -> State:
        return self._states[node]

    def neighbors(self, node: Node) -> list[Node]:
        """Adjacent (up/down/left/right) Nodes that are not Barriers."""
        candidates = (
            Node(node.x + 1, node.y),
            Node(node.x - 1, node.y),
            Node(node.x, node.y + 1),
            Node(node.x, node.y - 1),
        )
        return [n for n in candidates if n in self and self._states[n] is not State.BARRIER]

    def place(self, node: Node) -> None:
        """Handle a click: the first places Start, the second End, further ones Barriers."""
        if self._states[node] not in _PAINTABLE:
            return
        if self.start is None:
            self.start = node
            self._states[node] = State.START
        elif self.end is None:
            self.end = node
            self._states[node] = State.END
        else:
            self._states[node] = State.BARRIER

    def erase(self, node: Node) -> None:
        self._states[node] = State.EMPTY
        if node == self.start:
            self.start = None
        elif node == self.end:
            self.end = None

    def mark(self, node: Node, state: State) -> None:
        """Paint a Node with a Search state, leaving Start, End and Barriers untouched."""
        if state not in _SEARCH_STATES:
            raise ValueError(f"A Search cannot paint {state.name}")
        if self._states[node] in _PAINTABLE:
            self._states[node] = state

    def clear_search(self) -> None:
        """Remove the Open, Closed and Path states left by a previous Search."""
        for node, state in self._states.items():
            if state in _SEARCH_STATES:
                self._states[node] = State.EMPTY
