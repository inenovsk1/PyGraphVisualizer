"""The Prompt: the panel shown over a finished Board, offering what to do next."""

import enum

import pygame
import pygame_gui

PANEL_SIZE = (380, 130)
BOTTOM_MARGIN = 24


class Choice(enum.Enum):
    CONTINUE = enum.auto()
    NEW_CONFIG = enum.auto()


class Prompt:
    def __init__(self, window_size: tuple[int, int], *, found: bool) -> None:
        width, height = window_size
        panel_width, panel_height = PANEL_SIZE
        self._manager = pygame_gui.UIManager(window_size)
        panel = pygame_gui.elements.UIPanel(
            pygame.Rect(
                (width - panel_width) // 2,
                height - panel_height - BOTTOM_MARGIN,
                panel_width,
                panel_height,
            ),
            manager=self._manager,
        )
        pygame_gui.elements.UILabel(
            pygame.Rect(10, 10, panel_width - 40, 30),
            "Path found" if found else "No path found",
            manager=self._manager,
            container=panel,
        )
        self.continue_button = pygame_gui.elements.UIButton(
            pygame.Rect(10, 55, 160, 40),
            "Continue",
            manager=self._manager,
            container=panel,
            tool_tip_text="Same Config, new empty board (ENTER)",
        )
        self.new_config_button = pygame_gui.elements.UIButton(
            pygame.Rect(190, 55, 160, 40),
            "New config",
            manager=self._manager,
            container=panel,
            tool_tip_text="Back to the Menu",
        )

    def handle_event(self, event: pygame.event.Event) -> Choice | None:
        self._manager.process_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return Choice.CONTINUE
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element is self.continue_button:
                return Choice.CONTINUE
            if event.ui_element is self.new_config_button:
                return Choice.NEW_CONFIG
        return None

    def update(self, time_delta: float) -> None:
        self._manager.update(time_delta)

    def draw(self, surface: pygame.Surface) -> None:
        self._manager.draw_ui(surface)
