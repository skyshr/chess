import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from .Piece import Piece

class Rook(Piece):
    def __init__(self, side, x, y, id):
        super().__init__(side, x, y, id)
        for _ in range(0, 8, 2):
            ux, uy = self.unit_dirs[_]
            self.dirs[_] = [(i*ux, i*uy) for i in range(1, 8)]         

# r = Rook(0, 0, 0)
# r.possible_move()