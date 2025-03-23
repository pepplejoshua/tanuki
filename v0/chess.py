import os
from typing import Tuple
from logic_check import is_valid_move
from type_defs import Board, BoardLoc

board: Board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],  # Rank 8 (Black)
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],  # Rank 7
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 6
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 5
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 4
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 3
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],  # Rank 2 (White)
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],  # Rank 1
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board: Board):
    for i, row in enumerate(board):
        print(f"{8 - i} | {' '.join(row)}")
    print("    a b c d e f g h")


def move_piece(board: Board, start: BoardLoc, end: BoardLoc):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


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


def play_game():
    is_white_turn = True
    error_msg_from_last_turn = ""
    last_move = ""

    while True:
        clear_screen()
        print_board(board)
        print(f"\nCurrent turn: {'White' if is_white_turn else 'Black'}")
        if error_msg_from_last_turn:
            print(f"Last move '{last_move}' error: {error_msg_from_last_turn}")
            error_msg_from_last_turn = ""

        move = input("\nYour move (e.g., e2e4 or 'quit'): ")
        if move.lower() == "quit":
            break

        last_move = move

        try:
            if len(move) != 4:
                raise ValueError("Invalid move format")

            start, end = parse_move(move)
            if is_valid_move(board, start, end, is_white_turn):
                move_piece(board, start, end)
                is_white_turn = not is_white_turn
        except ValueError as e:
            error_msg_from_last_turn = str(e)
            continue


play_game()
