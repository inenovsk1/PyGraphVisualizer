"""Pathfinding Algorithms, written as generators that yield Steps.

An Algorithm never draws or touches pygame (see ADR-0001): it reads the Board and
yields a ``Step`` each time it makes observable progress. The caller decides when and
how to render, and applies each Step to the Board with ``apply_step``.
"""

import heapq
from collections import deque
from collections.abc import Callable, Iterator
from dataclasses import dataclass

from pygraphvisualizer.board import Board, Node, State


@dataclass(frozen=True, slots=True)
class Step:
    """One increment of progress in a Search, reported between redraws.

    ``opened`` and ``closed`` are the Nodes that became Open or Closed since the
    previous Step. ``path`` is only set on the final Step of a successful Search: the
    Nodes strictly between Start and End, ordered from the End side back toward Start.
    """

    opened: tuple[Node, ...] = ()
    closed: tuple[Node, ...] = ()
    path: tuple[Node, ...] | None = None


Algorithm = Callable[[Board, Node, Node], Iterator[Step]]


def apply_step(board: Board, step: Step) -> None:
    """Paint the Board to reflect a Step."""
    for node in step.opened:
        board.mark(node, State.OPEN)
    for node in step.closed:
        board.mark(node, State.CLOSED)
    for node in step.path or ():
        board.mark(node, State.PATH)


def _path(came_from: dict[Node, Node], start: Node, end: Node) -> tuple[Node, ...]:
    path: list[Node] = []
    current = end
    while current in came_from:
        current = came_from[current]
        if current != start:
            path.append(current)
    return tuple(path)


def bfs(board: Board, start: Node, end: Node) -> Iterator[Step]:
    """Breadth First Search: expands Nodes in order of distance from Start."""
    seen = {start}
    came_from: dict[Node, Node] = {}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current == end:
            yield Step(path=_path(came_from, start, end))
            return

        opened: list[Node] = []
        for neighbor in board.neighbors(current):
            if neighbor not in seen:
                seen.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                opened.append(neighbor)

        yield Step(opened=tuple(opened), closed=(current,) if current != start else ())


def dfs(board: Board, start: Node, end: Node) -> Iterator[Step]:
    """Depth First Search: follows one branch as far as it goes, then backtracks.

    Open Nodes are the branch currently being followed; Nodes become Closed when the
    search backtracks out of them.
    """
    seen = {start}
    came_from: dict[Node, Node] = {}
    stack = [(start, iter(board.neighbors(start)))]

    while stack:
        current, neighbors = stack[-1]
        for neighbor in neighbors:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            came_from[neighbor] = current
            if neighbor == end:
                yield Step(path=_path(came_from, start, end))
                return
            yield Step(opened=(neighbor,))
            stack.append((neighbor, iter(board.neighbors(neighbor))))
            break
        else:
            stack.pop()
            if current != start:
                yield Step(closed=(current,))


def _heuristic(a: Node, b: Node) -> int:
    """Manhattan distance, which never overestimates on a 4-connected Board."""
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar(board: Board, start: Node, end: Node) -> Iterator[Step]:
    """A*: expands the Node with the lowest (distance so far + estimated distance left)."""
    came_from: dict[Node, Node] = {}
    g_score = {start: 0}
    order = 0
    heap = [(_heuristic(start, end), order, start)]
    closed: set[Node] = set()

    while heap:
        _, _, current = heapq.heappop(heap)
        if current in closed:
            continue
        if current == end:
            yield Step(path=_path(came_from, start, end))
            return
        closed.add(current)

        opened: list[Node] = []
        for neighbor in board.neighbors(current):
            tentative = g_score[current] + 1
            known = g_score.get(neighbor)
            if known is None or tentative < known:
                if known is None:
                    opened.append(neighbor)
                g_score[neighbor] = tentative
                came_from[neighbor] = current
                order += 1
                heapq.heappush(heap, (tentative + _heuristic(neighbor, end), order, neighbor))

        yield Step(opened=tuple(opened), closed=(current,) if current != start else ())


ALGORITHMS: dict[str, Algorithm] = {"BFS": bfs, "DFS": dfs, "AStar": astar}
