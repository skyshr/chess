import itertools
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Knight(Piece):
    def __init__(self, side, x, y):
        super().__init__(side, x, y)
        self.dirs = [
            (x, y) 
            for a, b in [([-1, 1], [-2, 2]), ([-2, 2], [-1, 1])]
            for x, y in itertools.product(a, b)
    ]

# k = Knight(0, 0, 0)
# k.possible_move()