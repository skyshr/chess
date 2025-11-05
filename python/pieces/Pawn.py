import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Pawn(Piece):
    def __init__(self, side, x, y):
        super().__init__(side, x, y)

# p = Pawn(0, 0, 0)
# p.possible_move()