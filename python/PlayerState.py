from enum import IntEnum

class PlayerState(IntEnum):
    ANY = 0
    SINGLE_CHECK = 1
    DOUBLE_CHECK = 2
    CHECKMATE = 3