# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A pygame (v2) visualizer for grid pathfinding algorithms (BFS, DFS, A*). There is no build step, dependency manifest, test suite, or linter — just two Python files. Install `pygame` manually.

## Running

```
./main.py -a {BFS|DFS|AStar} -b <N> [-f]     # e.g. ./main.py -a AStar -b 50 -f
./main.py --help
```

`-a` and `-b` are required; `-f` is fullscreen (otherwise a 1280x720 window). The board is N×N. Controls: first click = start, second click = end, further click/drag = barriers, right-click = erase, SPACE = run, TAB = clear, ESC = quit.

Because it opens a GUI window, changes can only be verified by running the app interactively.

## Architecture

- `main.py` — `Color` enum (a node's state *is* its color; `Node.is_barrier()` etc. compare against it), `Node` class, drawing helpers, and `main()` with the event loop. The loop redraws every frame, handles mouse/keyboard, and on SPACE recomputes every node's neighbors and calls the selected algorithm **synchronously**.
- `graph_algo.py` — `BFS`, `DFS`, `AStar`, each with signature `(refresh_func, construct_path, grid, start_node, end_node)`. These run their own blocking loop: they mutate node colors (`make_open` / `make_closed`), call `refresh_func()` each step to render, and poll `pygame.event.get()` for `QUIT` so the window can still be closed mid-run.
- `refresh_func` and `construct_path` are `functools.partial`s built in `main()`'s SPACE handler, so the algorithms never touch pygame surfaces directly except for event polling. On success, an algorithm calls `construct_path(came_from)`, which colors the path and runs the circle animation in `animate_path`.

### Adding an algorithm

Add the function to `graph_algo.py` with the same signature, add its name to the `choices` list of the `-a` argument, and add an `elif` branch in the SPACE handler in `main()`.

## Gotchas

- Grid is indexed `grid[x][y]` (column-major: first index is the horizontal cell, `Node(row, col, ...)` stores `_xcoord=row`). `rows` and `cols` are both `board_size`, but node width/height are derived separately from screen width/height, so cells are rectangular on non-square displays.
- `Node.__eq__`/`__hash__` are based on grid coordinates only, so nodes work as dict/set keys (`came_from`, `visited`, `g_score`).
- Neighbors are recalculated only when SPACE is pressed (`update_neighbors`), and barriers are excluded from them there.
- The `-a` argument is declared as `'-a' '--algo'` with no comma (Python concatenates to `'-a--algo'`); `-a X` still works via argparse prefix matching, but `--algo` does not. Fix with a comma if touching it.
- `DFS` is recursive and uses a module-level `stop_recursion` flag plus `sys.setrecursionlimit(10000)`; large boards can still hit recursion limits.
- Running an algorithm a second time without pressing TAB leaves the previous open/closed/path colors on the grid.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues (inenovsk1/PyGraphVisualizer) via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
