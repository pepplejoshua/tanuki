import os
from type_defs import Board, BoardLoc
from typing import Tuple, Union


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


def print_colored_board(
    board: Board,
    selected: Union[BoardLoc, None] = None,
    moves: Union[list[BoardLoc], None] = None,
):
    moves = moves or []
    for i, row in enumerate(board):
        print(f"{8 - i} |", end=" ")
        for j, piece in enumerate(row):
            if selected and (i, j) == selected:
                print(f"{BG_GREEN}{piece}{RESET}", end=" ")
            elif (i, j) in moves:
                if piece == ".":
                    print(f"{BG_BLUE}.{RESET}", end=" ")
                else:
                    print(f"{BG_RED}{piece}{RESET}", end=" ")
            else:
                print(piece, end=" ")
        print()
    print("    a b c d e f g h")


def print_board(board: Board):
    for i, row in enumerate(board):
        print(f"{8 - i} | {' '.join(row)}")
    print("    a b c d e f g h")
