from logic_check import is_valid_move
from utils import print_board, clear_screen, parse_move, move_piece
from type_defs import Board

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
