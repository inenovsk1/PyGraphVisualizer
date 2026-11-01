"""A Session: one Board drawn with one Config, for exactly one Search and its Path animation."""

from collections.abc import Iterator
from dataclasses import replace

import pygame

from pygraphvisualizer.algorithms import ALGORITHMS, Step, apply_step
from pygraphvisualizer.board import Board
from pygraphvisualizer.config import Config
from pygraphvisualizer.prompt import Choice, Prompt
from pygraphvisualizer.screen import OpenMenu, StartSession, Transition
from pygraphvisualizer.view import BoardView, PathAnimation


class Session:
    def __init__(
        self, surface: pygame.Surface, config: Config, window_size: tuple[int, int]
    ) -> None:
        self.config = config
        self.board = Board(config.board_size)
        self.prompt: Prompt | None = None
        self._surface = surface
        self._window_size = window_size
        self._view = BoardView(surface, config.board_size, *window_size)
        self._search: Iterator[Step] | None = None
        self._animation: PathAnimation | None = None
        self._step_budget = 0.0

    @property
    def finished(self) -> bool:
        """Whether the Search and Path animation are over and the Prompt is showing."""
        return self.prompt is not None

    @property
    def _busy(self) -> bool:
        return self._search is not None or self._animation is not None

    def handle_event(self, event: pygame.event.Event) -> Transition | None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return OpenMenu()
        if self.prompt is not None:
            choice = self.prompt.handle_event(event)
            if choice is Choice.CONTINUE:
                return StartSession(self.config)
            if choice is Choice.NEW_CONFIG:
                return OpenMenu()
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self._reset()
            elif event.key == pygame.K_SPACE:
                self._start_search()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._edit(event.pos, left=event.button == 1, right=event.button == 3, drag=False)
        elif event.type == pygame.MOUSEMOTION:
            self._edit(event.pos, left=event.buttons[0], right=event.buttons[2], drag=True)
        return None

    def update(self, time_delta: float) -> None:
        if self.prompt is not None:
            self.prompt.update(time_delta)
        elif self._search is not None:
            self._advance_search()
        elif self._animation is not None:
            self._advance_animation()

    def draw(self) -> None:
        self._view.draw(self.board, self._animation)
        if self.prompt is not None:
            self.prompt.draw(self._surface)

    def _reset(self) -> None:
        self.board = Board(self.config.board_size)
        self._search = None
        self._animation = None

    def _edit(self, pos: tuple[int, int], *, left: bool, right: bool, drag: bool) -> None:
        node = self._view.node_at(pos)
        if node is None or self._busy:
            return
        if right:
            self.board.erase(node)
        elif left and (self.board.ready or not drag):
            self.board.place(node)

    def _start_search(self) -> None:
        board = self.board
        if self._busy or board.start is None or board.end is None:
            return
        board.clear_search()
        self._step_budget = 0.0
        self._search = ALGORITHMS[self.config.algo](board, board.start, board.end)

    def _advance_search(self) -> None:
        """Consume as many Steps as the Speed allows this frame."""
        self._step_budget += self.config.speed.steps_per_frame
        while self._step_budget >= 1 and self._search is not None:
            self._step_budget -= 1
            step = next(self._search, None)
            if step is None:
                self._search = None
                self._finish(found=False)
                return
            # The Path is revealed by the animation rather than painted all at once
            apply_step(self.board, replace(step, path=None))
            if step.path is not None:
                self._animation = PathAnimation(step.path)
                self._search = None

    def _advance_animation(self) -> None:
        assert self._animation is not None
        self._animation.advance(
            self.board, self._view.cell_height, self.config.speed.path_pixels_per_frame
        )
        if self._animation.finished:
            self._animation = None
            self._finish(found=True)

    def _finish(self, *, found: bool) -> None:
        self.prompt = Prompt(self._window_size, found=found)
