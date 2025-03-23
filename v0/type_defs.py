from typing import Tuple
from enum import Enum

BoardLoc = Tuple[int, int]
Board = list[list[str]]


class MoveType(Enum):
    ADVANCE = "Advance"
    CAPTURE = "Capture"
    DOUBLE_ADVANCE = "Double Advance"  # for pawn's first move


Move = Tuple[BoardLoc, MoveType]
