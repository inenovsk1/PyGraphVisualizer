# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A pygame-ce visualizer for grid pathfinding algorithms (BFS, DFS, A*). Its window shows a Menu (choose a Config), then a Session (one Board, one Search), then a Prompt (continue or new Config). A uv-managed Python package (`src/pygraphvisualizer/`) with a pytest suite, Ruff and Pyright. Python >=3.12, developed on 3.14. Vocabulary is in `GLOSSARY.md`; use those terms (Board, Node, State, Search, Step, Config, Speed, Menu, Session, Prompt), not grid/graph/visited.

## Commands

```
uv sync                                              # install
uv run pygraphvisualizer [-a {BFS|DFS|AStar}] [-b <N>] [-f]   # run; also python -m pygraphvisualizer
uv run pytest                                        # tests (headless)
uv run pytest tests/test_algorithms.py               # single file
uv run ruff check . && uv run ruff format .          # lint + format
uv run pyright                                       # type check (strict)
```

`-a` and `-b` are optional and only preselect the Menu (`-b` is 2-200); `-f` is fullscreen, otherwise a 1280x720 window. Controls in a Session: first click = Start, second = End, further click/drag = Barriers, right-click = erase, SPACE = run, TAB = clear, ESC = back to the Menu. ESC in the Menu quits; ENTER = Start (Menu) or Continue (Prompt).

The look of the GUI can't be tested, but its behavior can: `tests/test_app.py` sets `SDL_VIDEODRIVER=dummy`, builds an `App`, posts pygame events and calls `App.tick`. Anything visual still needs a human running the app (or `pygame.image.save` on the display surface to look at a frame).

## Architecture

- `board.py` - `State` enum, `Node` (an `(x, y)` NamedTuple) and `Board`, which owns every Node's State plus Start/End. No pygame.
- `algorithms.py` - `bfs`, `dfs`, `astar` as generators with signature `(board, start, end) -> Iterator[Step]`, plus `Step`, `apply_step` and the `ALGORITHMS` registry. No pygame (ADR-0001): they read the Board and yield Steps; they never draw or poll events. The final Step of a successful Search carries the `path`.
- `config.py` - `Config` (Board size, Algorithm, `Speed`), the `Speed` levels and `parse_board_size` (the 2-200 limits). No pygame.
- `cli.py` - argparse and `Options`; `Options.initial_config()` is what the first Menu shows.
- `theme.py` - State -> color map.
- `view.py` - `BoardView` (pixels <-> Nodes, drawing; the caller flips the display) and `PathAnimation`.
- `screen.py` - the `Screen` protocol (`handle_event`, `update`, `draw`) and the `Transition`s a Screen returns: `StartSession(config)`, `OpenMenu`, `Quit`.
- `menu.py` - `Menu` screen built with `pygame_gui` (ADR-0002): Board size entry, Algorithm and Speed dropdowns, Start.
- `session.py` - `Session` screen: owns the Board, runs one Search at the Config's Speed, then the Path animation, then shows the `Prompt` (`prompt.py`).
- `app.py` - `App`: the one window and the main loop. `tick(dt)` feeds events to the current Screen, switches Screens on a Transition, updates and draws. This is the only module with an event loop.

### Adding an algorithm

Write a generator `(board, start, end) -> Iterator[Step]` in `algorithms.py` and add it to `ALGORITHMS`; the `-a` choices come from that dict. Test it by adding it to the parametrized lists in `tests/test_algorithms.py`.

## Gotchas

- `Node(x, y)`: `x` is the column and `y` the row. Cells are rectangular on non-square displays because width and height are divided separately.
- `Board.neighbors` returns Nodes in the order +x, -x, +y, -y and excludes Barriers. Neighbors are computed on demand.
- `Board.mark` only paints Search states and never overwrites Start, End or Barrier. `Board.clear_search` removes Open/Closed/Path; it runs before every Search, so re-running without TAB is fine.
- `Step.path` lists the Nodes strictly between Start and End, ordered from the End side. An empty tuple means adjacent Start and End; `None` means no path found.
- The path is not painted by `apply_step` in the app: `PathAnimation` reveals it one Node at a time and marks each Node as Path when its circle fills the cell.
- Speed is Steps consumed per frame (a fraction means a Step every few frames) and Path animation pixels per frame; Ultra is 2x xFast. A Session fixes its Config, so Speed never changes mid-Search.
- A Session is exactly one Search. When it ends (Path found or not) the Prompt appears over the Board: Continue starts a new Session with the same Config on an empty Board, New config opens the Menu. The Menu always opens with the last Config used.
- Editing and SPACE are ignored while a Search or Path animation is running, and SPACE/TAB are ignored while the Prompt shows; otherwise TAB resets the Board within the same Session. ESC in a Session or Prompt goes to the Menu; ESC in the Menu quits.
- `pygame_gui` text entry restricts typing to digits, but the Board size is still validated with `parse_board_size`; Start stays disabled and a message is shown until it is allowed. Nothing is clamped.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues (inenovsk1/PyGraphVisualizer) via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
