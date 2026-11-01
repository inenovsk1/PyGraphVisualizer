import pytest

from pygraphvisualizer.cli import Options, parse_args
from pygraphvisualizer.config import DEFAULT_CONFIG, Config, Speed


def test_parses_short_options():
    assert parse_args(["-a", "AStar", "-b", "50", "-f"]) == Options("AStar", 50, True)


def test_parses_long_options():
    assert parse_args(["--algo", "BFS", "--board", "30"]) == Options("BFS", 30, False)


def test_fullscreen_defaults_to_off():
    assert not parse_args(["-a", "DFS", "-b", "10"]).fullscreen


def test_every_option_is_optional():
    assert parse_args([]) == Options(None, None, False)


def test_unknown_algorithm_is_rejected():
    with pytest.raises(SystemExit):
        parse_args(["-a", "Dijkstra", "-b", "10"])


@pytest.mark.parametrize("size", ["abc", "1", "0", "-5", "201", "3.5"])
def test_board_size_must_be_an_integer_in_range(size: str):
    with pytest.raises(SystemExit) as exc:
        parse_args(["-a", "BFS", "-b", size])
    assert exc.value.code == 2


@pytest.mark.parametrize("size", ["2", "200"])
def test_board_size_bounds_are_inclusive(size: str):
    assert parse_args(["-a", "BFS", "-b", size]).board_size == int(size)


def test_initial_config_uses_the_defaults_when_nothing_is_given():
    assert parse_args([]).initial_config() == DEFAULT_CONFIG


def test_initial_config_preselects_what_was_given():
    options = parse_args(["-a", "DFS"])
    assert options.initial_config() == Config(DEFAULT_CONFIG.board_size, "DFS", Speed.NORMAL)

    options = parse_args(["-b", "75"])
    assert options.initial_config() == Config(75, DEFAULT_CONFIG.algo, Speed.NORMAL)
