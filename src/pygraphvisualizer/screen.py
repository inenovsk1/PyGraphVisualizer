"""What the App shows in its one window: a Screen, and how one Screen hands over to another."""

from dataclasses import dataclass
from typing import Protocol

import pygame

from pygraphvisualizer.config import Config


@dataclass(frozen=True, slots=True)
class StartSession:
    """Leave the current Screen and begin a Session with this Config."""

    config: Config


@dataclass(frozen=True, slots=True)
class OpenMenu:
    """Leave the current Screen and show the Menu."""


@dataclass(frozen=True, slots=True)
class Quit:
    """Close the program."""


Transition = StartSession | OpenMenu | Quit


class Screen(Protocol):
    def handle_event(self, event: pygame.event.Event) -> Transition | None:
        """React to one event. Returns a Transition when the App should switch Screens."""
        ...

    def update(self, time_delta: float) -> None:
        """Advance by one frame."""
        ...

    def draw(self) -> None:
        """Draw onto the display surface. The App flips the display."""
        ...
