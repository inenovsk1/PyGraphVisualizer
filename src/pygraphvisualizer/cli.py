"""Command line interface."""

import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from pygraphvisualizer.algorithms import ALGORITHMS

MIN_BOARD_SIZE = 2
MAX_BOARD_SIZE = 200

DESCRIPTION = """Python Graph Visualizer written with pygame
Usage instructions:
1. Click once anywhere on the board to mark the Start node.
2. Click a second time somewhere on the board to mark the End node.
3. Click, hold, and drag to create Barriers. Right-click to erase.
4. Press SPACE for the algorithm to start.
5. Press TAB to clear the board so 1-4 can be performed again.
6. Press ESCAPE or your OS's program shutdown combination to close."""


@dataclass(frozen=True, slots=True)
class Options:
    algo: str
    board_size: int
    fullscreen: bool


def _board_size(value: str) -> int:
    try:
        size = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from None
    if not MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE:
        raise argparse.ArgumentTypeError(
            f"must be between {MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}, got {size}"
        )
    return size


def parse_args(argv: Sequence[str] | None = None) -> Options:
    parser = argparse.ArgumentParser(
        prog="pygraphvisualizer",
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-f", "--fullscreen", action="store_true", help="Fullscreen mode vs. Windowed mode"
    )
    parser.add_argument(
        "-a",
        "--algo",
        choices=list(ALGORITHMS),
        required=True,
        help="Algorithm to visualize",
    )
    parser.add_argument(
        "-b",
        "--board",
        dest="board_size",
        type=_board_size,
        required=True,
        help="Size of the board - if 30, then the board is 30x30",
    )
    args = parser.parse_args(argv)
    return Options(args.algo, args.board_size, args.fullscreen)
