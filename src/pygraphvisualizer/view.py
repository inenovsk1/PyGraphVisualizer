"""Drawing the Board with pygame."""

from collections import deque

import pygame

from pygraphvisualizer.board import Board, Node, State
from pygraphvisualizer.theme import BACKGROUND, GRID, STATE_COLORS


class PathAnimation:
    """Grows a circle in each Path Node in turn, then paints the Node as Path.

    Nodes are given in the order they should light up. The circle is drawn on top of
    the Node's current look, so a Node only becomes Path on the Board once its circle
    has filled the cell.
    """

    def __init__(self, nodes: tuple[Node, ...]) -> None:
        self._pending = deque(nodes)
        self._radius = 0

    @property
    def finished(self) -> bool:
        return not self._pending

    @property
    def current(self) -> Node | None:
        return self._pending[0] if self._pending else None

    @property
    def radius(self) -> int:
        return self._radius

    def advance(self, board: Board, cell_height: float) -> None:
        if not self._pending:
            return
        self._radius += 1
        if self._radius > int(cell_height) // 2:
            board.mark(self._pending.popleft(), State.PATH)
            self._radius = 0


class BoardView:
    """Maps between Board Nodes and screen pixels, and draws the Board."""

    def __init__(self, screen: pygame.Surface, board_size: int, width: int, height: int) -> None:
        self._screen = screen
        self._width = width
        self._height = height
        self.cell_width = width / board_size
        self.cell_height = height / board_size
        self._size = board_size

    def node_at(self, pos: tuple[int, int]) -> Node | None:
        """The Node under a pixel position, or None if it falls outside the Board."""
        x, y = pos
        node = Node(int(x // self.cell_width), int(y // self.cell_height))
        if 0 <= node.x < self._size and 0 <= node.y < self._size:
            return node
        return None

    def draw(self, board: Board, animation: PathAnimation | None = None) -> None:
        self._screen.fill(BACKGROUND)
        for node in board.nodes():
            color = STATE_COLORS[board.state(node)]
            self._screen.fill(color, self._rect(node))
        self._draw_grid_lines()
        if animation is not None and animation.current is not None and animation.radius > 0:
            rect = self._rect(animation.current)
            pygame.draw.circle(
                self._screen, STATE_COLORS[State.PATH], rect.center, animation.radius
            )
        pygame.display.flip()

    def _rect(self, node: Node) -> pygame.Rect:
        return pygame.Rect(
            round(node.x * self.cell_width),
            round(node.y * self.cell_height),
            round(self.cell_width) + 1,
            round(self.cell_height) + 1,
        )

    def _draw_grid_lines(self) -> None:
        for i in range(self._size):
            y = i * self.cell_height
            pygame.draw.aaline(self._screen, GRID, (0, y), (self._width, y))
            x = i * self.cell_width
            pygame.draw.aaline(self._screen, GRID, (x, 0), (x, self._height))
