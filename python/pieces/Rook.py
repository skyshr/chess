from itertools import chain
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Rook(Piece):
    def __init__(self, side, x, y):
        super().__init__(side, x, y)
        self.dirs = list(chain(
            ((0, i) for i in range(-7, 8) if i != 0),
            ((i, 0) for i in range(-7, 8) if i != 0)
        ))            

# r = Rook(0, 0, 0)
# r.possible_move()