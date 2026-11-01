# PyGraphVisualizer

A [pygame](https://pyga.me) visualizer for grid pathfinding algorithms: Breadth First Search, Depth First Search and A*.

## Setup

Requires [uv](https://docs.astral.sh/uv/) (it installs Python and the dependencies for you).

```
uv sync
```

## Usage

```
uv run pygraphvisualizer -a {BFS|DFS|AStar} -b <size> [-f]
uv run pygraphvisualizer --help
```

`python -m pygraphvisualizer ...` works too. `-a` and `-b` are required; `-f` runs fullscreen instead of in a 1280x720 window. The board is `size` x `size`, with a size from 2 to 200.

### Examples

Fullscreen A* on a 50x50 board:

```
uv run pygraphvisualizer -f -a AStar -b 50
```

Breadth First Search in a window on a 30x30 board:

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
| `ESC` | Quit |

## Development

```
uv run pytest            # tests (headless, no display needed)
uv run ruff check .      # lint
uv run ruff format .     # format
uv run pyright           # type check
```

See [GLOSSARY.md](GLOSSARY.md) for the project's vocabulary and [docs/adr](docs/adr) for design decisions.

## Caveats

The larger the board, the longer a search takes, and the app runs at 60 FPS with one step per frame. A board of 30 to 60 works well.

## License

BSD 3-Clause. See [LICENSE](LICENSE).
