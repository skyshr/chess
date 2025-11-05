from itertools import chain
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Bishop(Piece):
    def __init__(self, side, x, y):
        super().__init__(side, x, y)
        self.dirs = list(chain(
            ((i, i) for i in range(-7, 8) if i != 0),
            ((i, -i) for i in range(-7, 8) if i != 0)
        ))
            

# b = Bishop(0, 0, 0)
# b.possible_move()