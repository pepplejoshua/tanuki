# tanuki_chess.py
board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],  # Rank 8
    ["P", "P", "P", "P", "P", "P", "P", "P"],  # Rank 7
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 6
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 5
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 4
    [".", ".", ".", ".", ".", ".", ".", "."],  # Rank 3
    ["p", "p", "p", "p", "p", "p", "p", "p"],  # Rank 2
    ["r", "n", "b", "q", "k", "b", "n", "r"],  # Rank 1
]


def print_board(board):
    for i, row in enumerate(board):
        print(f"{8 - i} | {' '.join(row)}")
    print("    a b c d e f g h")


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def parse_move(move_str):
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
    while True:
        print_board(board)
        move = input("Your move (e.g., e2e4): ")
        if move == "quit":
            break
        start, end = parse_move(move)
        move_piece(board, start, end)


play_game()
