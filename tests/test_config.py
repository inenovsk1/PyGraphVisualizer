import pytest

from pygraphvisualizer.config import (
    DEFAULT_CONFIG,
    MAX_BOARD_SIZE,
    MIN_BOARD_SIZE,
    Speed,
    parse_board_size,
)


def test_speed_levels_are_ordered_slowest_to_fastest():
    assert [speed.label for speed in Speed] == ["Slow", "Normal", "Fast", "xFast", "Ultra"]
    steps = [speed.steps_per_frame for speed in Speed]
    pixels = [speed.path_pixels_per_frame for speed in Speed]
    assert steps == sorted(steps)
    assert pixels == sorted(pixels)


def test_normal_speed_is_one_step_per_frame():
    assert Speed.NORMAL.steps_per_frame == 1
    assert Speed.NORMAL.path_pixels_per_frame == 1


def test_ultra_runs_at_twice_the_rate_of_xfast():
    assert Speed.ULTRA.steps_per_frame == 2 * Speed.XFAST.steps_per_frame
    assert Speed.ULTRA.path_pixels_per_frame == 2 * Speed.XFAST.path_pixels_per_frame


def test_default_config():
    assert (DEFAULT_CONFIG.board_size, DEFAULT_CONFIG.algo, DEFAULT_CONFIG.speed) == (
        30,
        "BFS",
        Speed.NORMAL,
    )


@pytest.mark.parametrize("text", ["2", "30", "200", " 15 "])
def test_valid_board_sizes_are_accepted(text: str):
    assert parse_board_size(text) == int(text)


@pytest.mark.parametrize("text", ["1", "0", "-5", "201", "5000"])
def test_out_of_range_board_size_is_rejected_with_the_allowed_range(text: str):
    with pytest.raises(ValueError, match=rf"{MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}"):
        parse_board_size(text)


@pytest.mark.parametrize("text", ["", " ", "abc", "3.5", "1e2"])
def test_non_integer_board_size_is_rejected(text: str):
    with pytest.raises(ValueError, match="not an integer"):
        parse_board_size(text)
