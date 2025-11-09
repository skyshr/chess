import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class King(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for _ in range(7):
            self.dirs[_] = [self.unit_dirs[_]]

# k = King(0, 0, 0)
# k.possible_move()