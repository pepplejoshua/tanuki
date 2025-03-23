import os
from type_defs import Board, BoardLoc
from typing import Tuple


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board: Board):
    for i, row in enumerate(board):
        print(f"{8 - i} | {' '.join(row)}")
    print("    a b c d e f g h")


def move_piece(board: Board, start: BoardLoc, end: BoardLoc):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def loc_to_notation(loc: BoardLoc) -> str:
    files = "abcdefgh"
    rank = 8 - loc[0]
    file = files[loc[1]]
    return f"{file}{rank}"


def parse_move(move_str: str) -> Tuple[BoardLoc, BoardLoc]:
    # "e2e4" -> ((6, 4), (4, 4))
    files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    start_file, start_rank, end_file, end_rank = (
        move_str[0],
        move_str[1],
        move_str[2],
        move_str[3],
    )
    start = (8 - int(start_rank), files[start_file])
    end = (8 - int(end_rank), files[end_file])
    return start, end
