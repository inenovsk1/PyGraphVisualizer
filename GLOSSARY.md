# PyGraphVisualizer

An interactive visualizer that shows pathfinding algorithms exploring a square Board, so a person can watch how each one searches from a Start to an End.

## Language

**Board**:
The square N×N field of Nodes the user draws on and the Algorithm searches. The Config's size sets N.
_Avoid_: Grid, graph, map

**Node**:
A single square on the Board. Each Node is adjacent to its up/down/left/right neighbors, except those that are Barriers.
_Avoid_: Cell, tile, square, vertex

**State**:
What a Node currently is: *Empty*, *Start*, *End*, *Barrier*, *Open*, *Closed* or *Path*. A State is distinct from the color used to show it.
_Avoid_: Color (as a synonym for state), type

**Start**:
The State of the single Node a Search begins from. Placed by the first click.
_Avoid_: Begin, source, origin

**End**:
The State of the single Node a Search tries to reach. Placed by the second click.
_Avoid_: Goal, target, destination

**Barrier**:
The State of a Node that cannot be entered. Drawn by clicking or dragging after Start and End are placed.
_Avoid_: Wall, obstacle, blocked

**Open**:
The State of a Node a Search has discovered but not yet finished examining.
_Avoid_: Frontier, queued

**Closed**:
The State of a Node a Search has finished examining.
_Avoid_: Visited (this term also covers Open Nodes, so it is ambiguous)

**Path**:
The chain of Nodes from Start to End that a successful Search found, shown in the Path State.
_Avoid_: Route, solution

## Searching

**Algorithm**:
A named pathfinding strategy the user selects in the Menu as part of a Config: BFS, DFS or A*.
_Avoid_: Solver, strategy

**Search**:
One run of an Algorithm on the Board from Start to End. It ends with either a Path or no Path.
_Avoid_: Run, execution, traversal

**Step**:
One increment of progress a Search reports between redraws: the Nodes that became Open or Closed since the last Step, or the finished Path.
_Avoid_: Tick, event, move

## Sessions

**Config**:
The combination of Board size, Algorithm and Speed the user chooses in the Menu. It stays fixed for the Sessions that follow until the user chooses a new one.
_Avoid_: Settings, options, setup

**Speed**:
How fast a Search and its Path are shown, chosen as one of the named levels Slow, Normal, Fast, xFast or Ultra. It is part of the Config and does not change mid-Session.
_Avoid_: Rate, delay, FPS

**Menu**:
The screen where the user chooses a Config before a Session. It opens with the most recently chosen Config already filled in.
_Avoid_: Launcher, settings screen

**Prompt**:
The panel shown over the finished Board when a Session ends, offering to continue with the same Config or to choose a new one in the Menu.
_Avoid_: Dialog, popup, end screen

**Session**:
One Board drawn with one Config, lasting for exactly one Search and its Path animation. It ends with the Prompt, or earlier if the user abandons it. Continuing with the same Config starts a new Session on a fresh, empty Board.
_Avoid_: Game, round, run
