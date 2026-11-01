import itertools

import pytest

from pygraphvisualizer.algorithms import ALGORITHMS, Step, apply_step
from pygraphvisualizer.board import Board, Node, State
from tests.conftest import make_board


def search(name: str, board: Board) -> list[Step]:
    assert board.start is not None and board.end is not None
    return list(ALGORITHMS[name](board, board.start, board.end))


def found_path(steps: list[Step]) -> tuple[Node, ...] | None:
    return steps[-1].path if steps else None


def assert_valid_path(board: Board, path: tuple[Node, ...]) -> None:
    """The path leads from Start to End through adjacent, non-Barrier Nodes."""
    assert board.start is not None and board.end is not None
    # path runs from the End side back toward Start, excluding both ends
    chain = [board.end, *path, board.start]
    for a, b in itertools.pairwise(chain):
        assert b in board.neighbors(a), f"{a} -> {b} is not a legal move"


ALL = list(ALGORITHMS)
SHORTEST = ["BFS", "AStar"]

DETOUR = (
    "S.#..",
    "..#..",
    "..#..",
    "..#..",
    "....E",
)


@pytest.mark.parametrize("name", ALL)
def test_finds_a_path_in_an_open_board(name: str):
    board = make_board("S...", "....", "....", "...E")
    path = found_path(search(name, board))
    assert path is not None
    assert_valid_path(board, path)


@pytest.mark.parametrize("name", ALL)
def test_reports_no_path_when_end_is_walled_off(name: str):
    board = make_board("S...", "....", "..##", "..#E")
    assert found_path(search(name, board)) is None


@pytest.mark.parametrize("name", ALL)
def test_adjacent_start_and_end_give_an_empty_path(name: str):
    board = make_board("SE", "..")
    assert found_path(search(name, board)) == ()


@pytest.mark.parametrize("name", ALL)
def test_path_goes_around_barriers(name: str):
    board = make_board(*DETOUR)
    path = found_path(search(name, board))
    assert path is not None
    assert_valid_path(board, path)
    assert not any(board.state(node) is State.BARRIER for node in path)


@pytest.mark.parametrize("name", SHORTEST)
def test_shortest_path_is_found_around_a_wall(name: str):
    board = make_board(*DETOUR)
    path = found_path(search(name, board))
    assert path is not None
    # the wall forces 4 moves down and 4 right: 8 moves, so 7 Nodes strictly between
    assert len(path) == 7


@pytest.mark.parametrize("name", SHORTEST)
def test_shortest_path_in_open_board_is_straight(name: str):
    board = make_board("S...E", ".....", ".....", ".....", ".....")
    path = found_path(search(name, board))
    assert path is not None
    assert len(path) == 3


def test_dfs_backtracks_out_of_a_dead_end():
    # DFS tries the Start's right neighbor first, which leads into a dead-end pocket
    board = make_board(
        "S..#",
        ".#.#",
        ".###",
        "...E",
    )
    path = found_path(search("DFS", board))
    assert path is not None
    assert_valid_path(board, path)


@pytest.mark.parametrize("name", ALL)
def test_path_is_the_final_step_and_only_once(name: str):
    board = make_board("S...", "....", "....", "...E")
    steps = search(name, board)
    assert steps[-1].path is not None
    assert all(step.path is None for step in steps[:-1])


@pytest.mark.parametrize("name", ALL)
def test_a_search_never_reports_barriers_or_start_as_closed(name: str):
    board = make_board("S.#.", "..#.", "..#.", "...E")
    steps = search(name, board)
    reported = {node for step in steps for node in (*step.opened, *step.closed)}
    assert not any(board.state(node) is State.BARRIER for node in reported)
    assert board.start not in {node for step in steps for node in step.closed}


@pytest.mark.parametrize("name", ALL)
def test_applying_all_steps_paints_the_path_and_keeps_start_and_end(name: str):
    board = make_board("S...", "..#.", "..#.", "...E")
    steps = search(name, board)
    for step in steps:
        apply_step(board, step)
    path = found_path(steps)
    assert path is not None
    assert all(board.state(node) is State.PATH for node in path)
    assert board.state(Node(0, 0)) is State.START
    assert board.state(Node(3, 3)) is State.END
    assert board.state(Node(2, 1)) is State.BARRIER


def test_rerunning_after_clearing_leaves_no_stale_states():
    board = make_board("S...", "....", "....", "...E")
    for step in search("BFS", board):
        apply_step(board, step)
    board.clear_search()
    assert all(
        board.state(node) in {State.EMPTY, State.START, State.END, State.BARRIER}
        for node in board.nodes()
    )
