from pygraphvisualizer.board import Board, Node


def make_board(*rows: str) -> Board:
    """Build a Board from ASCII art: S start, E end, # barrier, . empty.

    Row index is ``y`` and column index is ``x``.
    """
    board = Board(len(rows))
    assert all(len(row) == len(rows) for row in rows), "board must be square"
    cells: dict[str, list[Node]] = {char: [] for char in "SE#."}
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            cells[char].append(Node(x, y))
    board.place(cells["S"][0])
    board.place(cells["E"][0])
    for node in cells["#"]:
        board.place(node)
    return board
