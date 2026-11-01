from pygraphvisualizer.board import Board, Node, State


def test_new_board_is_all_empty():
    board = Board(3)
    assert all(board.state(node) is State.EMPTY for node in board.nodes())
    assert len(list(board.nodes())) == 9


def test_interior_node_has_four_neighbors():
    board = Board(3)
    assert set(board.neighbors(Node(1, 1))) == {Node(0, 1), Node(2, 1), Node(1, 0), Node(1, 2)}


def test_corner_node_has_two_neighbors():
    board = Board(3)
    assert set(board.neighbors(Node(0, 0))) == {Node(1, 0), Node(0, 1)}
    assert set(board.neighbors(Node(2, 2))) == {Node(1, 2), Node(2, 1)}


def test_barriers_are_not_neighbors():
    board = Board(3)
    board.place(Node(0, 0))  # start
    board.place(Node(2, 2))  # end
    board.place(Node(1, 0))  # barrier
    assert board.neighbors(Node(0, 0)) == [Node(0, 1)]


def test_first_click_is_start_second_is_end_then_barriers():
    board = Board(4)
    board.place(Node(0, 0))
    assert board.start == Node(0, 0)
    assert board.end is None
    board.place(Node(3, 3))
    assert board.end == Node(3, 3)
    assert board.ready
    board.place(Node(1, 1))
    assert board.state(Node(0, 0)) is State.START
    assert board.state(Node(3, 3)) is State.END
    assert board.state(Node(1, 1)) is State.BARRIER


def test_barrier_cannot_overwrite_start_or_end():
    board = Board(4)
    board.place(Node(0, 0))
    board.place(Node(3, 3))
    board.place(Node(0, 0))
    board.place(Node(3, 3))
    assert board.state(Node(0, 0)) is State.START
    assert board.state(Node(3, 3)) is State.END


def test_end_cannot_be_placed_on_start():
    board = Board(4)
    board.place(Node(1, 1))
    board.place(Node(1, 1))
    assert board.end is None
    assert board.state(Node(1, 1)) is State.START


def test_erase_start_allows_placing_it_again():
    board = Board(4)
    board.place(Node(0, 0))
    board.place(Node(3, 3))
    board.erase(Node(0, 0))
    assert board.start is None
    assert not board.ready
    board.place(Node(2, 2))
    assert board.start == Node(2, 2)


def test_clear_search_keeps_start_end_and_barriers():
    board = Board(4)
    board.place(Node(0, 0))
    board.place(Node(3, 3))
    board.place(Node(1, 1))
    board.mark(Node(0, 1), State.OPEN)
    board.mark(Node(0, 2), State.CLOSED)
    board.mark(Node(0, 3), State.PATH)
    board.clear_search()
    assert board.state(Node(0, 1)) is State.EMPTY
    assert board.state(Node(0, 2)) is State.EMPTY
    assert board.state(Node(0, 3)) is State.EMPTY
    assert board.state(Node(0, 0)) is State.START
    assert board.state(Node(3, 3)) is State.END
    assert board.state(Node(1, 1)) is State.BARRIER


def test_mark_never_overwrites_start_end_or_barrier():
    board = Board(4)
    board.place(Node(0, 0))
    board.place(Node(3, 3))
    board.place(Node(1, 1))
    for node in (Node(0, 0), Node(3, 3), Node(1, 1)):
        board.mark(node, State.CLOSED)
    assert board.state(Node(0, 0)) is State.START
    assert board.state(Node(3, 3)) is State.END
    assert board.state(Node(1, 1)) is State.BARRIER


def test_contains_rejects_out_of_range_nodes():
    board = Board(3)
    assert Node(2, 2) in board
    assert Node(3, 0) not in board
    assert Node(-1, 0) not in board
