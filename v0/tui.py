from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.message import Message
from textual.widgets import Header, Static
from textual import events

from type_defs import BoardLoc, Move, MoveType, Board
from logic_check import get_possible_moves


class ChessSquare(Static):
    """A single square on the chess board"""

    class Selected(Message):
        """Message sent when a square is selected"""

        def __init__(self, location: BoardLoc) -> None:
            self.location = location
            super().__init__()

    DEFAULT_CSS = """
        ChessSquare {
            width: 5;
            height: 2;
            content-align: center middle;
        }

        ChessSquare.light {
            background: #ffffff;
            color: #000000;
        }

        ChessSquare.dark {
            background: #666666;
            color: #ffffff;
        }

        ChessSquare.selected {
            background: lightblue 60%;
        }

        ChessSquare.possible-move {
            background: green 90%;
        }

        ChessSquare.possible-capture {
            background: red 30%;
        }
    """

    def __init__(self, piece: str, is_light: bool, location: BoardLoc):
        super().__init__(piece)
        self.location = location
        self.add_class("light" if is_light else "dark")

    def on_click(self) -> None:
        """Handle mouse clicks on the square."""
        self.post_message(self.Selected(self.location))


class ChessBoard(Static):
    """Chess board widget."""

    DEFAULT_CSS = """
            ChessBoard {
                layout: grid;
                grid-size: 10 10;  /* 8x8 board + 2 label rows/columns */
                grid-columns: 5 5 5 5 5 5 5 5 5 5;
                grid-rows: 2 2 2 2 2 2 2 2 2 2;
                content-align: center middle;
                height: auto;
                padding-top: 2;
                border: solid green;
            }

            .label {
                width: 5;
                height: 2;
                content-align: center middle;
                color: $text;
            }
        """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_pos: BoardLoc | None = None
        self.possible_moves: list[Move] = []
        self.board = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
        ]

    def compose(self) -> ComposeResult:
        # Generate all widgets first
        widgets = []

        # Top row (files a-h)
        widgets.append(Static(" ", classes="label"))
        for file in "abcdefgh":
            widgets.append(Static(file, classes="label"))
        widgets.append(Static(" ", classes="label"))

        # Middle rows (the board itself plus rank numbers)
        for rank in range(8):
            widgets.append(Static(str(8 - rank), classes="label"))
            for file in range(8):
                is_light = (rank + file) % 2 == 0
                piece = self.board[rank][file]
                widgets.append(
                    ChessSquare(piece if piece != "." else " ", is_light, (rank, file))
                )
            widgets.append(Static(str(8 - rank), classes="label"))

        # Bottom row (files a-h again)
        widgets.append(Static(" ", classes="label"))
        for file in "abcdefgh":
            widgets.append(Static(file, classes="label"))
        widgets.append(Static(" ", classes="label"))

        # Yield all widgets
        for widget in widgets:
            yield widget

    def on_chess_square_selected(self, message: ChessSquare.Selected) -> None:
        """Handle square selection"""
        # If clicking the currently selected square, deselect it
        if self.selected_pos == message.location:
            self.selected_pos = None
            self.possible_moves = []
        else:
            self.selected_pos = message.location
            self.possible_moves = get_possible_moves(self.board, message.location)
        self.refresh_highlights()

    def refresh_highlights(self) -> None:
        """Update the visual state of all squares"""
        for y in range(8):
            for x in range(8):
                square = self._get_square_at((y, x))
                if square:
                    # Clear existing state classes
                    square.remove_class("selected")
                    square.remove_class("possible-move")
                    square.remove_class("possible-capture")

                    if (y, x) == self.selected_pos:
                        square.add_class("selected")

                    for move, move_type in self.possible_moves:
                        if (y, x) == move:
                            if move_type == MoveType.CAPTURE:
                                square.add_class("possible-capture")
                            else:
                                square.add_class("possible-move")

    def _get_square_at(self, location: BoardLoc) -> ChessSquare | None:
        """Get the ChessSquare widget at a given location"""
        try:
            widget = list(self.query(ChessSquare).results())[
                location[0] * 8 + location[1]
            ]
            return widget
        except IndexError:
            return None


