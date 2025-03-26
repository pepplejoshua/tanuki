from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Static


class ChessSquare(Static):
    """A single square on the chess board"""

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
    """

    def __init__(self, piece: str, is_light: bool):
        super().__init__(piece)
        self.add_class("light" if is_light else "dark")


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
                padding-top: 1;
                border: solid green;
            }

            .label {
                width: 5;
                height: 2;
                content-align: center middle;
                color: $text;
            }
        """

    def compose(self) -> ComposeResult:
        board = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
        ]

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
                piece = board[rank][file]
                widgets.append(ChessSquare(piece if piece != "." else " ", is_light))
            widgets.append(Static(str(8 - rank), classes="label"))

        # Bottom row (files a-h again)
        widgets.append(Static(" ", classes="label"))
        for file in "abcdefgh":
            widgets.append(Static(file, classes="label"))
        widgets.append(Static(" ", classes="label"))

        # Yield all widgets
        for widget in widgets:
            yield widget


class MoveHistory(Static):
    """Move history panel."""

    DEFAULT_CSS = """
        MoveHistory {
            height: 100%;
            padding-left: 1;
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
        # Test
        for i in range(50):  # Add some test moves
            self.moves.append(("e2e4", "e7e5"))

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
    """

    def compose(self) -> ComposeResult:
        yield Static("Game Info")


class CommandBar(Static):
    """Command input bar."""

    DEFAULT_CSS = """
        CommandBar {
            border: solid yellow;
        }
    """

    def compose(self) -> ComposeResult:
        yield Static("Command Bar")


class ChessApp(App):
    """The main chess application."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 50% 50%;
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


if __name__ == "__main__":
    app = ChessApp()
    app.run()
