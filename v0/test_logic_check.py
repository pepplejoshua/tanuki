from logic_check import is_valid_pawn_move, is_valid_knight_move
from utils import parse_move


def test_pawn_moves():
    # Test board with some specific positions
    test_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],  # 8
        [".", ".", ".", ".", ".", ".", ".", "."],  # 7
        [".", ".", ".", ".", ".", ".", ".", "."],  # 6
        [".", ".", ".", "♟", ".", ".", ".", "♟"],  # 5
        [".", ".", ".", ".", "♙", ".", ".", "♙"],  # 4
        [".", ".", ".", ".", ".", ".", ".", "."],  # 3
        ["♙", "♙", "♙", "♙", ".", "♙", "♙", "."],  # 2
        [".", ".", ".", ".", ".", ".", ".", "."],  # 1
    ]  #  a    b    c    d    e    f    g    h

    # Test cases for white pawn at e4
    start, end = parse_move("e4d5")
    assert is_valid_pawn_move(test_board, start, end, True)  # Capture black pawn at d5

    start, end = parse_move("e4e6")
    assert not is_valid_pawn_move(
        test_board, start, end, True
    )  # Can't move 2 squares (not first move)

    start, end = parse_move("e4e5")
    assert is_valid_pawn_move(test_board, start, end, True)  # Can move 1 square forward

    start, end = parse_move("e4e3")
    assert not is_valid_pawn_move(test_board, start, end, True)  # Can't move backwards

    # Test cases for white pawn at starting position a2
    start, end = parse_move("a2a4")
    assert is_valid_pawn_move(
        test_board, start, end, True
    )  # Can move 2 squares on first move

    start, end = parse_move("a2a3")
    assert is_valid_pawn_move(
        test_board, start, end, True
    )  # Can move 1 square on first move

    # Can't move white pawn at h4 to h5
    # since there is a black pawn (no capture)
    start, end = parse_move("h4h5")
    assert not is_valid_pawn_move(test_board, start, end, True)


def test_knight_moves():
    # Test board with various scenarios
    test_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],  # 8
        [".", ".", ".", ".", ".", ".", ".", "."],  # 7
        [".", ".", "♟", ".", "♟", ".", ".", "."],  # 6
        [".", "♟", ".", ".", ".", "♟", ".", "."],  # 5
        [".", ".", ".", "♘", ".", ".", ".", "."],  # 4
        [".", "♟", ".", ".", "♙", "♟", ".", "."],  # 3
        [".", ".", "♟", ".", "♟", ".", ".", "."],  # 2
        [".", ".", ".", ".", ".", ".", ".", "."],  # 1
    ]  #  a    b    c    d    e    f    g    h

    # White knight at d4 can take black pieces (showing all valid moves)
    start, end = parse_move("d4c6")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4e6")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4c2")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4e2")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4b5")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4b3")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4f5")
    assert is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4f3")
    assert is_valid_knight_move(test_board, start, end, True)

    # White knight at d4 performing invalid moves
    start, end = parse_move("d4c5")
    assert not is_valid_knight_move(test_board, start, end, True)

    start, end = parse_move("d4e3")
    assert not is_valid_knight_move(test_board, start, end, True)


test_pawn_moves()
test_knight_moves()
