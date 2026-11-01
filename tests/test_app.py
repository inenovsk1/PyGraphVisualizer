"""Headless smoke tests that drive the whole App through posted pygame events."""

from collections.abc import Iterator

import pygame
import pygame_gui
import pytest

from pygraphvisualizer.app import WINDOW_SIZE, App
from pygraphvisualizer.cli import Options
from pygraphvisualizer.config import DEFAULT_CONFIG, Config, Speed
from pygraphvisualizer.menu import Menu
from pygraphvisualizer.session import Session

FRAME = 1 / 60
MAX_FRAMES = 5000


@pytest.fixture
def make_app(monkeypatch: pytest.MonkeyPatch) -> Iterator[type[App]]:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    yield App
    pygame.quit()


def press(key: int) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, unicode="", mod=0))


def click(pos: tuple[int, int], button: int = 1) -> None:
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button))


def click_node(size: int, x: int, y: int) -> None:
    width, height = WINDOW_SIZE
    click((int((x + 0.5) * width / size), int((y + 0.5) * height / size)))


def menu_of(app: App) -> Menu:
    assert isinstance(app.screen, Menu)
    return app.screen


def session_of(app: App) -> Session:
    assert isinstance(app.screen, Session)
    return app.screen


def start_session(app: App, config: Config) -> Session:
    """Choose a Config in the Menu and press Start."""
    menu = menu_of(app)
    menu.choose(config)
    app.tick(FRAME)
    press(pygame.K_RETURN)
    assert app.tick(FRAME)
    return session_of(app)


def run_until_finished(app: App) -> int:
    """Press SPACE and tick until the Prompt appears. Returns the frames it took."""
    press(pygame.K_SPACE)
    for frame in range(1, MAX_FRAMES):
        assert app.tick(FRAME)
        if session_of(app).finished:
            return frame
    raise AssertionError("the Search never finished")


def draw_open_board(size: int) -> None:
    click_node(size, 0, 0)
    click_node(size, size - 1, size - 1)


def test_opens_on_the_menu_preselected_from_the_command_line(make_app: type[App]):
    app = make_app(Options("DFS", 12, False))
    assert menu_of(app).config == Config(12, "DFS", Speed.NORMAL)


def test_menu_defaults_when_nothing_is_preselected(make_app: type[App]):
    app = make_app(Options(None, None, False))
    assert menu_of(app).config == DEFAULT_CONFIG


def test_escape_in_the_menu_quits(make_app: type[App]):
    app = make_app(Options(None, None, False))
    press(pygame.K_ESCAPE)
    assert not app.tick(FRAME)


def test_closing_the_window_quits(make_app: type[App]):
    app = make_app(Options(None, None, False))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    assert not app.tick(FRAME)


@pytest.mark.parametrize("text", ["", "1", "201", "500", "1000"])
def test_invalid_board_size_does_not_start_a_session(make_app: type[App], text: str):
    app = make_app(Options(None, None, False))
    menu = menu_of(app)
    menu.enter_board_size(text)
    app.tick(FRAME)
    assert menu.config is None
    assert menu.error  # tells the user why

    press(pygame.K_RETURN)
    app.tick(FRAME)
    assert app.screen is menu


def test_a_valid_board_size_clears_the_error(make_app: type[App]):
    app = make_app(Options(None, None, False))
    menu = menu_of(app)
    menu.enter_board_size("500")
    app.tick(FRAME)
    menu.enter_board_size("40")
    app.tick(FRAME)
    assert menu.error == ""
    assert menu.config is not None
    assert menu.config.board_size == 40


def test_start_opens_a_session_with_the_chosen_config(make_app: type[App]):
    app = make_app(Options(None, None, False))
    config = Config(8, "AStar", Speed.FAST)
    session = start_session(app, config)
    assert session.config == config
    assert session.board.size == 8


def test_a_session_runs_one_search_and_then_shows_the_prompt(make_app: type[App]):
    app = make_app(Options(None, None, False))
    session = start_session(app, Config(6, "BFS", Speed.ULTRA))
    assert session.prompt is None
    draw_open_board(6)
    run_until_finished(app)
    assert session.prompt is not None


