from enum import IntEnum

class PlayerState(IntEnum):
    ANY = 0
    CHECK = 1
    SINGLE_CHECK = 2
    DOUBLE_CHECK = 3
    CHECKMATE = 4
    STALEMATE = 5
    END = 6
    ESC = 7