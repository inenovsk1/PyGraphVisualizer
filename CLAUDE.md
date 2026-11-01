# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A pygame-ce visualizer for grid pathfinding algorithms (BFS, DFS, A*). A uv-managed Python package (`src/pygraphvisualizer/`) with a pytest suite, Ruff and Pyright. Python >=3.12, developed on 3.14. Vocabulary is in `GLOSSARY.md`; use those terms (Board, Node, State, Search, Step), not grid/graph/visited.

## Commands

```
uv sync                                              # install
uv run pygraphvisualizer -a {BFS|DFS|AStar} -b <N> [-f]   # run; also python -m pygraphvisualizer
uv run pytest                                        # tests (headless)
uv run pytest tests/test_algorithms.py               # single file
uv run ruff check . && uv run ruff format .          # lint + format
uv run pyright                                       # type check (strict)
```

`-a` and `-b` are required (`-b` is 2-200); `-f` is fullscreen, otherwise a 1280x720 window. Controls: first click = Start, second = End, further click/drag = Barriers, right-click = erase, SPACE = run, TAB = clear, ESC = quit.

The GUI can't be exercised by tests. To smoke-test headlessly, set `SDL_VIDEODRIVER=dummy`, build an `App`, post pygame events and call its `_handle_events`/`_advance`/`_view.draw`. Anything visual still needs a human running the app.

## Architecture

- `board.py` - `State` enum, `Node` (an `(x, y)` NamedTuple) and `Board`, which owns every Node's State plus Start/End. No pygame.
- `algorithms.py` - `bfs`, `dfs`, `astar` as generators with signature `(board, start, end) -> Iterator[Step]`, plus `Step`, `apply_step` and the `ALGORITHMS` registry. No pygame (ADR-0001): they read the Board and yield Steps; they never draw or poll events. The final Step of a successful Search carries the `path`.
- `cli.py` - argparse and `Options`; board size validation.
- `theme.py` - State -> color map.
- `view.py` - `BoardView` (pixels <-> Nodes, drawing) and `PathAnimation`.
- `app.py` - `App`: window, input, and the main loop. Each frame it handles events, advances the running Search by one Step (or the Path animation), and redraws. This is the only module with an event loop.

### Adding an algorithm

Write a generator `(board, start, end) -> Iterator[Step]` in `algorithms.py` and add it to `ALGORITHMS`; the `-a` choices come from that dict. Test it by adding it to the parametrized lists in `tests/test_algorithms.py`.

## Gotchas

- `Node(x, y)`: `x` is the column and `y` the row. Cells are rectangular on non-square displays because width and height are divided separately.
- `Board.neighbors` returns Nodes in the order +x, -x, +y, -y and excludes Barriers. Neighbors are computed on demand.
- `Board.mark` only paints Search states and never overwrites Start, End or Barrier. `Board.clear_search` removes Open/Closed/Path; it runs before every Search, so re-running without TAB is fine.
- `Step.path` lists the Nodes strictly between Start and End, ordered from the End side. An empty tuple means adjacent Start and End; `None` means no path found.
- The path is not painted by `apply_step` in the app: `PathAnimation` reveals it one Node at a time and marks each Node as Path when its circle fills the cell.
- Editing and SPACE are ignored while a Search or Path animation is running; TAB always resets.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues (inenovsk1/PyGraphVisualizer) via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
