import itertools
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class King(Piece):
    def __init__(self, side, x, y):
        super().__init__(side, x, y)
        self.dirs = [
            (x, y) for x, y in itertools.product([-1, 0, 1], repeat=2)
            if not (x == 0 and y == 0)
        ]

# k = King(0, 0, 0)
# k.possible_move()