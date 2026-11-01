"""The Menu: where the user chooses a Config before a Session."""

import pygame
import pygame_gui

from pygraphvisualizer.algorithms import ALGORITHMS
from pygraphvisualizer.config import (
    MAX_BOARD_SIZE,
    MIN_BOARD_SIZE,
    Config,
    Speed,
    parse_board_size,
)
from pygraphvisualizer.screen import Quit, StartSession, Transition
from pygraphvisualizer.theme import BACKGROUND

COLUMN_WIDTH = 380
FIELD_WIDTH = 190
ROW_HEIGHT = 32


class Menu:
    def __init__(
        self, surface: pygame.Surface, config: Config, window_size: tuple[int, int]
    ) -> None:
        self._surface = surface
        self._window_size = window_size
        self.error = ""
        self.choose(config)

    @property
    def config(self) -> Config | None:
        """The Config currently shown, or None while the Board size is not allowed."""
        try:
            board_size = parse_board_size(self._size_entry.get_text())
        except ValueError:
            return None
        algo = self._algo_dropdown.selected_option[0]
        speed = next(s for s in Speed if s.label == self._speed_dropdown.selected_option[0])
        return Config(board_size, algo, speed)

    def choose(self, config: Config) -> None:
        """Show these values, replacing whatever is currently entered."""
        self._build(config)

    def enter_board_size(self, text: str) -> None:
        self._size_entry.set_text(text)

    def handle_event(self, event: pygame.event.Event) -> Transition | None:
        self._manager.process_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return Quit()
            if event.key == pygame.K_RETURN:
                return self._start()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element is self._start_button:
            return self._start()
        return None

    def update(self, time_delta: float) -> None:
        self._validate()
        self._manager.update(time_delta)

    def draw(self) -> None:
        self._surface.fill(BACKGROUND)
        self._manager.draw_ui(self._surface)

    def _start(self) -> Transition | None:
        config = self.config
        return StartSession(config) if config is not None else None

    def _validate(self) -> None:
        """Explain why the typed Board size is not allowed, and gate the Start button."""
        try:
            parse_board_size(self._size_entry.get_text())
        except ValueError as problem:
            error = f"Board size {problem}"
        else:
            error = ""
        if error == self.error and self._start_button.is_enabled == (error == ""):
            return
        self.error = error
        self._error_label.set_text(error)
        if error:
            self._start_button.disable()
        else:
            self._start_button.enable()

    def _build(self, config: Config) -> None:
        width, height = self._window_size
        left = (width - COLUMN_WIDTH) // 2
        top = height // 2 - 170
        field_left = left + COLUMN_WIDTH - FIELD_WIDTH

        def row(y: int, x: int = left, w: int = COLUMN_WIDTH - FIELD_WIDTH) -> pygame.Rect:
            return pygame.Rect(x, top + y, w, ROW_HEIGHT)

        self._manager = pygame_gui.UIManager(self._window_size)
        manager = self._manager
        label_width = COLUMN_WIDTH - FIELD_WIDTH - 10
        pygame_gui.elements.UILabel(
            pygame.Rect(left, top, COLUMN_WIDTH, 40), "PyGraphVisualizer", manager=manager
        )

        pygame_gui.elements.UILabel(
            row(60, w=label_width),
            f"Board size ({MIN_BOARD_SIZE}-{MAX_BOARD_SIZE})",
            manager=manager,
        )
        self._size_entry = pygame_gui.elements.UITextEntryLine(
            row(60, field_left, FIELD_WIDTH), manager=manager, initial_text=str(config.board_size)
        )
        self._size_entry.set_allowed_characters("numbers")
        self._error_label = pygame_gui.elements.UILabel(
            pygame.Rect(left, top + 96, COLUMN_WIDTH, 24), "", manager=manager
        )

        pygame_gui.elements.UILabel(row(135, w=label_width), "Algorithm", manager=manager)
        self._algo_dropdown = pygame_gui.elements.UIDropDownMenu(
            list(ALGORITHMS), config.algo, row(135, field_left, FIELD_WIDTH), manager=manager
        )

        pygame_gui.elements.UILabel(row(180, w=label_width), "Speed", manager=manager)
        self._speed_dropdown = pygame_gui.elements.UIDropDownMenu(
            [speed.label for speed in Speed],
            config.speed.label,
            row(180, field_left, FIELD_WIDTH),
            manager=manager,
        )

        self._start_button = pygame_gui.elements.UIButton(
            pygame.Rect(left + (COLUMN_WIDTH - 240) // 2, top + 250, 240, 44),
            "Start",
            manager=manager,
        )
        self.error = ""
        self._validate()
