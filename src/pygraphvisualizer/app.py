"""The pygame application: window, input handling and the main loop."""

from collections.abc import Iterator
from dataclasses import replace

import pygame

from pygraphvisualizer.algorithms import ALGORITHMS, Step, apply_step
from pygraphvisualizer.board import Board
from pygraphvisualizer.cli import Options, parse_args
from pygraphvisualizer.view import BoardView, PathAnimation

FPS = 60
WINDOW_SIZE = (1280, 720)


class App:
    def __init__(self, options: Options) -> None:
        self._options = options
        pygame.init()
        if options.fullscreen:
            screen = pygame.display.set_mode()
            pygame.display.toggle_fullscreen()
        else:
            screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("PyGraphVisualizer")

        info = pygame.display.Info()
        self._view = BoardView(screen, options.board_size, info.current_w, info.current_h)
        self._clock = pygame.time.Clock()
        self._reset()

    def _reset(self) -> None:
        self._board = Board(self._options.board_size)
        self._search: Iterator[Step] | None = None
        self._animation: PathAnimation | None = None

    @property
    def _busy(self) -> bool:
        return self._search is not None or self._animation is not None

    def run(self) -> None:
        while self._handle_events():
            self._advance()
            self._view.draw(self._board, self._animation)
            self._clock.tick(FPS)
        pygame.quit()

    def _handle_events(self) -> bool:
        """Process input. Returns False when the app should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_TAB:
                    self._reset()
                elif event.key == pygame.K_SPACE:
                    self._start_search()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._edit(event.pos, left=event.button == 1, right=event.button == 3, drag=False)
            elif event.type == pygame.MOUSEMOTION:
                self._edit(event.pos, left=event.buttons[0], right=event.buttons[2], drag=True)
        return True

    def _edit(self, pos: tuple[int, int], *, left: bool, right: bool, drag: bool) -> None:
        node = self._view.node_at(pos)
        if node is None or self._busy:
            return
        if right:
            self._board.erase(node)
        elif left and (self._board.ready or not drag):
            self._board.place(node)

    def _start_search(self) -> None:
        board = self._board
        if self._busy or board.start is None or board.end is None:
            return
        board.clear_search()
        self._search = ALGORITHMS[self._options.algo](board, board.start, board.end)

    def _advance(self) -> None:
        """Move the running Search (or the Path animation) forward by one frame."""
        if self._search is not None:
            step = next(self._search, None)
            if step is None:
                self._search = None
            else:
                # The Path is revealed by the animation rather than painted all at once
                apply_step(self._board, replace(step, path=None))
                if step.path is not None:
                    self._animation = PathAnimation(step.path)
                    self._search = None
        elif self._animation is not None:
            self._animation.advance(self._board, self._view.cell_height)
            if self._animation.finished:
                self._animation = None


def main() -> None:
    App(parse_args()).run()