class MoveHistory(Static):
    """Move history panel."""

    DEFAULT_CSS = """
        MoveHistory {
            height: 100%;
            padding: 0 0 0 1;
            border: solid blue;
        }

        .title {
            text-style: bold;
        }

        .moves-container {
            height: 90%;
            margin-top: 1;
        }
    """

    def __init__(self, id: str):
        super().__init__(id)
        self.moves: list[tuple[str, str]] = []  # (white_move, black_move)
        # Add some test moves
        # for i in range(50):
        #     self.moves.append(("e2e4", "e7e5"))

    def compose(self) -> ComposeResult:
        yield Static("Move History", classes="title")
        with ScrollableContainer(classes="moves-container"):
            # Example moves for testing
            for i, move in enumerate(self.moves):
                yield Static(
                    f"{i + 1}. {move[0]:<8} {move[1]}",
                    classes="move-row",
                )

    def add_move(self, move: str, is_white: bool) -> None:
        if is_white:
            self.moves.append((move, ""))
        else:
            if not self.moves:
                self.moves.append(("", move))
            else:
                temp = (self.moves[-1][0], move)
                self.moves[-1] = temp
        self.refresh_moves()

    def refresh_moves(self) -> None:
        scroll_container = self.query_one(ScrollableContainer)
        scroll_container.remove_children()

        for i, (white_move, black_move) in enumerate(self.moves, 1):
            move_text = f"{i}. {white_move:<8} {black_move}"
            scroll_container.mount(Static(move_text, classes="move-row"))


class GameInfo(Static):
    """Game information panel."""

    DEFAULT_CSS = """
        GameInfo {
            height: 100%;
            padding-left: 1;
            border: solid red;
        }

        .title {
            text-style: bold;
        }

        .info-container {
            margin-top: 1;
        }
    """

    def compose(self) -> ComposeResult:
        yield Static("Game Info", classes="title")
        with Vertical(classes="info-container"):
            yield Static("Selected: None", id="selected-piece")
            yield Static("", id="possible-moves")

    def update_info(
        self,
        selected_pos: BoardLoc | None,
        board: Board,
        possible_moves: list[Move],
    ) -> None:
        """Update game info based on board state"""
        selected = self.query_one("#selected-piece", Static)
        moves = self.query_one("#possible-moves", Static)

        if selected_pos is None:
            selected.update("Selected: None")
            moves.update("")
        else:
            y, x = selected_pos
            piece = board[y][x]
            selected.update(f"Selected: {piece} at {chr(x + 97)}{8 - y}")

            # Show possible moves in algebraic notation
            moves_text = "\nPossible moves:\n"
            for move, move_type in possible_moves:
                move_y, move_x = move
                notation = f"{chr(move_x + 97)}{8 - move_y}"
                moves_text += f"• {notation} ({move_type.value})\n"
            moves.update(moves_text)


class CommandBar(Static):
    """Command input bar."""

    DEFAULT_CSS = """
        CommandBar {
            height: 100%;
            padding-left: 1;
            border: solid yellow;
        }

        .title {
            text-style: bold;
        }
    """

    def compose(self) -> ComposeResult:
        yield Static("Command Bar", classes="title")


class Tanuki(App):
    """The main chess application."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 45% 55%;
        grid-rows: 1fr auto;
    }

     #side-panel {
        layout: grid;
        grid-size: 2;
        grid-rows: 1fr 1fr;
        height: 100%;
        width: 100%;
    }

    #side-content {
        width: 100%;
        height: 100%;
    }

    #board-area {
        width: 100%;
        height: 100%;
    }

    #move-history {
        width: 100%;
        height: 100%;
    }

    #game-info {
        width: 100%;
        height: 50%;
    }

    #command-bar {
        width: 100%;
        height: 50%;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ChessBoard(id="board-area")

        with Horizontal(id="side-panel"):
            with Vertical(id="side-content"):
                yield GameInfo(id="game-info")
                yield CommandBar(id="command-bar")
            yield MoveHistory(id="move-history")

    def on_chess_square_selected(self, message: ChessSquare.Selected) -> None:
        """Update game info when a square is selected"""
        board = self.query_one(ChessBoard)
        game_info = self.query_one(GameInfo)
        game_info.update_info(board.selected_pos, board.board, board.possible_moves)

    def on_key(self, event: events.Key) -> None:
        board = self.query_one(ChessBoard)
        game_info = self.query_one(GameInfo)
        game_info.update_info(board.selected_pos, board.board, [])

        # Initialize cursor if not set
        if board.selected_pos is None:
            board.selected_pos = (0, 0)
            board.possible_moves = get_possible_moves(board.board, (0, 0))
            board.refresh_highlights()
            game_info.update_info(board.selected_pos, board.board, board.possible_moves)
            return

        y, x = board.selected_pos
        match event.key:
            case "up" if y > 0:
                board.selected_pos = (y - 1, x)
            case "down" if y < 7:
                board.selected_pos = (y + 1, x)
            case "left" if x > 0:
                board.selected_pos = (y, x - 1)
            case "right" if x < 7:
                board.selected_pos = (y, x + 1)
            case "escape":
                board.selected_pos = None
                board.possible_moves = []
            case "enter" | "space":
                # should show possible moves on current selection
                if board.selected_pos:  # placeholder
                    board.selected_pos = None
                    board.possible_moves = []

        if board.selected_pos is not None:
            board.possible_moves = get_possible_moves(board.board, board.selected_pos)
        board.refresh_highlights()
        game_info.update_info(board.selected_pos, board.board, board.possible_moves)


if __name__ == "__main__":
    app = Tanuki()
    app.run()
