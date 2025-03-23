import os
from type_defs import Board, BoardLoc, Move, MoveType
from typing import Tuple, Union


def is_black_piece(piece: str) -> bool:
    return piece in "♚♛♜♝♞♟"


def is_white_piece(piece: str) -> bool:
    return piece in "♔♕♖♗♘♙"


def is_pawn(piece: str) -> bool:
    return piece in "♙♟"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def move_piece(board: Board, start: BoardLoc, end: BoardLoc):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def loc_to_notation(loc: BoardLoc) -> str:
    files = "abcdefgh"
    rank = 8 - loc[0]
    file = files[loc[1]]
    return f"{file}{rank}"


def notation_to_loc(notation: str) -> BoardLoc:
    # "e2" -> (6, 4)
    files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    file, rank = notation[0], notation[1]
    return (8 - int(rank), files[file])


def parse_move(move_str: str) -> Tuple[BoardLoc, BoardLoc]:
    # "e2e4" -> ((6, 4), (4, 4))
    return (notation_to_loc(move_str[:2]), notation_to_loc(move_str[2:]))


# Terminal colors
RESET = "\033[0m"
BG_GREEN = "\033[42m"
BG_BLUE = "\033[44m"
BG_RED = "\033[41m"
# Keep these for possible moves list only
FG_BLUE = "\033[34m"
FG_RED = "\033[31m"


def print_colored_board(
    board: Board,
    selected: Union[BoardLoc, None] = None,
    moves: Union[list[Move], None] = None,
):
    moves = moves or []
    move_locs = {loc for loc, _ in moves}
    move_types = {loc: move_type for loc, move_type in moves}

    for i, row in enumerate(board):
        print(f"{8 - i} |", end=" ")
        for j, piece in enumerate(row):
            if selected and (i, j) == selected:
                # Highlight selected piece with green background
                print(f"{BG_GREEN}{piece}{RESET}", end=" ")
            elif (i, j) in move_locs:
                move_type = move_types[(i, j)]
                if piece == ".":
                    if move_type == MoveType.ADVANCE:
                        # Blue background for normal moves
                        print(f"{BG_BLUE}•{RESET}", end=" ")
                    elif move_type == MoveType.DOUBLE_ADVANCE:
                        # Different symbol for double advance
                        print(f"{BG_BLUE}◊{RESET}", end=" ")
                else:  # Capture
                    print(f"{BG_RED}{piece}{RESET}", end=" ")
            else:
                # Normal pieces without color
                print(piece, end=" ")
        print()
    print("    a b c d e f g h")


def print_possible_moves(start_notation: str, moves: list[Move]):
    print(f"\nPossible moves from {start_notation}:")
    for move, move_type in moves:
        end_notation = loc_to_notation(move)
        if move_type == MoveType.CAPTURE:
            print(
                f"  {FG_RED}{start_notation}{end_notation}{RESET} ({move_type.value})"
            )
        elif move_type == MoveType.DOUBLE_ADVANCE:
            print(
                f"  {FG_BLUE}{start_notation}{end_notation}{RESET} ({move_type.value})"
            )
        else:  # normal advance
            print(
                f"  {FG_BLUE}{start_notation}{end_notation}{RESET} ({move_type.value})"
            )


#
def print_board(board: Board):
    for i, row in enumerate(board):
        print(f"{8 - i} | {' '.join(row)}")
    print("    a b c d e f g h")
