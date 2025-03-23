from type_defs import Board, BoardLoc, Move, MoveType
from utils import is_white_piece, is_black_piece, is_pawn


def is_valid_pawn_move(
    board: Board, start: BoardLoc, end: BoardLoc, pawn_is_white: bool
) -> bool:
    target = board[end[0]][end[1]]

    # determine the direction of movement
    direction = -1 if pawn_is_white else 1

    # normal forward move (no capture allowed)
    if start[1] == end[1]:  # we are moving along the same column / file
        # 1 square move
        if end[0] == start[0] + direction:
            return target == "."  # must move to an empty square

        # first move of a pawn can be 2 squares
        # white pawns start at rank 2 (8 total ranks - 6th index)
        # Black pawns start at rank 7 (8 total ranks - 1st index)
        if (pawn_is_white and start[0] == 6) or (not pawn_is_white and start[0] == 1):
            if end[0] == start[0] + 2 * direction:
                middle_square = board[start[0] + direction][start[1]]
                return (
                    target == "." and middle_square == "."
                )  # both squares must be empty

    # diagonal capture of opponent piece
    # we check that the end row (rank) is 1 ahead of the start row (rank)
    # and
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
    # if it was white's turn and they entered e4d5,
    # direction = -1
    # which converts to the piece move operation (4, 4) -> (3, 3)
    # we can see that the end[0] (3) == start[0] + (-1) (4 - 1 = 3)
    # we can also confirm that end[1] - start[1] |3 - 4| = 1
    # the same proof holds if the black piece was on f5
    if end[0] == start[0] + direction and abs(end[1] - start[1]) == 1:
        if pawn_is_white:
            return is_black_piece(target)
        return is_white_piece(target)

    return False


def is_valid_move(
    board: Board, start: BoardLoc, end: BoardLoc, is_white_turn: bool
) -> bool:
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
        raise ValueError(f"White's turn but trying to move {piece}")
    if not is_white_turn and not is_black_piece(piece):
        raise ValueError(f"Black's turn but trying to move {piece}")

    # Pawn movement
    if is_pawn(piece):
        if not is_valid_pawn_move(board, start, end, is_white_turn):
            raise ValueError("Invalid pawn move")

    # Temporarily allow all moves
    return True


def get_pawn_moves(board: Board, start: BoardLoc) -> list[Move]:
    moves = []
    piece = board[start[0]][start[1]]
    is_white = is_white_piece(piece)
    direction = -1 if is_white else 1

    # Forward moves
    forward = (start[0] + direction, start[1])
    if 0 <= forward[0] <= 7:
        if board[forward[0]][forward[1]] == ".":
            moves.append((forward, MoveType.ADVANCE))
            # First move can be two squares
            if (is_white and start[0] == 6) or (not is_white and start[0] == 1):
                two_forward = (start[0] + 2 * direction, start[1])
                if board[two_forward[0]][two_forward[1]] == ".":
                    moves.append((two_forward, MoveType.DOUBLE_ADVANCE))

    # Diagonal captures
    for file_offset in [-1, 1]:
        new_file = start[1] + file_offset
        if 0 <= new_file <= 7:
            capture = (start[0] + direction, new_file)
            if 0 <= capture[0] <= 7:
                target = board[capture[0]][capture[1]]
                if (is_white and is_black_piece(target)) or (
                    not is_white and is_white_piece(target)
                ):
                    moves.append((capture, MoveType.CAPTURE))

    return moves


def get_possible_moves(board: Board, start: BoardLoc) -> list[Move]:
    piece = board[start[0]][start[1]]
    if piece == ".":
        return []

    if is_pawn(piece):
        return get_pawn_moves(board, start)

    return []
