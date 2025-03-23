from logic_check import is_valid_move, get_possible_moves
from type_defs import Board
from utils import (
    clear_screen,
    loc_to_notation,
    notation_to_loc,
    move_piece,
    parse_move,
    print_board,
    print_colored_board,
)

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

                    # Print possible moves in notation
                    print(f"\nPossible moves from {last_move}:")
                    for move in possible_moves:
                        print(f"  {last_move}{loc_to_notation(move)}")
                else:
                    print_board(board)
                    error_msg = "Empty square selected"
            except (ValueError, IndexError):
                print_board(board)
                error_msg = "Invalid square"
        else:
            print_board(board)

        print(f"\nCurrent turn: {'White' if is_white_turn else 'Black'}")
        if error_msg:
            print(f"Error: {error_msg}")
            error_msg = ""

        move = input("\nYour move (e.g., e2e4, e2 for preview, or 'quit'): ")
        if move.lower() == "quit":
            break

        last_move = move

        if len(move) == 4:  # Regular move
            try:
                start, end = parse_move(move)
                if is_valid_move(board, start, end, is_white_turn):
                    move_piece(board, start, end)
                    is_white_turn = not is_white_turn
                    last_move = ""
            except ValueError as e:
                error_msg = str(e)


play_game()
