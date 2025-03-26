from type_defs import Board, BoardLoc, Move, MoveType
from utils import is_bishop, is_black_piece, is_knight, is_pawn, is_rook, is_white_piece


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


def is_valid_knight_move(
    board: Board, start: BoardLoc, end: BoardLoc, knight_is_white: bool
) -> bool:
    # get the differences in rank and file
    rank_diff = abs(end[0] - start[0])
    file_diff = abs(end[1] - start[1])

    # check if it's an L-shape move (2 up + 1 left | right OR 1 up + 2 left | right)
    if not ((rank_diff == 2 and file_diff == 1) or (rank_diff == 1 and file_diff == 2)):
        return False

    # check if target square has a friendly piece
    target = board[end[0]][end[1]]
    if knight_is_white:
        return not is_white_piece(target)  # can't capture own piece

    return not is_black_piece(target)  # can't capture own piece


def is_valid_bishop_move(
    board: Board, start: BoardLoc, end: BoardLoc, bishop_is_white: bool
) -> bool:
    # get the differences in rank(row) and file(column)
    rank_diff = end[0] - start[0]
    file_diff = end[1] - start[1]

    # check if move is diagonal (absolute differences should be equal)
    if abs(rank_diff) != abs(file_diff):
        return False

    # determine direction of movement
    rank_step = 1 if rank_diff > 0 else -1
    file_step = 1 if file_diff > 0 else -1

    # check path for blocking pieces
    current_rank = start[0] + rank_step
    current_file = start[1] + file_step

    # check all diagonal squares between start and end (exclusive)
    while (current_rank, current_file) != end:
        if board[current_rank][current_file] != ".":
            return False  # path is blocked
        current_rank += rank_step
        current_file += file_step

    # check destination square
    target = board[end[0]][end[1]]
    if bishop_is_white:
        return not is_white_piece(target)  # can't capture own piece
    return not is_black_piece(target)  # can't capture own piece


def is_valid_rook_move(
    board: Board, start: BoardLoc, end: BoardLoc, rook_is_white: bool
) -> bool:
    # get the difference in rank and file
    rank_diff = end[0] - start[0]
    file_diff = end[1] - start[1]

    # check if move is horizontal (same row) or vertical (same column)
    if rank_diff != 0 and file_diff != 0:  # one of them must be 0
        return False

    # determine the direction of movement
    rank_step = 0 if rank_diff == 0 else (1 if rank_diff > 0 else -1)
    file_step = 0 if file_diff == 0 else (1 if file_diff > 0 else -1)

    # check path for blocking pieces
    current_rank = start[0] + rank_step
    current_file = start[1] + file_step

    # check all squares between start and end (exclusive)
    while (current_rank, current_file) != end:
        if board[current_rank][current_file] != ".":
            return False  # path is blocked
        current_rank += rank_step
        current_file += file_step

    # check destination square
    target = board[end[0]][end[1]]
    if rook_is_white:
        return not is_white_piece(target)  # can't capture own piece
    return not is_black_piece(target)  # can't capture own piece


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

    if is_pawn(piece):
        if not is_valid_pawn_move(board, start, end, is_white_turn):
            raise ValueError("Invalid pawn move")
    elif is_knight(piece):
        if not is_valid_knight_move(board, start, end, is_white_turn):
            raise ValueError("Invalid knight move")
    elif is_bishop(piece):
        if not is_valid_bishop_move(board, start, end, is_white_turn):
            raise ValueError("Invalid bishop move")
    elif is_rook(piece):
        if not is_valid_rook_move(board, start, end, is_white_turn):
            raise ValueError("Invalid rook move")

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


def get_knight_moves(board: Board, start: BoardLoc) -> list[Move]:
    moves = []
    piece = board[start[0]][start[1]]
    is_white = is_white_piece(piece)

    # offsets to compute all possible knight moves
    offsets = [
        (-2, -1),
        (-2, 1),  # Up 2, left/right 1
        (2, -1),
        (2, 1),  # Down 2, left/right 1
        (-1, -2),
        (-1, 2),  # Up 1, left/right 2
        (1, -2),
        (1, 2),  # Down 1, left/right 2
    ]

    for rank_offset, file_offset in offsets:
        new_rank = start[0] + rank_offset
        new_file = start[1] + file_offset

        # check if the move is within board bounds
        if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
            end = (new_rank, new_file)
            target = board[new_rank][new_file]

            # determine if it's a capture or a regular move
            if target == ".":
                moves.append((end, MoveType.ADVANCE))
            elif (is_white and is_black_piece(target)) or (
                not is_white and is_white_piece(target)
            ):
                moves.append((end, MoveType.CAPTURE))

    return moves


def get_bishop_moves(board: Board, start: BoardLoc) -> list[Move]:
    moves = []
    piece = board[start[0]][start[1]]
    is_white = is_white_piece(piece)

    # check all 4 diagonal directions
    directions = [
        (-1, -1),  # North West
        (-1, 1),  # North East
        (1, -1),  # South West
        (1, 1),  # South East
    ]

    # for each direction, compute all possible squares we can
    # move to
    for rank_step, file_step in directions:
        current_rank = start[0] + rank_step
        current_file = start[1] + file_step

        # keep moving in this direction until we hit a piece or the board edge
        while 0 <= current_rank <= 7 and 0 <= current_file <= 7:
            target = board[current_rank][current_file]
            end = (current_rank, current_file)

            if target == ".":
                moves.append((end, MoveType.ADVANCE))
            elif (is_white and is_black_piece(target)) or (
                not is_white and is_white_piece(target)
            ):
                moves.append((end, MoveType.CAPTURE))
                break  # stop after a capture
            else:
                break  # stop at friendly piece

            current_rank += rank_step
            current_file += file_step

    return moves


def get_rook_moves(board: Board, start: BoardLoc) -> list[Move]:
    moves = []
    piece = board[start[0]][start[1]]
    is_white = is_white_piece(piece)

    # check all 4 directions
    directions = [
        (-1, 0),  # North
        (1, 0),  # South
        (0, -1),  # West
        (0, 1),  # East
    ]

    for rank_step, file_step in directions:
        current_rank = start[0] + rank_step
        current_file = start[1] + file_step

        # keep moving in this direction until we hit a piece or the board's edge
        while 0 <= current_rank <= 7 and 0 <= current_file <= 7:
            target = board[current_rank][current_file]
            end = (current_rank, current_file)

            if target == ".":
                moves.append((end, MoveType.ADVANCE))
            elif (is_white and is_black_piece(target)) or (
                not is_white and is_white_piece(target)
            ):
                moves.append((end, MoveType.CAPTURE))
                break  # stop after capture
            else:
                break  # stop at friendly piece

            current_rank += rank_step
            current_file += file_step

    return moves


def get_possible_moves(board: Board, start: BoardLoc) -> list[Move]:
    piece = board[start[0]][start[1]]
    if piece == ".":
        return []

    if is_pawn(piece):
        return get_pawn_moves(board, start)
    elif is_knight(piece):
        return get_knight_moves(board, start)
    elif is_bishop(piece):
        return get_bishop_moves(board, start)
    elif is_rook(piece):
        return get_rook_moves(board, start)

    return []
