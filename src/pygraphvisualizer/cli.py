"""Command line interface."""

import argparse
from collections.abc import Sequence
from dataclasses import dataclass, replace

from pygraphvisualizer.algorithms import ALGORITHMS
from pygraphvisualizer.config import DEFAULT_CONFIG, Config, parse_board_size

DESCRIPTION = """Python Graph Visualizer written with pygame
The Menu opens first: choose the Board size, Algorithm and Speed, then press Start.
-a and -b only preselect the Menu's Algorithm and Board size.

In a Session:
1. Click once anywhere on the board to mark the Start node.
2. Click a second time somewhere on the board to mark the End node.
3. Click, hold, and drag to create Barriers. Right-click to erase.
4. Press SPACE for the algorithm to start. When it finishes, choose to continue with
   the same Config or to go back to the Menu.
5. Press TAB to clear the board so 1-4 can be performed again.
6. Press ESCAPE to return to the Menu (from the Menu it closes the program)."""


@dataclass(frozen=True, slots=True)
class Options:
    algo: str | None
    board_size: int | None
    fullscreen: bool

    def initial_config(self) -> Config:
        """The Config the Menu starts with: the defaults, overridden by what was given."""
        config = DEFAULT_CONFIG
        if self.algo is not None:
            config = replace(config, algo=self.algo)
        if self.board_size is not None:
            config = replace(config, board_size=self.board_size)
        return config


def _board_size(value: str) -> int:
    try:
        return parse_board_size(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from None


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
        help="Algorithm preselected in the Menu",
    )
    parser.add_argument(
        "-b",
        "--board",
        dest="board_size",
        type=_board_size,
        help="Board size preselected in the Menu - if 30, then the board is 30x30",
    )
    args = parser.parse_args(argv)
    return Options(args.algo, args.board_size, args.fullscreen)
