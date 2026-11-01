# PyGraphVisualizer

A [pygame](https://pyga.me) visualizer for grid pathfinding algorithms: Breadth First Search, Depth First Search and A*.

## Setup

Requires [uv](https://docs.astral.sh/uv/) (it installs Python and the dependencies for you).

```
uv sync
```

## Usage

```
uv run pygraphvisualizer [-a {BFS|DFS|AStar}] [-b <size>] [-f]
uv run pygraphvisualizer --help
```

`python -m pygraphvisualizer ...` works too. The Menu opens first, where you choose the board size (2 to 200), the algorithm and the speed (Slow, Normal, Fast, xFast, Ultra), then press Start. `-a` and `-b` only preselect the Menu's algorithm and board size; `-f` runs fullscreen instead of in a 1280x720 window.

Each Start opens a board for one run of the chosen algorithm. When it finishes, a prompt offers to continue with the same Config on a fresh board, or to go back to the Menu and pick new ones.

### Examples

Fullscreen, with the Menu preselecting A* on a 50x50 board:

```
uv run pygraphvisualizer -f -a AStar -b 50
```

Windowed, with the Menu preselecting Breadth First Search on a 30x30 board:

```
uv run pygraphvisualizer -a BFS -b 30
```

### Controls

| Input | Action |
|---|---|
| First click | Place the Start node |
| Second click | Place the End node |
| Click or drag | Draw barriers |
| Right-click | Erase |
| `SPACE` | Run the algorithm |
| `TAB` | Clear the board |
| `ENTER` | Menu: Start. Prompt: Continue |
| `ESC` | On a board or the prompt: back to the Menu. In the Menu: quit |

## Development

```
uv run pytest            # tests (headless, no display needed)
uv run ruff check .      # lint
uv run ruff format .     # format
uv run pyright           # type check
```

See [GLOSSARY.md](GLOSSARY.md) for the project's vocabulary and [docs/adr](docs/adr) for design decisions.

## Caveats

The larger the board, the longer a search takes. At Normal speed the app runs at 60 FPS with one step per frame, so a board of 30 to 60 works well; pick a faster speed for bigger boards.

## License

BSD 3-Clause. See [LICENSE](LICENSE).
