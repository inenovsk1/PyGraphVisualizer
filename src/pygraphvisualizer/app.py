"""The pygame application: the one window, and the loop that switches between Screens."""

import pygame

from pygraphvisualizer.cli import Options, parse_args
from pygraphvisualizer.menu import Menu
from pygraphvisualizer.screen import OpenMenu, Quit, Screen, StartSession, Transition
from pygraphvisualizer.session import Session

FPS = 60
WINDOW_SIZE = (1280, 720)


class App:
    def __init__(self, options: Options) -> None:
        pygame.init()
        if options.fullscreen:
            self._surface = pygame.display.set_mode()
            pygame.display.toggle_fullscreen()
        else:
            self._surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("PyGraphVisualizer")

        info = pygame.display.Info()
        self._window_size = (info.current_w, info.current_h)
        self._clock = pygame.time.Clock()
        self._config = options.initial_config()
        self.screen: Screen = Menu(self._surface, self._config, self._window_size)

    def run(self) -> None:
        running = True
        while running:
            running = self.tick(self._clock.tick(FPS) / 1000)
        pygame.quit()

    def tick(self, time_delta: float) -> bool:
        """Handle input, advance the current Screen and redraw. Returns False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            transition = self.screen.handle_event(event)
            if transition is not None and not self._switch(transition):
                return False
        self.screen.update(time_delta)
        self.screen.draw()
        pygame.display.flip()
        return True

    def _switch(self, transition: Transition) -> bool:
        """Show the Screen a Transition asks for. Returns False when it asks to quit."""
        match transition:
            case Quit():
                return False
            case StartSession(config):
                self._config = config
                self.screen = Session(self._surface, config, self._window_size)
            case OpenMenu():
                self.screen = Menu(self._surface, self._config, self._window_size)
        return True


def main() -> None:
    App(parse_args()).run()
