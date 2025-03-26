from logic_check import is_valid_move, get_possible_moves
from type_defs import Board
from utils import (
    clear_screen,
    notation_to_loc,
    move_piece,
    parse_move,
    print_board,
    print_colored_board,
    print_possible_moves,
    teleport_piece,
)

board: Board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],  # Rank 8
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],  # Rank 7 (Black)
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 6
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 5
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 4
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 3
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],  # Rank 2 (White)
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],  # Rank 1
]


def play_game():
    is_white_turn = True
    error_msg = ""
    last_move = ""

    while True:
        clear_screen()

        if len(last_move) == 2:  # Preview mode
            try:
                start = notation_to_loc(last_move)
                piece = board[start[0]][start[1]]
                if piece != ".":
                    possible_moves = get_possible_moves(board, start)
                    print_colored_board(board, start, possible_moves)
                    print_possible_moves(last_move, possible_moves)
                else:
                    print_board(board)
                    error_msg = "Empty square selected"
            except (ValueError, IndexError):
                print_board(board)
                error_msg = "Invalid square"
        else:
            print_board(board)

        print(f"\nCurrent turn: {'White' if is_white_turn else 'Black'}")
        print(f"Last Move: \033[38;5;208m{last_move}\033[0m")
        if error_msg:
            print(f"Error: {error_msg}")
            error_msg = ""

        move = input(
            "\nYour move (e.g., e2e4, e2 for preview, or 'q' or 'quit' to exit): "
        ).lower()
        if move == "quit" or move == "q":
            break

        last_move = move
        if move.startswith(";") and len(move) == 5:
            try:
                start, end = parse_move(move[1:])
                teleport_piece(board, start, end)
                continue
            except (ValueError, IndexError) as e:
                error_msg = f"Invalid teleport: {e}"
                continue

        if len(move) == 4:  # Regular move
            try:
                start, end = parse_move(move)
                if is_valid_move(board, start, end, is_white_turn):
                    move_piece(board, start, end)
                    is_white_turn = not is_white_turn
            except ValueError as e:
                error_msg = str(e)


play_game()
