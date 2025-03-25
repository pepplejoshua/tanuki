from logic_check import is_valid_pawn_move, is_valid_knight_move, is_valid_bishop_move
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


def test_bishop_moves():
    # Test board with various scenarios:
    test_board = [
        [".", ".", ".", ".", ".", ".", ".", "."],  # 8
        [".", ".", ".", "♟", ".", ".", ".", "."],  # 7
        [".", ".", ".", ".", ".", ".", ".", "."],  # 6
        [".", ".", ".", "♗", ".", ".", ".", "."],  # 5
        [".", ".", ".", ".", "♙", ".", ".", "."],  # 4
        [".", ".", ".", ".", ".", ".", ".", "."],  # 3
        [".", ".", ".", ".", ".", ".", ".", "."],  # 2
        [".", ".", ".", ".", ".", ".", ".", "."],  # 1
    ]  #  a    b    c    d    e    f    g    h
    # White bishop at d5 can move:
    # - Northwest (c6, b7, a8)
    # - Northeast (e6, f7, g8)
    # - Southwest (c4, b3, a2)
    # - Southeast (e4 blocked by white pawn)
    # Cannot capture black pawn at d7 (not a diagonal move)

    # Valid moves
    start, end = parse_move("d5c6")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5b7")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5a8")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square

    start, end = parse_move("d5e6")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5f7")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5g8")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square

    start, end = parse_move("d5c4")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5b3")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5a2")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square

    start, end = parse_move("d5f7")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square
    start, end = parse_move("d5g8")
    assert is_valid_bishop_move(test_board, start, end, True)  # Empty square

    # Invalid moves
    start, end = parse_move("d5d7")
    assert not is_valid_bishop_move(test_board, start, end, True)  # Non-diagonal

    start, end = parse_move("d5e4")
    assert not is_valid_bishop_move(
        test_board, start, end, True
    )  # Blocked by own piece

    start, end = parse_move("d5f3")
    assert not is_valid_bishop_move(
        test_board, start, end, True
    )  # Diagonal but blocked by own piece

    # Test board edges
    test_board_2 = [
        [".", ".", ".", ".", ".", ".", ".", "."],  # 8
        [".", ".", ".", ".", ".", ".", ".", "."],  # 7
        [".", ".", ".", ".", ".", ".", ".", "."],  # 6
        [".", ".", ".", ".", ".", ".", ".", "."],  # 5
        [".", ".", ".", ".", ".", ".", ".", "."],  # 4
        [".", ".", ".", ".", ".", ".", ".", "."],  # 3
        [".", ".", ".", ".", ".", ".", ".", "♗"],  # 2
        [".", ".", ".", ".", ".", ".", ".", "."],  # 1
    ]  #  a    b    c    d    e    f    g    h
    # White bishop in corner at h2

    # Valid moves from corner
    start, end = parse_move("h2g3")
    assert is_valid_bishop_move(test_board_2, start, end, True)

    start, end = parse_move("h2g1")
    assert is_valid_bishop_move(test_board_2, start, end, True)

    start, end = parse_move("h2b8")
    assert is_valid_bishop_move(test_board_2, start, end, True)

    # Invalid moves from corner
    start, end = parse_move("h2h3")
    assert not is_valid_bishop_move(test_board_2, start, end, True)  # Not diagonal

    start, end = parse_move("h2g2")
    assert not is_valid_bishop_move(test_board_2, start, end, True)  # Not diagonal


test_pawn_moves()
test_knight_moves()
test_bishop_moves()