def test_prompt_is_also_shown_when_no_path_exists(make_app: type[App]):
    app = make_app(Options(None, None, False))
    session = start_session(app, Config(4, "BFS", Speed.ULTRA))
    draw_open_board(4)
    for y in range(4):  # a wall of Barriers between Start and End
        click_node(4, 1, y)
    run_until_finished(app)
    assert session.prompt is not None


def test_continue_starts_a_fresh_board_with_the_same_config(make_app: type[App]):
    app = make_app(Options(None, None, False))
    config = Config(6, "DFS", Speed.ULTRA)
    first = start_session(app, config)
    draw_open_board(6)
    run_until_finished(app)

    press(pygame.K_RETURN)
    app.tick(FRAME)
    second = session_of(app)
    assert second is not first
    assert second.config == config
    assert second.board.start is None
    assert second.prompt is None


def test_continue_button_starts_a_fresh_board(make_app: type[App]):
    app = make_app(Options(None, None, False))
    session = start_session(app, Config(6, "BFS", Speed.ULTRA))
    draw_open_board(6)
    run_until_finished(app)
    assert session.prompt is not None

    pygame.event.post(
        pygame.event.Event(pygame_gui.UI_BUTTON_PRESSED, ui_element=session.prompt.continue_button)
    )
    app.tick(FRAME)
    assert session_of(app) is not session


def test_new_config_returns_to_the_menu_with_the_last_config(make_app: type[App]):
    app = make_app(Options(None, None, False))
    config = Config(6, "AStar", Speed.ULTRA)
    session = start_session(app, config)
    draw_open_board(6)
    run_until_finished(app)
    assert session.prompt is not None

    pygame.event.post(
        pygame.event.Event(
            pygame_gui.UI_BUTTON_PRESSED, ui_element=session.prompt.new_config_button
        )
    )
    app.tick(FRAME)
    assert menu_of(app).config == config


def test_escape_abandons_a_session_and_returns_to_the_menu(make_app: type[App]):
    app = make_app(Options(None, None, False))
    config = Config(9, "DFS", Speed.SLOW)
    start_session(app, config)
    press(pygame.K_ESCAPE)
    assert app.tick(FRAME)
    assert menu_of(app).config == config


def test_escape_on_the_prompt_returns_to_the_menu(make_app: type[App]):
    app = make_app(Options(None, None, False))
    start_session(app, Config(6, "BFS", Speed.ULTRA))
    draw_open_board(6)
    run_until_finished(app)
    press(pygame.K_ESCAPE)
    assert app.tick(FRAME)
    assert isinstance(app.screen, Menu)


def test_tab_clears_the_board_within_the_same_session(make_app: type[App]):
    app = make_app(Options(None, None, False))
    session = start_session(app, Config(6, "BFS", Speed.NORMAL))
    draw_open_board(6)
    app.tick(FRAME)
    assert session.board.ready
    press(pygame.K_TAB)
    app.tick(FRAME)
    assert session_of(app) is session
    assert session.board.start is None


def test_space_and_tab_are_ignored_while_the_prompt_is_showing(make_app: type[App]):
    app = make_app(Options(None, None, False))
    session = start_session(app, Config(6, "BFS", Speed.ULTRA))
    draw_open_board(6)
    run_until_finished(app)

    press(pygame.K_SPACE)
    press(pygame.K_TAB)
    app.tick(FRAME)
    assert session_of(app) is session
    assert session.finished
    assert session.board.ready


def test_slower_speeds_take_more_frames_to_finish(make_app: type[App]):
    frames: dict[Speed, int] = {}
    for speed in (Speed.SLOW, Speed.NORMAL, Speed.ULTRA):
        app = make_app(Options(None, None, False))
        start_session(app, Config(5, "BFS", speed))
        draw_open_board(5)
        frames[speed] = run_until_finished(app)
        pygame.quit()
    assert frames[Speed.SLOW] > frames[Speed.NORMAL] > frames[Speed.ULTRA]
