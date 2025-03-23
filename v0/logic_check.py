from type_defs import Board, BoardLoc


def is_black_piece(piece):
    return piece in "♚♛♜♝♞♟"


def is_white_piece(piece):
    return piece in "♔♕♖♗♘♙"


def is_pawn(piece):
    return piece in "♙♟"


def is_valid_pawn_move(board, start, end, pawn_is_white):
    target = board[end[0]][end[1]]

    # determine the direction of movement
    direction = -1 if pawn_is_white else 1

    # check for a normal 1 square forward move
    if start[1] == end[1] and end[0] == start[0] + direction:
        return target == "."

    # first move of a pawn can be 2 squares
    if (pawn_is_white and start[0] == 6) or (not pawn_is_white and start[0] == 1):
        if start[1] == end[1] and end[0] == start[0] + 2 * direction:
            middle_square = board[start[0] + direction][start[1]]
            return target == "." and middle_square == "."

    # diagonal capture of opponent piece
    # we check that the end row (rank) is 1 ahead of the start row (rank)
    # AND
    # that the end column (file) is 1 less or 1 greater than the start column (file)
    # For example with this board:
    # 8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
    # 7 | ♟ ♟ ♟ . ♟ ♟ ♟ ♟
    # 6 | . . . . . . . .
    # 5 | . . . ♟ . . . .
    # 4 | . . . . ♙ . . .
    # 3 | . . . . . . . .
    # 2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙
    # 1 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    #     a b c d e f g h
    #
    # If it was white's turn and they entered e4d5,
    # direction = -1
    # which converts to the piece move operation (4, 4) -> (3, 3)
    # We can see that the end[0] (3) == start[0] + (-1) (4 - 1 = 3)
    # We can also confirm that end[1] - start[1] |3 - 4| = 1
    # The same proof holds if the black piece was on f5
    if end[0] == start[0] + direction and abs(end[1] - start[1]) == 1:
        if pawn_is_white:
            return is_black_piece(target)
        return is_white_piece(target)

    return False


def is_valid_move(board: Board, start: BoardLoc, end: BoardLoc, is_white_turn: bool):
    # Basic checks to make sure the end and start coordinates are
    # actually within the bounds of the board
    if not (
        0 <= start[0] <= 7
        and 0 <= start[1] <= 7
        and 0 <= end[0] <= 7
        and 0 <= end[1] <= 7
    ):
        return False  # Out of Bounds

    piece = board[start[0]][start[1]]

    # Can't move an empty square
    if piece == ".":
        return False

    # Check if moving the correct color
    if is_white_turn and not is_white_piece(piece):
        raise ValueError("Not your piece to move")
    if not is_white_turn and not is_black_piece(piece):
        raise ValueError("Not your piece to move")

    # Pawn movement
    if is_pawn(piece):
        if not is_valid_pawn_move(board, start, end, is_white_turn):
            raise ValueError("Invalid pawn move")

    # Temporarily allow all moves
    return True
